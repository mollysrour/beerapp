import pandas as pd
import numpy as np 
import argparse
import logging
import yaml

def create_mean_column(df, columns, name='mean_col'):
    """Creates a column of a pandas dataframe that is a mean of values in other columns
    
    Arguments:
        df {pd.DataFrame} -- Pandas data frame
        columns {list} -- list of columns to average values to create mean column
        name {str} -- name of new column (Default: {'mean_col'})
    
    Returns:
        df {pd.DataFrame} - dataframe with new column added
    """
    try:
        cols = df[columns] #just the columns of interest
    except:
        raise KeyError("Incorrect column names.")
        logger.error('Column names are incorrect. Re-enter column names.')
    values = list(cols.mean(axis=1).values) #mean value across these columns of interest
    df.loc[:, name] = values #creates new column with specified name with values as the mean values from above
    return df

def omit_values(df, column, valuelist):
    """Omits rows of pandas dataframe that has one of a set of values in a given column 
    
    Arguments:
        df {pd.DataFrame} -- Pandas data frame
        column {str} -- name of column to be evaluated
        valuelist {list} -- list of values that, if contained in the given column, means that a row should be omitted from the data frame
    
    Returns:
        df {pd.DataFrame} - dataframe with rows omitted
    """
    try:
        df = df[~df[column].isin(valuelist)] #Only keep rows with column values NOT in valuelist
    except: 
        raise KeyError('Incorrect column name.')
        logger.error('Column name is incorrect. Re-enter column name.')
    df = df.reset_index(drop=True) #Remove prior dataframe indexes
    return df

def aggregated_category_column(df, narrowcolumn, valuedict, broadcategory='beer_type'):
    """Creates an aggregated category column of a pandas dataframe that has particular values dictated by aggregating values 
    from the categorical narrowcolumn to a broader category
    
    Arguments:
        df {pd.DataFrame} -- Pandas data frame
        narrowcolumn {str} -- Name of narrow categorical column to be aggregated
        valuedict {dict} -- dictionary that has key: value pairs in the form of str: list. Str is 
        the created value for the aggregated column corresponding to the list of values in the narrow column
        broadcategory {str} --Name of the aggregated column to be created (Default: {'beer_type'})
    
    Returns:
        df {pd.DataFrame} - dataframe with new column added
    """ 
    for key, value in valuedict.items(): #iterating over key/value pair in valuedict
        try:
            df.loc[df[narrowcolumn].isin(value), broadcategory] = key #assigning key to broadcategory column for rows with values in narrow column
        except:
            raise KeyError('Either your narrowcolumn anme or your valuedict has incorrect values.')
            logger.error('Column name or value dictionary has been entered incorrectly. Please re-enter.')
    return df

def select_rename_features(df, oldnames, newnames):
    """Selects target features from a data frame and renames them. Returns the df with only the selected, renamed features
    
    Arguments:
        df {pd.DataFrame} -- Pandas data frame
        oldnames {list} -- List of feature names to be included in the df (current names)
        newnames {list} -- List of names for features to be renamed
    
    Returns:
        df {pd.DataFrame} -- Pandas data frame with only the selected renamed features
    """
    if range(len(oldnames)) == range(len(newnames)): #checking that names to replace is same length as old names
        for i in range(len(oldnames)):
            df = df.rename(columns={oldnames[i]: newnames[i]}) #rename columns
    else:
        raise ValueError('Length mismatch.')
        logger.error('List of features to be renamed must have same length as list of new names')
    return df[newnames] #select only renamed columns

def refine_data(df, idcolname='Beer_ID', usercolname='Reviewer', n=15):
    """Removes items from reviews dataframe who have less than n reviews.
    
    Arguments:
        df {pd.DataFrame} -- Pandas Data Frame 
        idcolname {str} -- name of item id column (Default: {'Beer_ID'})
        usercolname {str} -- name of user id column (Default: {'Reviewer'})
        n {int} -- Review threshold (Default: {15})
    
    Returns:
        df{pd.DataFrame} -- filtered Data Frame
    """
    try:
        df_grouped = df.groupby(idcolname).count() #group by idcolname, count number of reviews
    except:
        raise KeyError('Incorrect ID column name')
        logger.error('Please re-enter ID column name.')
    try:
        df_grouped =  df_grouped[df_grouped[usercolname] >=n] #only include rows with number of reviews > n
    except:
        raise KeyError('Incorrect User Column Name')
        logger.error("Please re-enter user column name.")
    df = df[df[idcolname].isin(df_grouped.index)] #select rows specified from df grouped
    df = df.reset_index(drop=True) #reset index to remove old df indexes
    return df

def run_clean(args):
    """Runs script to clean data.
    
    Arguments:
        args {argparse.Namespace} -- Script arguments, in this case, path to config file.
    
    Raises:
        ValueError: "Path to yaml config file must be provided through --config" if args.config not specified
        ValueError: "Path to CSV for input data must be provided through --input" if args.input not specified
        ValueError: "Path to CSV for output data must be provided through --output" if args.output not specified
    """
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['clean_data']
    else:
        raise ValueError("Path to yaml config file must be provided through --config")
    if args.input is not None:
        data = pd.read_csv(args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")
    data = create_mean_column(data, **config['create_mean_column'])
    data = omit_values(data, **config['omit_values'])
    data = aggregated_category_column(data, **config['aggregated_category_column'])
    data = select_rename_features(data, **config['select_rename_features'])
    data = refine_data(data, **config['refine_data'])
    logger.info('Cleaned Data')
    if args.output is not None:
        data.to_csv(args.output, index=False)
    else:
        raise ValueError("Path to CSV for output data must be provided through --output")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml')
    parser.add_argument('--input', default='data/beer_reviews.csv')
    parser.add_argument('--output', default='data/cleaned_beer_reviews.csv')
    args = parser.parse_args()
    
    run_clean(args)

    
