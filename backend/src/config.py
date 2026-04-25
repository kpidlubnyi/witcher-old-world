from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str = "development"
    
    OAUTH_GOOGLE_CLIENT_SECRET: str
    OAUTH_GOOGLE_CLIENT_ID: str
    OAUTH_GOOGLE_REDIRECT_URI: str
    
    DATABASE_URL: str
    JWT_SECRET: str
    
    @property
    def IS_PRODUCTION(self) -> bool:
        return self.MODE == "production"
    
    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings()