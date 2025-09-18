from pydantic_settings import SettingsConfigDict, BaseSettings

class TestSettings(BaseSettings):

    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env.test")

settings = TestSettings() #type: ignore
