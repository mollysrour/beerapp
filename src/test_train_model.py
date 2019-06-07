import src.train_model as tm 
import pandas as pd

def test_filter_data():
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reveiwer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    value = 'BeerA'
    col = 'Beer_ID'
    answers = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0],
        'Reveiwer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD']}
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