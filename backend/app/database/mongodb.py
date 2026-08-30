import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import pymongo
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.core.config import settings

logger = logging.getLogger("quantumcare.mongodb")

_client: Optional[MongoClient] = None


def get_mongo_client() -> Optional[MongoClient]:
    """
    Returns or initializes the singleton MongoDB client connection.
    """
    global _client
    if _client is None and settings.MONGODB_URI:
        try:
            _client = MongoClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                retryWrites=True,
                w="majority",
                appName="QuantumCare"
            )
            # Test connection with a quick ping
            _client.admin.command("ping")
            logger.info("[+] Successfully connected to MongoDB Atlas!")
        except Exception as e:
            logger.error(f"[!] MongoDB Atlas connection error: {e}")
            _client = None
    return _client


def get_mongo_db() -> Optional[Database]:
    """
    Returns the active MongoDB database instance.
    """
    client = get_mongo_client()
    if client:
        return client[settings.MONGODB_DB_NAME]
    return None


def get_collection(collection_name: str) -> Optional[Collection]:
    """
    Returns a collection from the active MongoDB database.
    """
    db = get_mongo_db()
    if db is not None:
        return db[collection_name]
    return None


def check_mongo_health() -> Dict[str, Any]:
    """
    Lightweight health check for MongoDB Atlas.
    """
    if not settings.MONGODB_URI:
        return {"status": "unconfigured", "connected": False, "message": "MONGODB_URI not provided"}

    client = get_mongo_client()
    if client is None:
        return {"status": "disconnected", "connected": False, "error": "Client initialization failed"}

    try:
        start = datetime.now(timezone.utc)
        client.admin.command("ping")
        latency_ms = round((datetime.now(timezone.utc) - start).total_seconds() * 1000, 2)
        db = client[settings.MONGODB_DB_NAME]
        collections = db.list_collection_names()
        return {
            "status": "healthy",
            "connected": True,
            "database": settings.MONGODB_DB_NAME,
            "latency_ms": latency_ms,
            "collections": collections
        }
    except Exception as ex:
        return {"status": "degraded", "connected": False, "error": str(ex)}


def init_mongo_indexes():
    """
    Ensures optimal indexes exist in MongoDB Atlas collections.
    """
    try:
        db = get_mongo_db()
        if db is None:
            return

        # Users collection
        db.users.create_index("email", unique=True)
        db.users.create_index("created_at")

        # Patients collection
        db.patients.create_index("patient_id")
        db.patients.create_index("user_id")

        # Analyses collection
        db.analyses.create_index("analysis_code", unique=True)
        db.analyses.create_index("patient_id")
        db.analyses.create_index("created_at")

        # Medical Images
        db.medical_images.create_index("patient_id")

        # Predictions
        db.predictions.create_index("analysis_id")

        logger.info("[+] MongoDB Atlas indexes initialized successfully.")
    except Exception as e:
        logger.warning(f"[*] Notice initializing MongoDB indexes: {e}")


# ==============================================================================
# Helper methods to mirror/sync application documents to MongoDB Atlas
# ==============================================================================

def mongo_upsert_user(user_data: Dict[str, Any]):
    """Sync user account to MongoDB Atlas."""
    coll = get_collection("users")
    if coll is not None:
        try:
            coll.update_one(
                {"email": user_data["email"]},
                {"$set": {**user_data, "updated_at": datetime.now(timezone.utc).isoformat()}},
                upsert=True
            )
        except Exception as e:
            logger.warning(f"[*] MongoDB user sync notice: {e}")


def mongo_save_patient(patient_data: Dict[str, Any]):
    """Sync patient record to MongoDB Atlas."""
    coll = get_collection("patients")
    if coll is not None:
        try:
            coll.update_one(
                {"patient_id": patient_data["patient_id"]},
                {"$set": {**patient_data, "updated_at": datetime.now(timezone.utc).isoformat()}},
                upsert=True
            )
        except Exception as e:
            logger.warning(f"[*] MongoDB patient sync notice: {e}")


def mongo_save_analysis_record(analysis_data: Dict[str, Any], prediction_data: Optional[Dict[str, Any]] = None):
    """Sync full hybrid analysis and quantum telemetry outcome to MongoDB Atlas."""
    coll = get_collection("analyses")
    if coll is not None:
        try:
            doc = {
                **analysis_data,
                "prediction": prediction_data,
                "synced_at": datetime.now(timezone.utc).isoformat()
            }
            coll.update_one(
                {"analysis_code": analysis_data["analysis_code"]},
                {"$set": doc},
                upsert=True
            )
        except Exception as e:
            logger.warning(f"[*] MongoDB analysis sync notice: {e}")
