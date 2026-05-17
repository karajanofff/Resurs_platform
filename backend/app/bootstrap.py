from sqlalchemy.orm import Session

from .models import User
from .security import hash_password
from .settings import settings


def ensure_bootstrap_admin(db: Session) -> None:
    if db.query(User).count():
        return

    if not all(
        [
            settings.bootstrap_admin_name,
            settings.bootstrap_admin_email,
            settings.bootstrap_admin_password,
        ]
    ):
        return

    db.add(
        User(
            full_name=settings.bootstrap_admin_name,
            email=settings.bootstrap_admin_email,
            password_hash=hash_password(settings.bootstrap_admin_password),
            role="admin",
        )
    )
    db.commit()
