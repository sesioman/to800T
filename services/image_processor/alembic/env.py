import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from app.config import Config
from app.database import Base
from app.models.images import Image
from alembic import context

config = context.config
config.set_main_option(name="sqlalchemy.url", value=Config.DATABASE_URL)
target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_async_engine(
        Config.DATABASE_URL,  # Directly use the database URL for async connection
        poolclass=NullPool,  # Use NullPool for async connections
        future=True,
    )

    try:
        # Establish the connection and run migrations
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    except Exception as e:
        print(f"Error during migration: {e}")
        raise  # Re-raise the exception for further handling if necessary
    finally:
        await connectable.dispose()  # Ensure resources are cleaned up

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
