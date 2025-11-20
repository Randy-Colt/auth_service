from datetime import datetime
from uuid import uuid4
from sqlalchemy import func, TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class User(Base):
    id: Mapped[uuid4] = mapped_column(UUID, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    login:  Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    project_id: Mapped[uuid4] = mapped_column(UUID)
    env: Mapped[str]
    domain: Mapped[str]
    locktime: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
