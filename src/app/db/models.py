import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, DateTime, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class User(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.timezone('UTC+3', func.now())
    )
    login:  Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    project_id: Mapped[uuid.UUID] = mapped_column(Uuid)
    env: Mapped[str]
    domain: Mapped[str]
    locktime: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
