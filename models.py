from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base

class Repository(Base):

    __tablename__ = "repositories"

    id = Column(Integer,
                primary_key=True,
                index=True)

    owner = Column(String)

    repo_name = Column(String)

    stars = Column(Integer)

    forks = Column(Integer)

    open_issues = Column(Integer)

    language = Column(String)