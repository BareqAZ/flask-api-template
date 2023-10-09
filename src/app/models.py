# Python imports
import hashlib
import uuid

# Local imports
from app import db


class Base(db.Model):
    __abstract__ = True

    id = db.Column(
        db.String(36), unique=True, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )


class User(Base):
    __tablename__ = "users"

    first_name = db.Column(db.String, nullable=True, unique=False)
    last_name = db.Column(db.String, nullable=True, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    api_key = db.Column(db.String(), unique=True)
    hashed_api_key = db.Column(db.String(150), nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # When a User is created, if no API key is given
        # Generate and hash a new API Key
        if not self.hashed_api_key:
            new_api_key = str(uuid.uuid4())
            self.hashed_api_key = hashlib.sha256(
                new_api_key.encode("utf-8")
            ).hexdigest()
