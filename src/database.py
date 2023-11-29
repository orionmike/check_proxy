import asyncio
from sqlalchemy import create_engine, delete

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DB_FILE


async_engine = create_async_engine(f"sqlite+aiosqlite:///{DB_FILE}")
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(f"sqlite:///{DB_FILE}")
sync_session_maker = sessionmaker(sync_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def recreate_all_table(engine) -> None:
    sync_engine.echo = False
    try:
        Base.metadata.drop_all(engine)
    except:
        pass
    Base.metadata.create_all(engine)
    sync_engine.echo = True


if __name__ == '__main__':
    print(DB_FILE)
    Base.metadata.create_all(sync_engine)
