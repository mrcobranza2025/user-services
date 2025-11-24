"""Create Firestore client after Firebase has been initialized.

Importing `src.core.firebase` ensures initialization runs before we call
`firestore.client()` which would otherwise raise "The default Firebase app does not exist".
"""
from firebase_admin import firestore


def get_db():
    """Return a Firestore client.

    The client is created lazily so importing modules doesn't fail if
    Firebase wasn't initialized yet (for example: missing credentials).
    """
    try:
        return firestore.client()
    except Exception as exc:
        # Surface a clearer error to the developer at runtime.
        raise RuntimeError(
            "Failed to create Firestore client. Make sure Firebase is initialized "
            "(set GOOGLE_APPLICATION_CREDENTIALS or provide a valid service account JSON)."
        ) from exc
