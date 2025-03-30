from pydantic_settings import BaseSettings, SettingsConfigDict
import stripe


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    STRIPE_SECRET_KEY: str  # Ensure this key is explicitly defined

    model_config = SettingsConfigDict(env_file=".env")  # Load environment variables


# Load settings from .env
settings = Settings()

# Configure Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# Check if the Stripe key is properly set
if not settings.STRIPE_SECRET_KEY:
    raise ValueError("STRIPE_SECRET_KEY is missing")
