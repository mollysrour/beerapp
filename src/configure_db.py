from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, Float, MetaData
import sqlalchemy as sql
import logging
import sys
import pandas as pd
import argparse
import yaml
import sqlite3
Base = declarative_base()  

class Top_Ten_Beers(Base):
    """Schema for Top Ten Beers Table """
    __tablename__ = 'top_ten_beers'
    Pkey = Column(Integer, primary_key=True)
    Beer_ID = Column(Integer, unique=False, nullable=False)
    Beer_Name = Column(String(200), unique=False, nullable=False)
    ABV = Column(Float, unique=False, nullable=True)
    Type = Column(String(200), unique=False, nullable=False)
    Style = Column(String(200), unique=False, nullable=False)
    Brewery = Column(String(200), unique=False, nullable=True)
  
    def __repr__(self):
	    top_ten_beers_repr = "<Top_Ten_Beers(Beer_ID='%d', Beer_Name='%s', ABV='%f', Type='%s', Style='%s', Brewery='%s')>"
	    return top_ten_beers_repr %(self.Beer_ID, self.Beer_Name, self.ABV, self.Type, self.Style, self.Brewery)

class User_Combinations(Base):
    """Schema for User Combinations Table """
    __tablename__ = 'user_combinations'
    Pkey = Column(Integer, primary_key=True)
    Beer_ID = Column(Integer, unique=False, nullable=False)
    Beer_Name = Column(String(200), unique=False, nullable=False)
    ABV = Column(Float, unique=False, nullable=True)
    Type = Column(String(200), unique=False, nullable=False)
    Style = Column(String(200), unique=False, nullable=False)
    Brewery = Column(String(200), unique=False, nullable=True)
    ID = Column(String(200), unique=False, nullable=False)

    def __repr__(self):
        user_combinations_repr = "<User_Combinations(Beer_ID='%d', Beer_Name='%s', ABV='%f', Type='%s', Style='%s', Brewery='%s', ID='%s')>"
        return user_combinations_repr %(self.Beer_ID, self.Beer_Name, self.ABV, self.Type, self.Style, self.Brewery, self.ID)

class User_Predictions(Base):
	"""Schema for User Predictions Table"""
	__tablename__ = 'user_predictions'
	Pkey = Column(Integer, primary_key=True)
	Beer_ID = Column(Integer, unique=False, nullable=False)
	score = Column(Float, unique=False, nullable=False)
	Beer_Name = Column(String(200), unique=False, nullable=False)
	ABV = Column(Float, unique=False, nullable=True)
	Type = Column(String(200), unique=False, nullable=False)
	Style = Column(String(200), unique=False, nullable=False)
	Brewery = Column(String(200), unique=False, nullable=True)
	ID = Column(String(200), unique=False, nullable=False)
	def __repr__(self):
		user_predictions_repr = "<User_Predictions(Beer_ID='%d', score = '%f', Beer_Name='%s', ABV='%f', Type='%s', Style='%s', Brewery='%s', ID='%s')>"
		return user_predictions_repr %(self.Beer_ID, self.score, self.Beer_Name, self.ABV, self.Type, self.Style, self.Brewery, self.ID)

def create_connection(rds=False, MYSQL_HOST='', MYSQL_DB="", MYSQL_SQLTYPE="mysql+pymysql", MYSQL_PORT=3306,
                      MYSQL_USER="", MYSQL_PASSWORD="", SQLITELOCALENGINE="sqlite:///../data/beers.db"):
	"""Creates RDS/SQlite connection.
	
	Keyword Arguments:
		rds {bool} -- If true, creates databased in RDS. If false, creates locally in sqlite (default: {False})
	"""
	if rds == True:
		engine_string = "{}://{}:{}@{}:{}/msia423".\
	format(MYSQL_SQLTYPE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT)
	else:
		engine_string = SQLITELOCALENGINE
	engine = sql.create_engine(engine_string)
	return engine

def create_db(rds=False, MYSQL_HOST='127.0.0.1', MYSQL_DB="", MYSQL_SQLTYPE="", MYSQL_PORT=10000,
                      MYSQL_USER="", MYSQL_PASSWORD="", SQLITELOCALENGINE=""):
    """Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    engine = create_connection(rds, MYSQL_HOST, MYSQL_DB, MYSQL_SQLTYPE, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, SQLITELOCALENGINE)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    """ Creates SqLalchemy session

    Arguments:
        engine_string --SQLAlchemy connection string in the form of: "{sqltype}://{username}:{password}@{host}:{port}/{database}"

    Returns:
        SQLAlchemy session
    """
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def persist_top10beers(session, records):
    """Adds score records to tweet_score table in SQL database
    
    Arguments:
        session {[session]} -- SQL database session
        records {[type]} -- list of dictionaries containing tweetid and score
    """
    numrec = 0 #keeps track of number of records added to db
    for index, i in records.iterrows():
        beer = Top_Ten_Beers(Beer_ID=i['Beer_ID'], Beer_Name=i['Beer_Name'], ABV=i['ABV'], Type=i['Type'], Style=i['Style'], Brewery=i['Brewery']) 
        session.add(beer) #add record
        numrec = numrec + 1 #keeps track of number of records added to db
    logger.info("Added {} records to SQL database".format(numrec))

def persist_usercombinations(session, records):
    """Adds score records to tweet_score table in SQL database
    
    Arguments:
        session {[session]} -- SQL database session
        records {[type]} -- list of dictionaries containing tweetid and score
    """
    numrec = 0 #keeps track of number of records added to db
    for index, i in records.iterrows():
        beer = User_Combinations(Beer_ID=i['Beer_ID'], Beer_Name=i['Beer_Name'], ABV=i['ABV'], Type=i['Type'], Style=i['Style'], Brewery=i['Brewery'], ID=i['ID']) 
        session.add(beer) #add record
        numrec = numrec + 1 #keeps track of number of records added to db
    logger.info("Added {} records to SQL database".format(numrec))

def persist_userpredictions(session, records):
    """Adds score records to tweet_score table in SQL database
    
    Arguments:
        session {[session]} -- SQL database session
        records {[type]} -- list of dictionaries containing tweetid and score
    """
    numrec = 0 #keeps track of number of records added to db
    for index, i in records.iterrows():
        beer = User_Predictions(Beer_ID=i['Beer_ID'], score=i['score'], Beer_Name=i['Beer_Name'], ABV=i['ABV'], Type=i['Type'], Style=i['Style'], Brewery=i['Brewery'], ID=i['ID']) 
        session.add(beer) #add record
        numrec = numrec + 1 #keeps track of number of records added to db
    logger.info("Added {} records to SQL database".format(numrec))


def configure(args):
    """Runs script to run scoring
    
    Arguments:
        args {argparse.Namespace} -- Script arguments
    
    Raises:
        ValueError: "Path to yaml config file must be provided through --config" if args.config not specified
        ValueError: "Path to CSV for input preds data must be provided through --input_preds" if args.input_preds not specified
        ValueError: "Path to CSV for input top10 data must be provided through --input_top10rows" if args.input_top10rows not specified
        ValueError: "Path to CSV for input combinations data must be provided through --input_combinations" if args.input_combinations not specified
    """
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['configure_db']
    else:
        raise ValueError("Path to yaml config file must be provided through --config")
    if args.rds:
        engine = create_db(rds=True, **config['rds'])
    else:
        engine = create_db(rds=False, **config['sqlite'])
    session = get_session(engine)

    if args.input_preds is not None:
        pred_data = pd.read_csv(args.input_preds)
    else:
        raise ValueError("Path to CSV for input preds must be provided through --input_preds")
        pred_data = pred_data.fillna(value=0)
        try:
            persist_userpredictions(session, pred_data)
            session.commit()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        finally:
            logger.info("Persisted {} prediction records.".format(len(pred_data.index)))
    
    if args.input_top10rows is not None:
        top10_data = pd.read_csv(args.input_top10rows)
    else:
        raise ValueError("Path to CSV for input top10 data must be provided through --input_top10rows")
        top10_data = top10_data.fillna(value=0)
        print(top10_data)
        try:
            persist_top10beers(session, top10_data)
            session.commit()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        finally:
            logger.info("Persisted {} top10beers records.".format(len(top10_data.index)))
    
    if args.input_combinations is not None:
        combinations_data = pd.read_csv(args.input_combinations)
    else:
        raise ValueError("Path to CSV for input combination data must be provided through --input_combinations")
        combinations_data = combinations_data.fillna(value=0)
        try:
            persist_usercombinations(session, combinations_data)
            session.commit()
        except Exception as e:
            logger.error(e)
            sys.exit(1)
        finally:
            logger.info("Persisted {} combination records.".format(len(combinations_data.index)))
            session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    parser.add_argument('--rds', default=False, help='path to yaml file with configurations')
    parser.add_argument('--input_preds', default='../data/preds.csv', help='config.yml')
    parser.add_argument('--input_top10rows', default='../data/top10.csv', help='config.yml')
    parser.add_argument('--input_combinations', default='../data/combinations.csv', help='config.yml')
    args = parser.parse_args()
    
    configure(args)

    