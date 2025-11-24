from fastapi import APIRouter, Depends
from src.core.firebase import verify_firebase_token
from src.services.firestore_service import FirestoreService

router = APIRouter()
service = FirestoreService()

@router.get("/")
def list_users(decoded = Depends(verify_firebase_token)):
    # return service.get_all("users")
    return ''