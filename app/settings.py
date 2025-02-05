from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(dotenv_path="../")

class Settings(BaseSettings):
	env: str = 'local'
	database_url: str
	postgres_user: str
	postgres_db: str
	postgres_password: str
	postgres_port: int
	postgres_host: str
	db_url: str
	app_env: str
	app_debug: str
	secret_key: str
	algorithm: str
	model_config = SettingsConfigDict(env_file=".env", extra='ignore')

	def active_database_url(self):
		return self.db_url if self.env == 'docker' else self.database_url

Config = Settings()



