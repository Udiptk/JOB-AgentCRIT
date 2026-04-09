from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import all models here so Alembic can discover them
from app.models.user import User  # noqa
from app.models.resume import Resume  # noqa
from app.models.job import Job  # noqa
from app.models.application import Application  # noqa
from app.models.notification import Notification  # noqa
