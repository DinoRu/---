from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class HashPassword:

	@classmethod
	def create_hash(cls, password: str):
		return pwd_context.hash(password)

	@classmethod
	def verify_hash(cls, plain_text: str, hashed_password: str):
		return pwd_context.verify(plain_text, hashed_password)