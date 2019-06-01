import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise.model_selection import train_test_split, KFold
from collections import defaultdict
from itertools import combinations
import yaml
import os
import logging
import argparse
import train_model as tm 

def precision_recall_at_k(predictions, outputtxt = None, k=10, threshold=3):
    """Returns average precision and recall at k metrics for each user.
    
    Arguments:
        predictions: {list of Prediction objects} -- The list of predictions, as returned by the test method of an algorithm.
        outputtxt -- file path for text output -- (default: {None})
        k {int} -- number of metrics -- (default: {10})
        threshold {int} -- ratings threshold -- (default {3})
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

def cross_validate(data, outputtxt, colnames, k_tuned, min_k_tuned, user_based_tuned, seed, folds):
    data = data[colnames]
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(data, reader)
    algo_KNNbasic = KNNBasic(k = k_tuned, min_k = min_k_tuned, user_based=user_based_tuned, random_state = seed)
    kf = KFold(n_splits=folds)
    for trainset, testset in kf.split(data):
        algo_KNNbasic.fit(trainset)
        predictions = algo_KNNbasic.test(testset)
        precisions, recalls = precision_recall_at_k(predictions, k=5, threshold=4)

    # Precision and recall can then be averaged over all users
    print(sum(prec for prec in precisions.values()) / len(precisions))
    print(sum(rec for rec in recalls.values()) / len(recalls))
    total_precision = (sum(prec for prec in precisions.values()) / len(precisions))
    total_recall = (sum(rec for rec in recalls.values()) / len(recalls))
    if outputtxt is not None:
        with open(outputtxt, "w") as f:
            print('Average Precision of Model: %0.3f' % total_precision, file = f)
            print('Accuracy Recall of Model: %0.3f' % total_recall, file = f)
        logger.info('Model evaluation saved to text file.')
    else:
        raise ValueError("Path to textfile for outputtxt data must be provided through --outputtxt")

def run_scoring(args):
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config_train = config['train_model']
        config_score = config['score_model']
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")

    if args.input is not None:
        data = pd.read_csv(args.input)
        typedata = tm.filter_data(data, config_score['test_type'], **config_train['filter_data'])
        if args.outputtxt is not None:
            cross_validate(data, args.outputtxt, **config_score['cross_validate'])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    parser.add_argument('--input', default='../data/cleaned_beer_reviews.csv', help='config.yml')
    parser.add_argument('--outputtxt', default='../data/modelscoring.txt', help='config.yml')
    args = parser.parse_args()

    run_scoring(args)

    

