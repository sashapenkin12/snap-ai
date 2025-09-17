"""
App config module.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    Settings class for environment variables.

    Attributes:
        DB_USER: Database user's name.
        DB_PASSWORD: Database user's password.
        DB_HOST: Address of the database.
        DB_NAME: Name of the database.

        ACCESS_TOKEN_EXPIRE_MINUTES: How long JWT access tokens will be valid.
        REFRESH_TOKEN_EXPIRE_DAYS: How long JWT refresh tokens will be valid.
    """
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def DATABASE_URL(self) -> str:
        return 'postgresql+asyncpg://{username}:{password}@{host}/{name}'.format(
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            name=self.DB_NAME,
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = AppSettings() #type: ignore
