from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, Float, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import config

Base = declarative_base()  

class Beer(Base):
	"""Create a data model for the database to be set up for capturing songs """
	__tablename__ = 'beer'
	beer_beerid = Column(Integer, primary_key=True)
	beer_name = Column(String(200), unique=False, nullable=False)
	beer_abv = Column(Float, unique=False, nullable=True)
	beer_style = Column(String(200), unique=False, nullable=False)
	brewery_name = Column(String(200), unique=False, nullable=True)
	review_profilename = Column(String(200), unique=False, nullable=False)
	mean_review = Column(Float, unique=False, nullable=False)
	beer_category = Column(String(200), unique=False, nullable=False)
  	  
	def __repr__(self):
		return '<Beer %r>' % self.beer_name

def create_db(rds=False):
	"""Creates database with Beers table and one row.
	
	Keyword Arguments:
		rds {bool} -- If true, creates databased in RDS. If false, creates locally in sqlite (default: {False})
	"""
	if rds = True:
		engine_string = "{}://{}:{}@{}:{}/msia423".\
	format(config.MYSQL_SQLTYPE, config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_HOST, config.MYSQL_PORT)
	else:
		engine_string = config.SQLITELOCALENGINE
	engine = sql.create_engine(engine_string)
	Base.metadata.create_all(engine)
	logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
	logger = logging.getLogger(__file__)
	# create a db session
	Session = sessionmaker(bind=engine)  
	session = Session()
	# add a record/track
	beer1 = Beer(beer_name = 'Black Horse Black Beer', beer_abv = 6.5, beer_style = "Foreign / Export Stout", 	brewery_name = "Vecchio Birraio", review_profilename = "stcules", mean_review = "2.9", beer_category = "Stout") 
	session.add(beer1)
	session.commit()   
	logger.info("Database created with beer added: Black Horse Black Beer")
	session.close()
	
if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Create and/or add data to database")
	parser.add_argument('--rds', default=False, help='path to yaml file with configurations')
	args = parser.parse_args()
	if args.rds:
		create_db(rds=True)
	else:
		create_db(rds=False)
		
	
	