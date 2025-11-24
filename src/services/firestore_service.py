from google.cloud import firestore

class FirestoreService:
    def __init__(self):
        self.db = firestore.Client()

    def get_all(self, collection: str):
        docs = self.db.collection(collection).stream()
        return [{"id": d.id, **d.to_dict()} for d in docs]
