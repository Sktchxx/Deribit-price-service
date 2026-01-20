from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    tickers: list[str] = Field(default_factory=lambda: ['btc_usd', 'eth_usd'])
    deribit_url: str = 'https://www.deribit.com/api/v2/public/get_index_price'

    postgres_user: str = 'user'
    postgres_password: str = 'pass'
    postgres_db: str = 'prices'
    postgres_host: str = 'db'
    postgres_port: int = 5432

    redis_host: str = 'redis'
    redis_port: int = 6379

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='',
        case_sensitive=False
    )


settings = Settings()


DATABASE_ASYNC_URL = (
    f"postgresql+asyncpg://{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)

DATABASE_SYNC_URL = (
    f"postgresql+psycopg2://{settings.postgres_user}:"
    f"{settings.postgres_password}@"
    f"{settings.postgres_host}:"
    f"{settings.postgres_port}/"
    f"{settings.postgres_db}"
)
