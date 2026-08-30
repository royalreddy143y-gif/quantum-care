from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, UserOut, Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new healthcare researcher or student account."""
    email_clean = user_in.email.strip().lower()
    existing_user = db.query(User).filter(User.email == email_clean).first()
    
    # Also check MongoDB Atlas
    from app.database.mongodb import get_mongo_db, mongo_upsert_user
    mongo_db = get_mongo_db()
    if not existing_user and mongo_db is not None:
        try:
            mongo_user = mongo_db.users.find_one({"email": email_clean})
            if mongo_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A user with this email already exists."
                )
        except HTTPException:
            raise
        except Exception:
            pass

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists."
        )

    hashed_pw = get_password_hash(user_in.password)
    user = User(
        email=email_clean,
        hashed_password=hashed_pw,
        full_name=user_in.full_name.strip(),
        role=user_in.role or "researcher",
        institution=user_in.institution or "QuantumCare Medical Institute",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Sync persistent user credentials to MongoDB Atlas
    try:
        mongo_upsert_user({
            "id": user.id,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "full_name": user.full_name,
            "role": user.role,
            "institution": user.institution,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        })
    except Exception as ex:
        print(f"[*] MongoDB user sync notice: {ex}")

    return user


@router.post("/login", response_model=Token)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate and obtain JWT bearer token."""
    email_clean = credentials.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    
    # If user not found in local ephemeral DB (e.g. after Render restart), look up in persistent MongoDB Atlas
    if not user:
        from app.database.mongodb import get_mongo_db
        mongo_db = get_mongo_db()
        if mongo_db is not None:
            try:
                mongo_user = mongo_db.users.find_one({"email": email_clean})
                if mongo_user and "hashed_password" in mongo_user:
                    if verify_password(credentials.password, mongo_user["hashed_password"]):
                        # Restore user to local DB
                        user = User(
                            email=mongo_user["email"],
                            hashed_password=mongo_user["hashed_password"],
                            full_name=mongo_user.get("full_name", "Clinician / Researcher"),
                            role=mongo_user.get("role", "researcher"),
                            institution=mongo_user.get("institution", "QuantumCare Medical Institute"),
                            is_active=mongo_user.get("is_active", True)
                        )
                        db.add(user)
                        db.commit()
                        db.refresh(user)
            except Exception as ex:
                print(f"[*] MongoDB auth recovery notice: {ex}")

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is disabled")

    access_token = create_access_token(subject=user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
def logout_user():
    """Client-side token invalidation confirmation."""
    return {"message": "Successfully logged out. Please clear authorization header."}


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Return currently authenticated researcher profile."""
    return current_user
