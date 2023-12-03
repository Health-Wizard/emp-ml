from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.config import env_config

url = URL.create(
    drivername=env_config.DRIVERNAME,
    username=env_config.USERNAME,
    password=env_config.PASSWORD,
    host=env_config.HOST,
    database=env_config.DATABASE,
    port=env_config.PORT
)

engine = create_engine(url)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)