from fastapi import APIRouter, Depends, HTTPException
from src.core.firestore import get_db
from src.core.firebase import verify_firebase_token

router = APIRouter()

@router.get("/config")
async def get_user_config(
    current_user = Depends(verify_firebase_token),
    db = Depends(get_db)
):
    user_id = current_user["uid"]

    # 1. Obtener userAccount
    user_doc = db.collection("users").document(user_id).get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_doc.to_dict()

    # Determinar accountId (igual que tu lógica actual)
    account_id = user_data["accountId"] if user_data["role"] != "account" else user_id

    # 2. Header Config
    header = (
        db.collection("config")
        .document(account_id)
        .collection("settings")
        .document("header")
        .get()
    )
    header_config = header.to_dict() if header.exists else {}

    # 3. Data Config
    data = (
        db.collection("config")
        .document(account_id)
        .collection("settings")
        .document("data")
        .get()
    )
    data_config = data.to_dict() if data.exists else {}

    # 4. Obtener todos los usuarios de esa cuenta
    users_query = (
        db.collection("users")
        .where("accountId", "==", account_id)
        .stream()
    )
    users = [doc.to_dict() | {"id": doc.id} for doc in users_query]

    return {
        "accountId": account_id,
        "user": user_data,
        "headerConfig": header_config,
        "dataConfig": data_config,
        "users": users,
    }
