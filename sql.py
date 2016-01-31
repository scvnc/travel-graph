from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()



Base = declarative_base()


class Route(Base):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True)
    source = Column(String)
    dest = Column(String)
    depart = Column(DateTime)
    arrive = Column(DateTime)
    fare = Column(Integer)
    carrier = Column(String)
    
    def __repr__ (self):
      return "{2} ({0} -> {1}) ${3}".format(self.source, self.dest, self.depart, self.fare)
    
Base.metadata.create_all(engine)

