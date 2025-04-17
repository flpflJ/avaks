from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.config import settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        # Создаём асинхронный движок
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Создаём фабрику сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
            class_=AsyncSession
        )

    # Просто async-функция без декораторов
    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)
