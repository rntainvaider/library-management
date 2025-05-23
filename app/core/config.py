from dotenv import load_dotenv
import os

_ = load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
localhost = os.getenv("localhost")
port = os.getenv("port")
dbname = os.getenv("dbname")

DATABASE_URL = (
    f"postgresql+psycopg2://{username}:{password}@{localhost}:{port}/{dbname}"
)
