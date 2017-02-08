from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String, Column, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///MerchManager.db', echo=True)
Session = sessionmaker(bind=engine)


# Table 1: merch: merch name, price (eg. Record, 19.99)
class Merch(Base):

    __tablename__ = 'merch'

    item = Column(String, primary_key=True)
    price = Column(Float)

    def __repr__(self):
        return 'Item: {} Price: ${}'.format(self.item, self.price)


# Table 2: shows: show id, date, venue(eg. 01, 12/12/12, Disco Lounge)
class Shows(Base):

    __tablename__ = 'shows'

    show_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    venue = Column(String)

    def __repr__(self):
        return 'Show id: {} Date: {} Venue: {}'.format(self.show_id, self.date, self.venue)


# Table 3: sales: show id, merch name, num sold (eg. 01, Record, 5.0, 10)
class Sales(Base):

    __tablename__ = 'sales'

    show_id = Column(Integer, ForeignKey('shows.show_id'), primary_key=True)
    item = Column(String, ForeignKey('merch.item'), primary_key=True)
    price = Column(Float, ForeignKey('merch.price'))
    sold = Column(Integer)

    def __repr__(self):
        return 'Show id: {} Item: {} Price: {} Sold: {}'.format(self.show_id, self.item, self.price, self.sold)


# Create each of the tables
Base.metadata.create_all(engine)


# Checks to see whether or not any sample data has already been created, returns true or false
# (Can't be added to db.py because python isn't happy with circular dependencies)
def check_sample_present():
    check_session = Session()
    num_items = check_session.query(Merch).count()
    check_session.close()
    if num_items > 0:
        return True
    else:
        return False


# Create sample data if not already present
if not check_sample_present():
    merch1 = Merch(item='Vinyl', price=20.0)
    merch2 = Merch(item='CD', price=15.0)
    merch3 = Merch(item='T-Shirt', price=25.0)

    show1 = Shows(date='April 13 2015', venue='Disco Lounge')
    show2 = Shows(date='April 15 2015', venue='Arcade')
    show3 = Shows(date='April 17 2015', venue='Bowling Alley')

    sale1 = Sales(show_id=1, item='Vinyl', price=20.0, sold=10)
    sale2 = Sales(show_id=1, item='CD', price=15.0, sold=5)
    sale3 = Sales(show_id=2, item='Vinyl', price=20.0, sold=15)

    save_samples = Session()
    save_samples.add_all([merch1, merch2, merch3, show1, show2, show3, sale1, sale2, sale3])
    save_samples.commit()
    save_samples.close()
