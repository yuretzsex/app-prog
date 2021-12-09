from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app_prog.models import User, Announcement, Local, Public

some_engine = create_engine('mysql://root:12345@localhost/aplabs')

Session = sessionmaker(bind=some_engine)

session = Session()
