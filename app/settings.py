from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(dotenv_path="../")

class Settings(BaseSettings):
	database_url: str
	secret_key: str
	algorithm: str

	class Config:
		env_file = "../.env"
