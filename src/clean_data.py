import pandas as pd
import numpy as np 
import argparse
import yaml
import logging

def create_mean_column(df, columns, name):
    """Creates a column of a pandas dataframe that is a mean of values in other columns
    
    Arguments:
        df {DataFrame} -- Pandas data frame
        columns {list} -- list of columns to average values to create mean column
        name {str} -- name of new column
    """

    df[name] = df[columns].mean(axis=1)
    return df

def omit_values(df, column, valuelist):
    """Omits rows of dataframe that has one of a set of values in a given column 
    
    Arguments:
        df {DataFrame} -- Pandas data frame
        column {str} -- name of column to be evaluated
        valuelist {list} -- list of values that, if contained in the given column, means that a row should be omitted from the data frame
    """
    df = df[~df[column].isin(valuelist)]
    return df

def aggregated_category_column(df, narrowcolumn, valuedict, broadcategory):
    """Creates an aggregated category column that has particular values dictated by values from narrowcolumn, 
    aggregating to a broader category
    
    
    Arguments:
        df {DataFrame} -- Pandas data frame
        narrowcolumn {str} -- Name of narrow categorical column to be aggregated
        valuedict {dict} -- dictionary that has key: value pairs in the form of str: list. Str is 
        the create value for the aggregated column corresponding to the list of values in the narrow column
        broadcategory {str} --Name of the aggregated column to be created
    """
    for key, value in valuedict.items():
        df.loc[df[narrowcolumn].isin(value), broadcategory] = key
    return df

def select_rename_features(df, oldnames, newnames):
    """Selects target features from a data frame and renames them. Returns the df with only the selected, renamed features
    
    Arguments:
        df {DataFrame} -- Pandas data frame
        oldnames {list} -- List of feature names to be included in the df (current names)
        newnames {list} -- List of names for features to be renamed
    
    Returns:
        df {DataFrame} -- Pandas data frame with only the selected renamed features
    """
    if range(len(oldnames)) == range(len(newnames)):
        for i in range(len(oldnames)):
            df = df.rename(columns={oldnames[i]: newnames[i]})
    else:
        raise ValueError('List of features to be renamed must have same length as list of new names')
    return df[newnames]

def refine_data(df, idcolname='Beer_ID', usercolname='Reviewer', n=15):
    """Removes items from dataframe who have less than n reviews.
    
    Arguments:
        df {pd.DataFrame} -- Pandas Data Frame 
        idcolname {str} -- name of item id column (Default: {'Beer_ID'})
        usercolname {str} -- name of user id column (Default: {'Reviewer'})
        n {int} -- Review threshold (Default: {15})
    
    Returns:
        df{pd.DataFrame} -- filtered Data Frame
    """
    df_grouped = df.groupby(idcolname).count()
    df_grouped =  df_grouped[df_grouped[usercolname] >=n]
    df = df[df[idcolname].isin(df_grouped.index)]
    return df

def run_clean(args):
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['clean_data']
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")
    if args.input is not None:
        data = pd.read_csv(args.input)
    else:
        raise ValueError("Path to yaml config file must be provided through --config")
    data = create_mean_column(data, **config['create_mean_column'])
    data = omit_values(data, **config['omit_values'])
    data = aggregated_category_column(data, **config['aggregated_category_column'])
    data = select_rename_features(data, **config['select_rename_features'])
    data = refine_data(data, **config['refine_data'])
    if args.output is not None:
        data.to_csv(args.output, index=False)
    else:
        raise ValueError("Path to CSV for output data must be provided through --output")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    parser.add_argument('--input', default='../data/beer_reviews.csv', help='config.yml')
    parser.add_argument('--output', default='../data/cleaned_beer_reviews.csv', help='config.yml')
    args = parser.parse_args()
    
    run_clean(args)

    
