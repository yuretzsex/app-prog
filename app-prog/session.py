from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Announcement, Local, Public

some_engine = create_engine('mysql://root:12345@localhost/aplabs')

Session = sessionmaker(bind=some_engine)

session = Session()

user = User(username="brawlstars",
             firstName="Leon",
             lastName="Vypav",
             password="doradura",
             email="bestbrawler2008@ukr.net",
             phone="+38028813372",
             city="Netishyn")

an1 = Announcement(tittle="Looking for a new foe",
                   content="I'm ready to brawl",
                   authorid=1)

an2 = Announcement(tittle="Dora",
                   content="Who wants to visit a new concert with me?",
                   authorid=1)

local1 = Local(announcementid=1)

public1 = Public(announcementid=2)

session.add(user)
session.add(an1)
session.add(an2)
session.add(local1)
session.add(public1)
session.commit()
