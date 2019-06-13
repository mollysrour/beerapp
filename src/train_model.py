from surprise import Dataset, Reader, KNNBasic
from collections import defaultdict
from itertools import combinations
import pandas as pd
import argparse
import logging
import yaml

def filter_data(df, value, col):
    """Given a data frame, column name, and value, outputs filtered data frame with rows that have that column value.

    Arguments:
    df {pd.DataFrame} -- Pandas DataFrame
    value {str} -- Name of specific value of column to filter on
    col {str} -- Name of column to filter on

    Returns:
    onetypedf {pd.DataFrame} -- Filtered DataFrame
    """
    try:
        onetypedf = df[df[col]==value] #Filtered by column value
    except:
        raise KeyError('Column name is incorrect.')
        logger.error('Please re-enter column name.')
    onetypedf = onetypedf.reset_index(drop=True) #remove old dataframe indices
    return onetypedf

def get_unique_items(df, col):
    """Given a dataframe and column name or list of column names, outputs unique items or rows. If given a column name,
    outputs a list of unique items in that column. If given a list of column names, outputs unique combinations of those columns.
    
    Arguments:
        df {pd.DataFrame} -- Pandas DataFrame
        col {str or list} -- Specified column name or list of column names
    
    Returns:
        itemlist {list or pd.DataFrame} -- List of unique items in col or unique combinations of columns
    """
    if type(col) == str: #if only one column given
        try:
            itemlist = list(df[col].drop_duplicates()) #unique items in given column
        except:
            raise KeyError('Column name is incorrect.')
            logger.error('Please re-enter column name.')
    else: #if multiple columns given
        try:
            itemlist = df[col].drop_duplicates() #unique combinations of given columns
        except:
            raise KeyError('Column names are incorrect.')
            logger.error('Please re-enter column names.')
    return itemlist

def top_n_popular(df, colnames, idcolname='Beer_ID', reviewcolname='Mean_Review', n=10):
    """Returns the top n most popular items in a dataset

    Args:
        df {pd.DataFrame} -- Full dataframe 
        colnames {list} -- list of column names needed to in the topdf
        idcolname {str} -- column name for item id (default: {'Beer_ID'})
        reviewcolname {str} -- column name for reviews (default: {'Mean_Review'})
        n {int} -- number of most popular items to return
    Returns:
        topdf {pd.DataFrame} -- DF showing the rows corresponding to the top n items, with review and profile name dropped.
    """
    try:
        df_groupedbyID = df.groupby([idcolname]).mean() #df grouped by item id, averaging reviews
    except:
        raise KeyError('Incorrect ID column name')
        logger.error('Please re-enter ID column name.')
    try:
        df_groupedbyID = df_groupedbyID.sort_values(reviewcolname, ascending=False) #sort df by review, descending
    except:
        raise KeyError('Incorrect review column name')
        logger.error('Please re-enter review column name.')
    top = df_groupedbyID.index[0:n].values.tolist() #find index of top n items
    rank_index = pd.DataFrame(top) #store rank
    rank_index.columns = ['Beer_ID'] #store rank
    try:
        topdf = get_unique_items(df[df[idcolname].isin(top)], colnames) #df containing the top n items, unordered
    except:
        raise KeyError('Column names are incorrect.')
        logger.error('Please re-enter column names.')
    rank_index = pd.DataFrame(top)
    rank_index.columns = ['Beer_ID']
    finaldf = pd.merge(rank_index, topdf, on='Beer_ID')
    return finaldf


def create_combinations(df, typename, n=2):
    """Creates dataframe of all possible row combinations of n rows, given a dataframe. 
    Also creates column 'ID' with value typename with index appended.

    Args:
        df {pd.DataFrame} -- Full dataframe
        typename {str} -- specified value that will be created as ID col (with index appended)
        n {int} -- number of rows in each combination. (default: {2})

    Returns:
        combdf {pd.DataFrame} -- DF of all possible row combinations of n rows with ID column added. Total number of rows will be
                                nrow(df) choose n.
    """
    combolist = []
    index = 1
    try:
        list(combinations(df.index,n))
    except:
        raise ValueError('N must be an integer.')
        logger.error('Re enter n for combinations.')
    for i in list(combinations(df.index,n)): #all possible combinations of n rows
        minidf = df.loc[i,:] #specific combination
        minidf['ID'] = typename + str(index) #ID column value
        combolist.append(minidf)
        index=index+1
    combodf = pd.concat(combolist, ignore_index=True) #all combinations
    return combodf
 
def create_user_rows(user_choices, user_id, idlist, reviewcolname='Mean_Review', idcolname='Beer_ID', usercolname='Reviewer'):
    """Creates new dataframe containing rows for a new user who is interested in items in user_choices
    
    Arguments:
        user_choices {list} -- List of item IDs chosen by the user
        user_id {str} -- User name provided by user
        idlist {list} -- List of unique items in dataset
        reviewcolname {str} -- column name for reviews (default: {'Mean_Review'})
        idcolname {str} -- column name for item ID (default: {'Beer_ID'})
        usercolname {str} -- column name for users (default: {'Reviewer'})
    
    Returns:
        user_rows {pd.DataFrame} -- dataframe containing rows for a new user who is interested in items in user_choices
    """
    user_rows = pd.DataFrame({usercolname: user_id, idcolname: idlist, reviewcolname: 0}) #create dataframe for user
    choiceitems = user_rows[idcolname].isin(user_choices) #finds user choices within df
    if not any(choiceitems):
        raise ValueError('User choices are not in dataset.')
        logger.error('Re-enter user choices.')
    user_rows.loc[choiceitems, reviewcolname] = 5 #sets user choice review to 5 for user
    return user_rows

def user_rows_combination_df(combdf, idlist, reviewcolname='Mean_Review', idcolname='Beer_ID', usercolname='Reviewer', n=2):
    """
    Arguments:
        combdf {pd.DataFrame} -- DF of all possible row combinations of n rows with ID column added (output of create_combinations)
        idlist {list} -- List of unique items in dataset
        reviewcolname {str} -- column name for reviews (default: {'Mean_Review'})
        idcolname {str} -- column name for item ID (default: {'Beer_ID'})
        usercolname {str} -- column name for users (default: {'Reviewer'})
    
    Returns:
        final_user_rows {pd.DataFrame} -- dataframe containing rows for users in combdf 
        user_idlist -- list of users
    """
    thelist = []
    index = 1
    for i in list(range(0, len(combdf.index), n)): #iterating through combinations
        j=i+1
        pair = combdf.loc[i:j,] #specific pair
        user_id = pair['ID'][i]
        user_rows = create_user_rows(pair[idcolname], user_id, idlist, reviewcolname, idcolname, usercolname)
        thelist.append(user_rows) #created user rows
        index=index+1
    final_user_rows = pd.concat(thelist, ignore_index=True)
    user_idlist = get_unique_items(final_user_rows, usercolname)
    return final_user_rows, user_idlist

def build_trainset(df, user_rows=None, colnames=None):
    """Create a training set for a collaborative filtering algorithm using scikit surprise
    
    Arguments:
        df {pd.DataFrame} -- dataframe
        user_rows {pd.DataFrame} -- Dataframe rows for new users with ratings for chosen items (default: {None})
        colnames {list} -- list of column names for userID, itemID, review, in that order. (default: {None})
        rating_scale {tuple} -- range of rating scale

    Returns:
        trainset {surprise.trainset.Trainset} -- training data in the Surprise package format
    """
    if colnames is not None:
        train = df[colnames]
    else:
        train = df
    reader = Reader(line_format='user item rating')
    if user_rows is not None:
        trainset_load = Dataset.load_from_df(pd.concat([train, user_rows]), reader) #dataset plus user rows
    else:
        trainset_load = Dataset.load_from_df(train, reader)
    trainset = trainset_load.build_full_trainset() #build trainset
    return trainset

def build_testset(df, reviewcolname='Mean_Review', idcolname='Beer_ID', usercolname='Reviewer'):
    """Builds test set for a collaborative filtering algorithm using scikit Surprise when given test rows

    Arguments: 
        df {pd.DataFrame} -- Pandas Data Frame
        reviewcolname {str} -- column name for reviews (default: {'Mean_Review'})
        idcolname {str} -- column name for item ID (default: {'Beer_ID'})
        usercolname {str} -- column name for users (default: {'Reviewer'})

    Returns:
        testset {list} -- list in test format that Surprise requires
    """
    testset = [(uid, iid, r) for (uid, iid, r) in zip(df[usercolname], df[idcolname], df[reviewcolname])]
    #testset formatted in proper surprise format
    return testset

def create_KNNmodel(trainset, k=50, min_k=5, user_based=True, random_state=12345):
    """Train the KNN model given a training set and model parameters
    
    Arguments:
        trainset {surprise.trainset.Trainset} -- training set, output from build_trainset
        k_tuned {int} -- number of neighbors, parameter for algorithm (default: {50})
        min_k_tuned{int} -- minimum neighbors, parameter for algorithm (default: {5})
        user_based_tuned {bool} -- user based or not, parameter for algorithm (default: {True})
        seed {int} -- random seed (default: {12345})

    Returns:
        model {surprise.prediction_algorithms.knns.KNNBasic} -- trained model object
    """
    model = KNNBasic(k=k, min_k=min_k, user_based=user_based, random_state=random_state)
    #created KNNmodel
    model.fit(trainset)

    return model

def get_top_n(predictions, toplist=None, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Arguments:
        predictions {list of Prediction objects} -- The list of predictions, as returned by the test method of an algorithm.
        toplist {pd.DataFrame} -- IDs of top items that have been already shown to user (default: {None})
        n {int}: The number of recommendations to output for each user. (default: {10})

    Returns:
        top_n {collections.defaultdict} -- A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """
    # First map the predictions to each user.
    top_n = defaultdict(list)
    if toplist is not None:
        for uid, iid, true_r, est, _ in predictions:
            if iid in toplist:
                logger.info('Skipped item due to presence in toplist.')
            else:
                top_n[uid].append((iid, est))
    else:
        for uid, iid, true_r, est, _ in predictions:
            top_n[uid].append((iid, est))
    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]
    return top_n


def predictions(df, model, user_id, testset, toplist, colnames, idcolname='Beer_ID', n=10):
    """Gets the top-n item predictions for a given user and produces those rows of the original dataset

    Arguments:
        df {pd.DataFrame} -- Original dataset
        model {model} -- a trained object from the Surprise package, output of build_KNNmodel
        user_id {str} -- User name provided by user
        testset {list} -- list in test format that Surprise requires, output of build_testset
        toplist {list} -- IDs of top items that have been already shown to user (default: {None})
        colnames -- columns of original dataset you wish to return (default: {None})
        idcolname -- name of item id column (default: {Beer_ID})
        n {int}: The number of recommendations to output for each user. (default: {10})

    Returns:
        user_recommend {pd.DataFrame} - colname columns of the original data for the top-n item predictions for a given user
    """
    predictions = model.test(testset) #test model on test set
    top_n = get_top_n(predictions, toplist, n) #get top n recommendations
    top_list = top_n[user_id] #targeting one user
    user_score = pd.DataFrame(top_list).rename(columns={0: idcolname, 1: 'score'}) #formatting score
    user_recommend = pd.merge(user_score, get_unique_items(df, colnames), on=idcolname, how='left')
    return user_recommend #final df

def top_fromdata(data, i, config):
    """Gets relevant information about top most popular rows in a dataset for a specific category pandas dataframe
    
    Arguments: 
        data {pd.DataFrame} -- Pandas DataFrame
        i {str} -- category value to filter the data on
        config {dict} -- configuration dictionary
    
    Returns:
        typedata {pd.DataFrame} -- data filtered by category value i (category column specified by config)
        itemlist {list} -- list of unique values of a column, specified by config, in data
        topdf {pd.DataFrame} -- n rows of data corresponding to top most popular items, sorted
        toplist {list} -- list of unique values of a column, specified by config, in topdf
    """
    typedata = filter_data(data, i, **config['filter_data']) #filter by type
    itemlist = get_unique_items(typedata, **config['get_unique_items']) #get unique items
    topdf = top_n_popular(typedata, **config['top_n_popular']) #find top n popular items
    toplist = get_unique_items(topdf, config['idcolname']) #get itemlist from top n popular

    return typedata, itemlist, topdf, toplist

def onepred_fromdata(j, user_rows, toplist, typedata, config):
    """Produces predictions for a single user
    
    Arguments:
        j {str} -- User ID 
        user_rows {pd.DataFrame} -- Dataframe rows for new users with ratings for chosen items 
        toplist {list} -- list of unique values of a column, specified by config, in topdf
        typedata {pd.DataFrame} -- data filtered by category value i (category column specified by config)
        config {dict} -- configuration dictionary
    
    Returns:
        preds {pd.DataFrame} -- colname columns of the original data for the top-n item predictions for a given user
    """
    userdata = filter_data(user_rows, j, **config['filter_data_user']) #filter by user
    trainset = build_trainset(typedata, userdata, **config['build_trainset']) #build trainset
    logger.info('Trainset built.')
    testset = build_testset(userdata, **config['build_testset']) #build testset
    logger.info('Testset built')
    model = create_KNNmodel(trainset, **config['create_KNNmodel']) #make model
    logger.info('Model built.')
    preds = predictions(typedata, model, j, testset, toplist, **config['predictions']) #predict for single user
    preds['ID'] = j #add unique user id
    return preds

def run_train(args):
    """Runs script to run training
    
    Arguments:
        args {argparse.Namespace} -- Script arguments
    
    Raises:
        ValueError: "Path to yaml config file must be provided through --config" if args.config not specified
        ValueError: "Path to CSV for input data must be provided through --input" if args.input not specified
        ValueError: "Path to CSV for output preds data must be provided through --output_preds" if args.output_preds not specified
        ValueError: "Path to CSV for output top10 data must be provided through --output_top10rows" if args.output_top10rows not specified
        ValueError: "Path to CSV for output combinations data must be provided through --output_combinations" if args.output_combinations not specified
    """
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['train_model']
    else:
        raise ValueError("Path to yaml config file must be provided through --config")
    if args.input is not None:
        data = pd.read_csv(args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")
    predoutput = []
    top10output = []
    combinationoutput = []
    for i in config['types']:
        typedata, itemlist, topdf, toplist = top_fromdata(data, i, config)
        top10output.append(topdf)
        combrows = create_combinations(topdf, i, **config['create_combinations'])
        combinationoutput.append(combrows)
        user_rows, user_idlist = user_rows_combination_df(combrows, itemlist, **config['user_rows_combination_df'])
        for j in user_idlist:
            preds = onepred_fromdata(j, user_rows, toplist, typedata, config)
            predoutput.append(preds)
    output_preds_df = pd.concat(predoutput, ignore_index=True)
    output_top10_df = pd.concat(top10output, ignore_index=True)
    output_combination_df = pd.concat(combinationoutput, ignore_index=True)
    if args.output_preds is not None:
        output_preds_df.to_csv(args.output_preds, index=False)
    else:
        raise ValueError("Path to CSV for output preds data must be provided through --output_preds")
    if args.output_top10rows is not None:
        output_top10_df.to_csv(args.output_top10rows, index=False)
    else:
        raise ValueError("Path to CSV for output top10 data must be provided through --output_top10rows")
    if args.output_combinations is not None:
        output_combination_df.to_csv(args.output_combinations, index=False)
    else:
        raise ValueError("Path to CSV for output combinations data must be provided through --output_combinations")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    parser.add_argument('--input', default='data/cleaned_beer_reviews.csv', help='config.yml')
    parser.add_argument('--output_preds', default='data/preds.csv', help='config.yml')
    parser.add_argument('--output_top10rows', default='data/top10.csv', help='config.yml')
    parser.add_argument('--output_combinations', default='data/combinations.csv', help='config.yml')
    args = parser.parse_args()

    run_train(args)

    
            
            
