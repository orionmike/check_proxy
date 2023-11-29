from datetime import datetime
from typing import Annotated
from database import Base, sync_engine, async_engine
from sqlalchemy.orm import Mapped, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]


class Proxy(Base):
    __tablename__ = "proxy"

    id: Mapped[intpk]
    url: Mapped[str]
    count_trying: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(nullable=True)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)


if __name__ == '__main__':
    Base.metadata.create_all(sync_engine)
