from sqlalchemy.orm import Session

from .models import User
from .security import hash_password
from .settings import settings


def ensure_bootstrap_admin(db: Session) -> None:
    defaults = [
        (
            settings.bootstrap_admin_name or "Administrator",
            settings.bootstrap_admin_email or "admin@example.com",
            settings.bootstrap_admin_password or "admin123",
            "admin",
        ),
        ("O'qituvchi", "teacher@example.com", "teacher123", "teacher"),
    ]

    for full_name, email, password, role in defaults:
        user = db.query(User).filter(User.email == email).first()
        if user:
            user.full_name = full_name
            user.role = role
            user.password_hash = hash_password(password)
            continue
        db.add(
            User(
                full_name=full_name,
                email=email,
                password_hash=hash_password(password),
                role=role,
            )
        )
    db.commit()
