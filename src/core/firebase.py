import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Header
import json

def _ensure_firebase_initialized():
    """Initialize Firebase Admin using env variable FIREBASE_SERVICE_ACCOUNT_JSON."""
    try:
        firebase_admin.get_app()
        return  # already initialized
    except ValueError:
        pass

    if "FIREBASE_SERVICE_ACCOUNT_JSON" not in os.environ:
        raise RuntimeError(
            "Missing FIREBASE_SERVICE_ACCOUNT_JSON environment variable."
        )

    sa_dict = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT_JSON"])
    cred = credentials.Certificate(sa_dict)

    try:
        firebase_admin.initialize_app(cred)
        print("Firebase initialized from FIREBASE_SERVICE_ACCOUNT_JSON")
    except Exception as exc:
        # Don't hide initialization errors: surface them so developer can fix credentials
        print("Failed to initialize Firebase:", exc)
        raise


_ensure_firebase_initialized()


def verify_firebase_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]

    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
