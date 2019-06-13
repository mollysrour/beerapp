import src.score_model as sm 
import src.train_model as tm
import surprise
import pandas as pd 


def test_precision_recall_at_k():
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'Mean_Review': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    userrowsdict = {'Reviewer': ['Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1'],
            'Beer_ID': ['BeerA', 'BeerB', 'BeerC', 'BeerD', 'BeerE', 'BeerF'],
            'Mean_Review': [5, 5, 0, 0, 0, 0]}
    user_rows= pd.DataFrame(userrowsdict)
    colnames = ['Reviewer', 'Beer_ID', 'Mean_Review']
    trainset = tm.build_trainset(the_input, user_rows, colnames)
    k = 50
    min_k = 5
    user_based = True
    random_state = 12345
    reviewcolname = 'Mean_Review'
    idcolname = 'Beer_ID'
    usercolname = 'Reviewer'
    testset = tm.build_testset(the_input, reviewcolname, idcolname, usercolname)
    model = tm.create_KNNmodel(trainset, k, min_k, user_based, random_state)
    predictions = model.test(testset)
    k = 10
    threshold = 3
    answers = ({'ReviewerA': 1, 'ReviewerB': 1, 'ReviewerC': 1}, {'ReviewerA': 1, 'ReviewerB': 0.0, 'ReviewerC': 0.0})
    assert answers == sm.precision_recall_at_k(predictions, k, threshold)
    assert isinstance(sm.precision_recall_at_k(predictions, k, threshold), tuple)
    assert len(sm.precision_recall_at_k(predictions, k, threshold)) == 2

def test_data_model_forcrossvalidation():
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'Mean_Review': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    config_train = {}
    config_train['build_trainset'] = {}
    config_train['build_trainset']['colnames'] = ['Reviewer', 'Beer_ID', 'Mean_Review']
    config_train['create_KNNmodel'] = {}
    config_train['create_KNNmodel']['k'] = 50
    config_train['create_KNNmodel']['min_k'] = 5
    config_train['create_KNNmodel']['user_based'] = True
    config_train['create_KNNmodel']['random_state'] = 12345
    assert isinstance(sm.data_model_forcrossvalidation(the_input, config_train)[0], surprise.dataset.DatasetAutoFolds)
    assert isinstance(sm.data_model_forcrossvalidation(the_input, config_train)[1], surprise.prediction_algorithms.knns.KNNBasic)

def test_kfold_crossvalidation():
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'Mean_Review': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    config_train = {}
    config_train['build_trainset'] = {}
    config_train['build_trainset']['colnames'] = ['Reviewer', 'Beer_ID', 'Mean_Review']
    config_train['create_KNNmodel'] = {}
    config_train['create_KNNmodel']['k'] = 50
    config_train['create_KNNmodel']['min_k'] = 5
    config_train['create_KNNmodel']['user_based'] = True
    config_train['create_KNNmodel']['random_state'] = 12345
    data, model = sm.data_model_forcrossvalidation(the_input, config_train)
    folds = 5
    k = 5
    threshold = 4
    answers = (1.0, 1.0)
    assert answers == sm.kfold_crossvalidation(data, model, folds, k, threshold)
    assert isinstance(sm.kfold_crossvalidation(data, model, folds, k, threshold), tuple)

