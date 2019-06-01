import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from collections import defaultdict
from itertools import combinations
import yaml
import os
import logging
import argparse

def filter_data(df, value, col):
    """Given a data frame, column name, and value, outputs data frame with rows that have that value in the column
    in the typecol

    Arguments:
    df {pd.DataFrame} -- Pandas DataFrame
    value {str} -- Name of specific value of column to filter on
    col {str} -- Name of column to filter on

    Returns:
    onetypedf {pd.DataFrame} -- Filtered DataFrame
    """
    onetypedf = df[df[col]==value]
    return onetypedf

def get_unique_items(df, col):
    """Given a dataframe and column name or list of column names, outputs unique items or rows. If given a column name,
    outputs a list of unique items in that column. If given a list of column names, outputs unique combinations of those columns.
    
    Arguments:
        df {pd.DataFrame} -- Pandas DataFrame
        col {str or list} -- Specified column name or list of column names
    
    Returns:
        itemlist {list} -- List of unique items in col or unique combinations of columns
    """
    itemlist = df[col].drop_duplicates()
    return itemlist

def top_ten_popular(df, typename, colnames, typecolname='Type', idcolname='Beer_ID', reviewcolname='Mean_Review'):
    """Returns the top ten most popular items in a dataset given a specific value of the type column.

    Args:
        df {pd.DataFrame} -- Full dataframe
        typename {str} -- specified value of type column 
        colnames {list} -- list of column names needed to in the top10df
        typecolname {str} -- column name for type (default: {'Type'})
        idcolname {str} -- column name for item id (default: {'Beer_ID'})
        reviewcolname {str} -- column name for reviews (default: {'Mean_Review'})

    Returns:
        top10df {pd.DataFrame} -- DF showing the rows corresponding to the top 10 items, with review and profile name dropped.
    """
    df_onetype = df[df[typecolname]==typename] #df filtered by value in type column
    df_groupedbyID = df_onetype.groupby([idcolname]).mean() #df grouped by item id, averaging reviews
    df_groupedbyID = df_groupedbyID.sort_values(reviewcolname, ascending=False) #sort df by review, descending
    top10 = df_groupedbyID.index[0:10].values.tolist() #find index of top 10 items
    top10df = df_onetype[df_onetype[idcolname].isin(top10)][colnames].drop_duplicates() #df containing the top 10 items
    return top10df


def create_combinations(df, typename, n=2):
    """Creates dataframe of all possible row combinations of n rows, given a dataframe. Also creates column 'ID' based on user input 
    of a string.

    Args:
        df {pd.DataFrame} -- Full dataframe
        typename {str} -- specified value that will be created as ID col (with index appended)
        n {int} -- number of rows in each combination. (default: {2})

    Returns:
        combdf {pd.DataFrame} -- DF of all possible row combinations of n rows with ID column added. Total number of rows will be
                                nrow(df) choose n.
    """
    thelist = []
    i = 1
    for index in list(combinations(df.index,n)):
        minidf = df.loc[index,:]
        minidf['ID'] = typename + str(i)
        thelist.append(minidf)
        i=i+1
    combdf = pd.concat(thelist, ignore_index=True)
    return combdf

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
    user_rows = pd.DataFrame({usercolname: user_id,
                                idcolname: idlist, reviewcolname: 0})
    choiceitems = user_rows[idcolname].isin(user_choices)
    user_rows.loc[choiceitems, reviewcolname] = 5
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
    for i in list(range(0, len(combdf.index), n)):
        j=i+1
        pair = combdf.loc[i:j,]
        user_id = pair['ID'][i]
        user_rows = create_user_rows(pair[idcolname], user_id, idlist, reviewcolname, idcolname, usercolname)
        thelist.append(user_rows)
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

    Returns:
        trainset {surprise.trainset.Trainset} -- training data in the Surprise package format
    """
    if colnames is not None:
        train = df[colnames]
    else:
        train = df
    reader = Reader(line_format='user item rating', rating_scale=(1, 5))
    if user_rows is not None:
        trainset_load = Dataset.load_from_df(pd.concat([train, user_rows]), reader)
    else:
        trainset_load = Dataset.load_from_df(train, reader)
    trainset = trainset_load.build_full_trainset()
    logger.info('Trainset built.')
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
    logger.info('Testset built.')
    return testset

def create_KNNmodel(trainset, testset, k_tuned=50, min_k_tuned=5, user_based_tuned=True, seed=12345):
    """Train the KNN model given a training set and model parameters
    
    Arguments:
        trainset {surprise.trainset.Trainset} -- training set, output from build_trainset
        k_tuned {int} -- number of neighbors, parameter for algorithm (default: {50})
        min_k_tuned{int} -- minimum neighbors, parameter for algorithm (default: {5})
        user_based_tuned {bool} -- user based or not, parameter for algorithm (default: {True})
        seed {int} -- random seed (default: {12345})

    Returns:
        model {model} -- trained model object
    """
    model = KNNBasic(k=k_tuned, min_k=min_k_tuned, user_based=user_based_tuned, random_state=seed)
    logger.info('Model built.')
    model.fit(trainset).test(testset)

    return model

def get_top_n(predictions, toptenlist=None, n=10):
    """Return the top-N recommendation for each user from a set of predictions.

    Arguments:
        predictions {list of Prediction objects} -- The list of predictions, as returned by the test method of an algorithm.
        toptenlist {pd.DataFrame} -- IDs of top ten items that have been already shown to user (default: {None})
        n {int}: The number of recommendations to output for each user. (default: {10})

    Returns:
        top_n {int} -- A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    """
    # First map the predictions to each user.
    top_n = defaultdict(list)
    if toptenlist is not None:
        for uid, iid, true_r, est, _ in predictions:
            if iid in toptenlist.values:
                print('skipped item')
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


def predictions(df, model, user_id, testset, toptenlist, colnames, idcolname='Beer_ID', n=10):
    """Gets the colnames columns of the original data for top-n item predictions for a given user

    Arguments:
        df {pd.DataFrame} -- Original dataset
        model {model} -- a trained object from the Surprise package, output of build_KNNmodel
        user_id {str} -- User name provided by user
        testset {list} -- list in test format that Surprise requires, output of build_testset
        toptenlist {list} -- IDs of top ten items that have been already shown to user (default: {None})
        colnames -- columns of original dataset you wish to return (default: {None})
        idcolname -- name of item id column (default: {Beer_ID})
        n {int}: The number of recommendations to output for each user. (default: {10})

    Returns:
        user_recommend: colname columns of the original data for the top-n item predictions for a given user
    """
    predictions = model.test(testset)
    top_n = get_top_n(predictions, toptenlist, n)
    top_list = top_n[user_id]
    user_score = pd.DataFrame(top_list).rename(columns={0: idcolname, 1: 'score'})
    user_recommend = pd.merge(user_score, get_unique_items(df, colnames), on=idcolname, how='left')
    return user_recommend

def run_train(args):
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['train_model']
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")

    if args.input is not None:
        data = pd.read_csv(args.input)
        predoutput = []
        top10output = []
        combinationoutput = []
        for i in config['types']:
            typedata = filter_data(data, i, **config['filter_data'])
            itemlist = get_unique_items(typedata, **config['get_unique_items'])
            top10df = top_ten_popular(typedata, i, **config['top_ten_popular'])
            toptenlist = get_unique_items(top10df, 'Beer_ID')
            top10output.append(top10df)
            combrows = create_combinations(top10df, i, **config['create_combinations'])
            combinationoutput.append(combrows)
            user_rows, user_idlist = user_rows_combination_df(combrows, itemlist, **config['user_rows_combination_df'])
            for j in user_idlist:
                userdata = filter_data(user_rows, j, **config['filter_data_user'])
                trainset = build_trainset(typedata, userdata, **config['build_trainset'])
                testset = build_testset(userdata, **config['build_testset'])
                model = create_KNNmodel(trainset, **config['create_KNNmodel'])
                preds = predictions(typedata, model, j, testset, toptenlist, **config['predictions'])
                preds['ID'] = j
                predoutput.append(preds)
        output_preds_df = pd.concat(predoutput, ignore_index=True)
        output_top10_df = pd.concat(top10output, ignore_index=True)
        output_combination_df = pd.concat(combinationoutput, ignore_index=True)
        if args.output_preds is not None:
            output_preds_df.to_csv(args.output_preds, index=False)
        if args.output_top10rows is not None:
            output_top10_df.to_csv(args.output_top10rows, index=False)
        if args.output_combinations is not None:
            output_combination_df.to_csv(args.output_combinations, index=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    parser.add_argument('--input', default='../data/cleaned_beer_reviews.csv', help='config.yml')
    parser.add_argument('--output_preds', default='../data/preds.csv', help='config.yml')
    parser.add_argument('--output_top10rows', default='../data/top10.csv', help='config.yml')
    parser.add_argument('--output_combinations', default='../data/combinations.csv', help='config.yml')
    args = parser.parse_args()

    run_train(args)

    
            
            
