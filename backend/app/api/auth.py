import random
import time
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.auth import (
    UserCreate,
    UserLogin,
    UserOut,
    Token,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ProfileUpdateRequest,
    ChangePasswordRequest
)
from app.core.security import verify_password, get_password_hash, create_access_token
from app.api.deps import get_current_user
from app.database.mongodb import get_mongo_db, mongo_upsert_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

# In-memory recovery code cache: { email: { "code": "123456", "expires_at": timestamp } }
_recovery_codes: Dict[str, Dict[str, Any]] = {}


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new healthcare researcher or student account."""
    email_clean = user_in.email.strip().lower()
    existing_user = db.query(User).filter(User.email == email_clean).first()
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


@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Generates a secure 6-digit password reset recovery code for the given email.
    """
    email_clean = req.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    
    # Also check MongoDB Atlas
    mongo_db = get_mongo_db()
    mongo_user = None
    if not user and mongo_db is not None:
        try:
            mongo_user = mongo_db.users.find_one({"email": email_clean})
        except Exception:
            pass

    if not user and not mongo_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No account found with this email address."
        )

    # Generate 6-digit recovery code
    code = f"{random.randint(100000, 999999)}"
    expires_at = time.time() + (15 * 60)  # 15 minutes expiration
    _recovery_codes[email_clean] = {"code": code, "expires_at": expires_at}

    # Also persist to MongoDB Atlas if available
    if mongo_db is not None:
        try:
            mongo_db.password_resets.update_one(
                {"email": email_clean},
                {"$set": {"code": code, "expires_at": expires_at}},
                upsert=True
            )
        except Exception:
            pass

    return {
        "status": "success",
        "message": f"Verification code sent. For immediate recovery, your code is: {code}",
        "email": email_clean,
        "reset_code": code
    }


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Validates recovery code and updates the user's password across SQLite and MongoDB Atlas.
    """
    email_clean = req.email.strip().lower()
    code_entered = req.reset_code.strip()

    # Check in-memory recovery cache
    record = _recovery_codes.get(email_clean)
    valid_code = False

    if record and record["code"] == code_entered and time.time() <= record["expires_at"]:
        valid_code = True
    else:
        # Check MongoDB Atlas
        mongo_db = get_mongo_db()
        if mongo_db is not None:
            try:
                db_record = mongo_db.password_resets.find_one({"email": email_clean})
                if db_record and db_record.get("code") == code_entered and time.time() <= db_record.get("expires_at", 0):
                    valid_code = True
            except Exception:
                pass

    if not valid_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset code. Please request a new recovery code."
        )

    new_hash = get_password_hash(req.new_password)
    user = db.query(User).filter(User.email == email_clean).first()
    
    if user:
        user.hashed_password = new_hash
        db.commit()
        db.refresh(user)

    # Sync updated password to MongoDB Atlas
    mongo_db = get_mongo_db()
    if mongo_db is not None:
        try:
            mongo_db.users.update_one(
                {"email": email_clean},
                {"$set": {"hashed_password": new_hash}}
            )
            # Clean up reset code
            mongo_db.password_resets.delete_one({"email": email_clean})
        except Exception as ex:
            print(f"[*] MongoDB password reset sync notice: {ex}")

    _recovery_codes.pop(email_clean, None)

    return {
        "status": "success",
        "message": "Your password has been successfully reset. Please sign in with your new credentials."
    }


@router.put("/profile", response_model=UserOut)
def update_profile(
    profile_in: ProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates the authenticated clinician / researcher's profile name, email, or institution.
    """
    old_email = current_user.email
    new_email = profile_in.email.strip().lower() if profile_in.email else None

    # Check if new email is already taken by another user
    if new_email and new_email != old_email:
        conflict = db.query(User).filter(User.email == new_email, User.id != current_user.id).first()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This email address is already in use by another account."
            )
        
        # Check MongoDB Atlas
        mongo_db = get_mongo_db()
        if mongo_db is not None:
            try:
                mongo_conflict = mongo_db.users.find_one({"email": new_email})
                if mongo_conflict and mongo_conflict.get("id") != current_user.id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="This email address is already in use by another account."
                    )
            except HTTPException:
                raise
            except Exception:
                pass

        current_user.email = new_email

    if profile_in.full_name:
        current_user.full_name = profile_in.full_name.strip()
    if profile_in.institution:
        current_user.institution = profile_in.institution.strip()

    db.commit()
    db.refresh(current_user)

    # Sync updated profile to MongoDB Atlas
    mongo_db = get_mongo_db()
    if mongo_db is not None:
        try:
            mongo_db.users.update_one(
                {"email": old_email},
                {"$set": {
                    "email": current_user.email,
                    "full_name": current_user.full_name,
                    "institution": current_user.institution
                }},
                upsert=True
            )
        except Exception as ex:
            print(f"[*] MongoDB profile update sync notice: {ex}")

    return current_user


@router.put("/change-password")
def change_password(
    req: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Updates the authenticated user's password after verifying their current password.
    """
    if not verify_password(req.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect."
        )

    new_hash = get_password_hash(req.new_password)
    current_user.hashed_password = new_hash
    db.commit()
    db.refresh(current_user)

    # Sync updated password to MongoDB Atlas
    mongo_db = get_mongo_db()
    if mongo_db is not None:
        try:
            mongo_db.users.update_one(
                {"email": current_user.email},
                {"$set": {"hashed_password": new_hash}}
            )
        except Exception as ex:
            print(f"[*] MongoDB password change sync notice: {ex}")

    return {
        "status": "success",
        "message": "Password changed successfully."
    }


@router.post("/logout")
def logout_user():
    """Client-side token invalidation confirmation."""
    return {"message": "Successfully logged out. Please clear authorization header."}


@router.get("/me", response_model=UserOut)
def read_current_user(current_user: User = Depends(get_current_user)):
    """Return currently authenticated researcher profile."""
    return current_user
