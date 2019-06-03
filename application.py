from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from src.configure_db import Top_Ten_Beers, User_Combinations, User_Predictions
import pandas as pd
import traceback
import logging

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
# Initialize the Flask application
app = Flask(__name__)
# Configure flask app from flask_config.py
app.config.from_pyfile('flask_config.py')

db = SQLAlchemy(app)

beertype = ''

def query_to_list(rset):
    """Converts SQLAlchemy query to list"""
    result = []
    for obj in rset:
        instance = inspect(obj)
        items = instance.attrs.items()
        result.append([x.value for _,x in items])
    return instance.attrs.keys(), result

@app.route('/')
def intro_page():
    """Main view that introduces users to app and prompts them to choose a broad beer type. Uses beerapp/templates/first.html template.
    Returns: rendered html template
    """
    logger.info('At introductory app page.')
    return render_template('first.html')

@app.route('/recommender', methods=['POST'])
def add_entry():
    """View that process a POST with beer type input and displays top ten beers for this type, queried from DB.
    Returns: rendered beerapp/templates/recommender.html template
    """
    global beertype 
    beertype = request.form['beertype']
    try:
        listbeers = db.session.query(Top_Ten_Beers).filter_by(Type=beertype)
        logger.debug("Top ten beers query accessed")
        return render_template('recommender.html', beertype=beertype, listbeers=listbeers)
    except:
        traceback.print_exc()
        logger.warning("Not able to display beers, error page returned")
        return render_template('error-noselection.html')

@app.route('/results', methods=['POST'])
def get_results():
    """View that process a POST with beer choice input and displays recommendations, queried from DB.
    Returns: rendered beerapp/templates/results.html template
    """
    try:
        firstbeer = int(request.form['beerchoice1'])
        secondbeer = int(request.form['beerchoice2'])
    except:
        traceback.print_exc()
        logger.warning("Not able to display recommendations, error page returned")
        return render_template('error-noselection.html')
    try:
        listbeers = db.session.query(Top_Ten_Beers).filter_by(Type=beertype)
        logger.debug("Top Ten Beers Query Accessed")
    except:
        traceback.print_exc()
        logger.warning("Not able to display recommendations, error page returned")
    if firstbeer==secondbeer:
        return render_template('error-samebeers.html')
    names, data = query_to_list(listbeers)
    top10df = pd.DataFrame.from_records(data, columns=names)
    usercomb = top10df.iloc[[firstbeer, secondbeer],:]
    try:
        allcomb = db.session.query(User_Combinations).filter_by(Type=beertype)
        logger.debug("Recommendation Query Accessed")
    except:
        traceback.print_exc()
        logger.warning("Not able to display recommendations, error page returned")
    names, data = query_to_list(allcomb)
    allcombdf = pd.DataFrame.from_records(data, columns=names)
    probablerows = allcombdf[allcombdf['Beer_ID'].isin(usercomb['Beer_ID'].values)]
    realrows = probablerows.groupby(['ID']).count()
    ID = realrows[realrows['Beer_ID']==2].index[0]
    try:
        preds = db.session.query(User_Predictions).filter_by(Type=beertype, ID=ID)
        logger.debug("Recommendation Results Query Accessed")
        return render_template('results.html', beertype=beertype, preds=preds)
    except:
        traceback.print_exc()
        logger.warning("Not able to display beers, error page returned")
        return render_template('error-noselection.html')

if __name__ == "__main__":

    app.run(host = '0.0.0.0', use_reloader=True, port=3000)
