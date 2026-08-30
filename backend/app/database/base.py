"""Database base configuration with async SQLAlchemy."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    """Dependency to get async DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()



async def create_tables():
    """Create all tables and apply additive SQLite columns for existing databases."""
    async with engine.begin() as conn:
        import app.models  # noqa — registers all models with Base.metadata
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_ensure_additive_columns)


def _ensure_additive_columns(sync_conn) -> None:
    """Add new columns on existing SQLite databases without dropping data."""
    dialect = sync_conn.dialect.name
    if dialect != "sqlite":
        return

    additions = {
        "learner_profiles": [
            ("bio", "TEXT"),
            ("profile_image", "TEXT"),
        ],
        "projects": [
            ("domain", "VARCHAR(100)"),
            ("problem_statement", "TEXT"),
            ("business_value", "TEXT"),
            ("resume_value", "VARCHAR(20)"),
            ("technologies", "JSON"),
            ("architecture", "TEXT"),
            ("resume_bullet", "TEXT"),
        ],
    }

    for table, columns in additions.items():
        existing = {
            row[1]
            for row in sync_conn.exec_driver_sql(f"PRAGMA table_info({table})").fetchall()
        }
        if not existing:
            continue
        for name, col_type in columns:
            if name not in existing:
                sync_conn.exec_driver_sql(f"ALTER TABLE {table} ADD COLUMN {name} {col_type}")

