import src.train_model as tm
import surprise
import pandas as pd

def test_filter_data():
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

def test_get_unique_items():
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

def test_top_n_popular():
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerB', 'BeerB', 'BeerC'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    colnames = ['Beer_ID', 'review_overall']
    idcolname = 'Beer_ID'
    reviewcolname = 'review_overall'
    n = 2
    answers = {'Beer_ID': ['BeerB', 'BeerC'],
        'review_overall': [3.0, 4.0]}
    output = pd.DataFrame(answers)
    assert isinstance(tm.top_n_popular(the_input, colnames, idcolname, reviewcolname, n), pd.DataFrame)
    assert output.equals(tm.top_n_popular(the_input, colnames, idcolname, reviewcolname, n))

def test_create_combinations():
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

def test_create_user_rows():
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

def test_user_rows_combination_df():
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
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'Mean_Review': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    userrowsdict = answers = {'Reviewer': ['Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1'],
            'Beer_ID': ['BeerA', 'BeerB', 'BeerC', 'BeerD', 'BeerE', 'BeerF'],
            'Mean_Review': [5, 5, 0, 0, 0, 0]}
    user_rows= pd.DataFrame(userrowsdict)
    colnames = ['Reviewer', 'Beer_ID', 'Mean_Review']
    assert isinstance(tm.build_trainset(the_input, user_rows, colnames), surprise.trainset.Trainset)

def test_build_testset():
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

def test_build_testset():
    inputs = {'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerB', 'BeerA', 'BeerB'],
        'Mean_Review': [1.5, 3.0, 1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerA', 'ReviewerC', 'ReviewerB', 'ReviewerC'],
        'ID': ['Test1', 'Test1', 'Test2', 'Test2', 'Test3', 'Test3']}
    the_input = pd.DataFrame(inputs)
    userrowsdict = answers = {'Reviewer': ['Test1', 'Test1', 'Test1', 'Test1', 'Test1', 'Test1'],
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