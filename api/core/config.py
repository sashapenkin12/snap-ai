"""
App config module.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    """
    Settings class for environment variables.

    Attributes:

    """
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str

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
