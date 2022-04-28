from sqlalchemy.sql.expression import text
import databases
import sqlalchemy

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://" \
                          f"{settings.database_username}:" \
                          f"{settings.database_password}@" \
                          f"{settings.database_hostname}:" \
                          f"{settings.database_port}/" \
                          f"{settings.database_name}"

database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URL)

payments = sqlalchemy.Table(
    "payments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, server_default=text("gen_random_uuid()"), primary_key=True),
    sqlalchemy.Column("type", sqlalchemy.String),
    sqlalchemy.Column("response_cielo", sqlalchemy.JSON),
)

metadata.create_all(engine)
