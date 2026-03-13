import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "creatorchain")
POSTGRES_USER = os.getenv("POSTGRES_USER", "creatorchain")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "creatorchain")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))

INITIA_RPC_URL = os.getenv("INITIA_RPC_URL", "http://localhost:26657")
INITIA_CHAIN_ID = os.getenv("INITIA_CHAIN_ID", "creatorchain-1")

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")

DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
