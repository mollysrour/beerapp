import collections
from collections import defaultdict
import src.train_model as tm
import surprise
import pandas as pd

def test_filter_data():
    """Tests the filter_data function"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    value = 'BeerA'
    col = 'Beer_ID'
    answers = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD']}
    output = pd.DataFrame(answers)
    assert isinstance(tm.filter_data(the_input, value, col), pd.DataFrame)
    assert output.equals(tm.filter_data(the_input, value, col))

def test_filter_data_bad():
    """Tests the filter_data function for a bad path"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    value = 'BeerA'
    col = 'Beer_IDOOPS'
    try:
        tm.filter_data(the_input, value, col)
        assert False
    except KeyError:
        assert True
    
def test_get_unique_items():
    """Tests the get_unique_items function"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    col_one = 'Beer_ID'
    output_one = ['BeerA', 'BeerB']
    col_many = ['Beer_ID', 'Reviewer']
    output_many = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    theoutput_many = pd.DataFrame(output_many)
    assert isinstance(tm.get_unique_items(the_input, col_one), list)
    assert isinstance(tm.get_unique_items(the_input, col_many), pd.DataFrame)
    assert output_one == tm.get_unique_items(the_input, col_one)
    assert theoutput_many.equals(tm.get_unique_items(the_input, col_many))

def test_get_unique_items_bad():
    """Tests the get_unique_items function for a bad path"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    col_one = 'Beer_IDOOPS'
    col_many = ['Beer_IDOOPS', 'Reviewer']
    try:
        tm.get_unique_items(the_input, col_one)
        assert False
    except KeyError:
        assert True
    try:
        tm.get_unique_items(the_input, col_many)
        assert False
    except KeyError:
        assert True

def test_top_n_popular():
    """Tests the top_n_popular function"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerB', 'BeerB', 'BeerC'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    colnames = ['Beer_ID', 'review_overall']
    idcolname = 'Beer_ID'
    reviewcolname = 'review_overall'
    n = 2
    answers = {'Beer_ID': ['BeerC', 'BeerB'],
        'review_overall': [4.0, 3.0]}
    output = pd.DataFrame(answers)
    assert isinstance(tm.top_n_popular(the_input, colnames, idcolname, reviewcolname, n), pd.DataFrame)
    assert output.equals(tm.top_n_popular(the_input, colnames, idcolname, reviewcolname, n))

def test_top_n_popular_bad():
    """Tests the top_n_popular function for a bad path"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerB', 'BeerB', 'BeerC'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    colnames = ['Beer_ID', 'review_overall']
    idcolname = 'Beer_IDOOPS'
    reviewcolname = 'review_overall'
    n = 2
    try:
        tm.top_n_popular(the_input, colnames, idcolname, reviewcolname, n)
        assert False
    except KeyError:
        assert True

def test_create_combinations():
    """Tests the create_combinations function"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC']}
    the_input = pd.DataFrame(inputs)
    typename = 'Test'
    n = 2
    answers = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'review_overall': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    output = pd.DataFrame(answers)
    assert isinstance(tm.create_combinations(the_input, typename, n), pd.DataFrame)
    assert output.equals(tm.create_combinations(the_input, typename, n))

def test_create_combinations_bad():
    """Tests the create_combinations function for a bad path"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC']}
    the_input = pd.DataFrame(inputs)
    typename = 'Test'
    n = 'OOPS'
    try:
        tm.create_combinations(the_input, typename, n)
        assert False
    except ValueError:
        assert True

def test_create_user_rows():
    """Tests the create_user_rows function"""
    user_choices = ['BeerA', 'BeerB']
    user_id = 'Test1'
    idlist = ['BeerA', 'BeerB', 'BeerC', 'BeerD', 'BeerE', 'BeerF']
    reviewcolname = 'Mean_Review'
    idcolname = 'Beer_ID'
    usercolname = 'Reviewer'
    answers = {'Reviewer': ['Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1'],
            'Beer_ID': ['BeerA', 'BeerB', 'BeerC', 'BeerD', 'BeerE', 'BeerF'],
            'Mean_Review': [5, 5, 0, 0, 0, 0]}
    output = pd.DataFrame(answers)
    assert isinstance(tm.create_user_rows(user_choices, user_id, idlist, reviewcolname, idcolname, usercolname), pd.DataFrame)
    assert output.equals(tm.create_user_rows(user_choices, user_id, idlist, reviewcolname, idcolname, usercolname))

def test_create_user_rows_bad():
    """Tests the create_user_rows function for a bad path"""
    user_choices = ['BeerG', 'BeerH']
    user_id = 'Test1'
    idlist = ['BeerA', 'BeerB', 'BeerC', 'BeerD', 'BeerE', 'BeerF']
    reviewcolname = 'Mean_Review'
    idcolname = 'Beer_ID'
    usercolname = 'Reviewer'
    try:
        tm.create_user_rows(user_choices, user_id, idlist, reviewcolname, idcolname, usercolname)
        assert False
    except ValueError:
        assert True

def test_user_rows_combination_df():
    """Tests the user_rows_combination_df function"""
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'review_overall': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    idlist = ['BeerA', 'BeerB']
    reviewcolname = 'review_overall'
    idcolname = 'Beer_ID'
    usercolname = 'Reviewer'
    
    answers = {'Reviewer': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3'],
            'Beer_ID': ['BeerA', 'BeerB', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
            'review_overall': [5, 0, 5, 5, 5, 5]}
    output = pd.DataFrame(answers)
    answers2 = ['Test1', 'Test2', 'Test3']
    assert isinstance(tm.user_rows_combination_df(the_input, idlist, reviewcolname, idcolname, usercolname)[0], pd.DataFrame)
    assert isinstance(tm.user_rows_combination_df(the_input, idlist, reviewcolname, idcolname, usercolname)[1], list)
    assert output.equals(tm.user_rows_combination_df(the_input, idlist, reviewcolname, idcolname, usercolname)[0])
    assert answers2 == tm.user_rows_combination_df(the_input, idlist, reviewcolname, idcolname, usercolname)[1]

def test_build_trainset():
    """Tests the build_trainset function"""
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
    assert isinstance(tm.build_trainset(the_input, user_rows, colnames), surprise.trainset.Trainset)

def test_build_testset():
    """Tests the build_testset function"""
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'Mean_Review': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    reviewcolname = 'Mean_Review'
    idcolname = 'Beer_ID'
    usercolname = 'Reviewer'
    answers = [('ReviewerA', 'BeerA', 1.5), ('ReviewerB', 'BeerA', 3.0), ('ReviewerA', 'BeerA', 1.5),
               ('ReviewerC', 'BeerB', 3.0), ('ReviewerB', 'BeerA', 3.0), ('ReviewerC', 'BeerB', 3.0)]
    assert isinstance(tm.build_testset(the_input, reviewcolname, idcolname, usercolname), list)
    assert len(answers) == 6
    assert len(answers[0]) == 3
    assert answers == tm.build_testset(the_input, reviewcolname, idcolname, usercolname)

def test_create_KNNmodel():
    """Tests the create_KNNmodel function"""
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
    assert isinstance(tm.create_KNNmodel(trainset, k, min_k, user_based, random_state), surprise.prediction_algorithms.knns.KNNBasic)

def test_get_top_n():
    """Tests the get_top_n function"""
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
    toplist = ['BeerE','BeerF']
    n=2
    predictions = model.test(testset)
    answers = defaultdict(list, {'ReviewerA': [('BeerA', 1.9412081984897525), ('BeerA', 1.9412081984897525)],
    'ReviewerB': [('BeerA', 2.8142076502732243), ('BeerA', 2.8142076502732243)], 
    'ReviewerC': [('BeerB', 2.0833333333333335), ('BeerB', 2.0833333333333335)]})
    assert answers == (tm.get_top_n(predictions, toplist, n))
    assert isinstance(tm.get_top_n(predictions, toplist, n), collections.defaultdict)

def test_predictions():
    """Tests the predictions function"""
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
    toplist = ['BeerE','BeerF']
    n=2
    user_id='ReviewerC'
    answers = {'Beer_ID': ['BeerB', 'BeerB'], 'score': [2.0833333333333335, 2.0833333333333335], 'Reviewer': ['ReviewerC', 'ReviewerC'], 
            'Mean_Review': [3.0, 3.0]}
    output = pd.DataFrame(answers)
    assert output.equals(tm.predictions(the_input, model, user_id, testset, toplist, colnames, idcolname, n))
    assert isinstance(tm.predictions(the_input, model, user_id, testset, toplist, colnames, idcolname, n), pd.DataFrame)
    



