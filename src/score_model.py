from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split, KFold
from collections import defaultdict
from itertools import combinations
try:
    import train_model as tm 
except:
    import src.train_model as tm
import pandas as pd
import numpy as np
import argparse
import logging
import yaml

def precision_recall_at_k(predictions, k=10, threshold=3):
    """Returns average precision and recall at k metrics for each user.
    
    Arguments:
        predictions: {list of Prediction objects} -- The list of predictions, as returned by the test method of an algorithm.
        k {int} -- number of metrics -- (default: {10})
        threshold {int} -- ratings threshold -- (default {3})
    Returns:
        Tuple consisting of:
        precision {float} -- Average precision of the model
        recall {float} -- Average recall of the model
    """
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r)) # First map the predictions to each user.
    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():
        
        user_ratings.sort(key=lambda x: x[0], reverse=True) # Sort user ratings by estimated value
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)  # Number of relevant items       
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])  # Number of recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold)) # Number of relevant and recommended items in top k
                              for (est, true_r) in user_ratings[:k])
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1  # Precision@K: Proportion of recommended items that are relevant
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1  # Recall@K: Proportion of relevant items that are recommended
    
    return precisions, recalls

def data_model_forcrossvalidation(data, config_train):
    """Creates data and empty model for use in kfold_crossvalidation function
    
    Arguments:
        data {pd.DataFrame} -- Pandas DataFrame
        config_train {dict} -- Dictionary of configurations corresponding to the train_model script
    
    Returns:
        data {surprise.dataset.DatasetAutoFolds} -- Surprise Dataset ready for cross validation
        model {surprise.prediction_algorithms.knns.KNNBasic} -- Surprise KNNBasic Model
    """
    t_configs = config_train['build_trainset'] #configurations for trainset
    data = data[t_configs['colnames']] #colnames configuration
    reader = Reader()
    data = Dataset.load_from_df(data, reader) #create surprise dataset
    model = KNNBasic(**config_train['create_KNNmodel']) #create knnmodel
    return data, model

def kfold_crossvalidation(data, model, folds=5, k=5, threshold=4):
    """Preforms K fold crossvalidation on a KNN surprise model and returns average precision and recall.
    
    Arguments:
        data {surprise.dataset.DatasetAutoFolds} -- Surprise Dataset
        model {surprise.prediction_algorithms.knns.KNNBasic} -- Surprise KNNBasic model
        folds {int} -- number of folds in cross validation (default: {5})
        k {int} -- number of metrics -- (default: {10})
        threshold {int} -- ratings threshold -- (default {3})
    
    Returns:
        Tuple consisting of:
        average_precision {float} -- Average precision of the model
        average_recall {float} -- Average recall of the model
    """
    kf = KFold(n_splits=folds)
    preclist = []
    reclist = []
    for trainset, testset in kf.split(data): #cross validation splits
        model.fit(trainset) #fit model on trainset
        predictions = model.test(testset)
        precisions, recalls = precision_recall_at_k(predictions, k=k, threshold=threshold)
        total_precision = (sum(prec for prec in precisions.values()) / len(precisions))
        total_recall = (sum(rec for rec in recalls.values()) / len(recalls))
        preclist.append(total_precision)
        reclist.append(total_recall)
    average_precision = np.mean(preclist)
    average_recall = np.mean(reclist)
    return average_precision, average_recall

def create_output(data, model, outputtxt, config):
    """Creates model scoring output of precision and recall
    
    Arguments:
        data {surprise.dataset.DatasetAutoFolds} -- Surprise Dataset
        model {surprise.prediction_algorithms.knns.KNNBasic} -- Surprise KNNBasic model
        outputtxt {str} -- File path for output text file
        config {dict} -- Dictionary of configurations corresponding to the score_model script
    
    Raises:
        ValueError: "Path to textfile for outputtxt data must be provided through --outputtxt
    """
    average_precision, average_recall = kfold_crossvalidation(data, model, **config['kfold_crossvalidation'])
    if outputtxt is not None:
        with open(outputtxt, "w") as f:
            print('Average Precision of Model: %0.3f' % average_precision, file = f)
            print('Average Recall of Model: %0.3f' % average_recall, file = f)
        logger.info('Model evaluation saved to text file.')
    else:
        raise ValueError("Path to textfile for outputtxt data must be provided through --outputtxt")

def run_scoring(args):
    """Runs script to run scoring
    
    Arguments:
        args {argparse.Namespace} -- Script arguments
    
    Raises:
        ValueError: "Path to yaml config file must be provided through --config" if args.config not specified
        ValueError: "Path to CSV for input data must be provided through --input" if args.input not specified
        ValueError: "Path to textfile for outputtxt data must be provided through --outputtxt" if args.outputtxt not specified
    """
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config_train = config['train_model']
        config_score = config['score_model']
    else:
        raise ValueError("Path to yaml config file must be provided through --config")

    if args.input is not None:
        data = pd.read_csv(args.input)
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")
    typedata = tm.filter_data(data, config_score['test_type'], **config_train['filter_data'])
    finaldata, model = data_model_forcrossvalidation(typedata, config_train)
    if args.outputtxt is not None:
        create_output(finaldata, model, args.outputtxt, config_score)
    else:
        raise ValueError("Path to textfile for outputtxt data must be provided through --outputtxt")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    parser.add_argument('--input', default='data/cleaned_beer_reviews.csv', help='config.yml')
    parser.add_argument('--outputtxt', default='data/modelscoring.txt', help='config.yml')
    args = parser.parse_args()

    run_scoring(args)

    

