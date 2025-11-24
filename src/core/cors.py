from fastapi.middleware.cors import CORSMiddleware
import os

def setup_cors(app):
    # Configure CORS origins via environment variable CORS_ORIGINS (comma-separated).
    # Default: allow localhost frontends and allow all in development if CORS_ORIGINS="*".
    _origins_env = os.environ.get("CORS_ORIGINS", "*")
    if _origins_env.strip() == "*":
        _allow_origins = ["*"]
        # Browsers won't accept wildcard origin together with credentials.
        _allow_credentials = False
    else:
        _allow_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]
        _allow_credentials = True

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allow_origins,
        allow_credentials=_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )
