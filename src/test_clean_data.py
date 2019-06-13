import src.clean_data as cd
import pandas as pd
import pytest

def test_create_mean_column():
    """Test the create_mean_column function"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0]}
    the_input = pd.DataFrame(inputs)
    columns = ['review_overall', 'review_appearance']
    name = 'mean_review'
    answers = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0], 
        'mean_review': [2.00, 3.00, 3.00, 3.25, 4.00]}
    output = pd.DataFrame(answers)
    assert isinstance(cd.create_mean_column(the_input, columns, name), pd.DataFrame)
    assert output.equals(cd.create_mean_column(the_input, columns, name))

def test_create_mean_column_bad():
    """Test the create_mean_column function for a bad path"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0]}
    the_input = pd.DataFrame(inputs)
    columns = ['review_overall', 'review_appearanceOOPS']
    name = 'mean_review'
    try:
        cd.create_mean_column(the_input, columns, name)
        assert False
    except KeyError:
        assert True

def test_omit_values():
    """Tests the omit_values function"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    the_input = pd.DataFrame(inputs)
    column = 'beer_style'
    valuelist = ['Hefeweizen', 'English Strong Ale']
    answers = {
        'brewery_id': [10325, 10325, 1075],
        'review_overall' : [3.0, 3.0, 4.0],
        'review_appearance': [3.0, 3.5, 4.0], 
        'beer_style': ['Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    output = pd.DataFrame(answers)
    assert isinstance(cd.omit_values(the_input, column, valuelist), pd.DataFrame)
    assert cd.omit_values(the_input, column, valuelist).shape[0] == 3
    assert output.equals(cd.omit_values(the_input, column, valuelist))

def test_omit_values_bad():
    """Tests the omit_values function for a bad path"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    the_input = pd.DataFrame(inputs)
    column = 'beer_styleOOPS'
    valuelist = ['Hefeweizen', 'English Strong Ale']
    try:
        cd.omit_values(the_input, column, valuelist)
        assert False
    except KeyError:
        assert True

def test_aggregated_category_column():
    """Tests the aggregated_category_column function"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    the_input = pd.DataFrame(inputs)
    narrowcolumn = 'beer_style'
    valuedict = {'BigBeer1': ['Hefeweizen','English Strong Ale', 'Foreign / Export Stout'], 'BigBeer2': ['German Pilsener', 'American Double / Imperial IPA']}  
    broadcategory = 'beer_type'
    answers = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA'],
        'beer_type': ['BigBeer1', 'BigBeer1', 'BigBeer1', 'BigBeer2', 'BigBeer2']}
    output = pd.DataFrame(answers)
    assert isinstance(cd.aggregated_category_column(the_input, narrowcolumn, valuedict, broadcategory), pd.DataFrame)
    assert output.equals(cd.aggregated_category_column(the_input, narrowcolumn, valuedict, broadcategory))

def test_aggregated_category_column():
    """Tests the aggregated_category_column function for a bad path"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    the_input = pd.DataFrame(inputs)
    narrowcolumn = 'beer_styleOOPS'
    valuedict = {'BigBeer1': ['Hefeweizen','English Strong Ale', 'Foreign / Export Stout'], 'BigBeer2': ['German Pilsener', 'American Double / Imperial IPA']}  
    broadcategory = 'beer_type'
    try:
        cd.aggregated_category_column(the_input, narrowcolumn, valuedict, broadcategory)
        assert False
    except KeyError:
        assert True
    
def test_select_rename_features():
    """Tests the select_rename_features function"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    the_input = pd.DataFrame(inputs)
    oldnames = ['brewery_id', 'review_overall', 'beer_style']
    newnames = ['Brewery', 'Review Overall', 'Beer Style']
    answers = {
        'Brewery': [10325, 10325, 10325, 10325, 1075],
        'Review Overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Beer Style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    output = pd.DataFrame(answers)
    assert cd.select_rename_features(the_input, oldnames, newnames).shape[1] == 3
    assert isinstance(cd.select_rename_features(the_input, oldnames, newnames), pd.DataFrame)
    assert output.equals(cd.select_rename_features(the_input, oldnames, newnames))

def test_select_rename_features_bad():
    """Tests the select_rename_features function for a bad path"""
    inputs = {
        'brewery_id': [10325, 10325, 10325, 10325, 1075],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'review_appearance': [2.5, 3.0, 3.0, 3.5, 4.0],
        'beer_style': ['Hefeweizen', 'English Strong Ale', 'Foreign / Export Stout', 'German Pilsener', 'American Double / Imperial IPA']}
    the_input = pd.DataFrame(inputs)
    oldnames = ['brewery_id', 'review_overall', 'beer_style']
    newnames = ['Brewery', 'Beer Style']
    try:
        cd.select_rename_features(the_input, oldnames, newnames)
        assert False
    except ValueError:
        assert True

def test_refine_data():
    """Tests the refine_data function"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    idcolname='Beer_ID'
    usercolname='Reviewer'
    n=3
    answers = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD']}
    output = pd.DataFrame(answers)
    assert cd.refine_data(the_input, idcolname, usercolname, n).shape[0] == 4
    assert isinstance(cd.refine_data(the_input, idcolname, usercolname, n), pd.DataFrame)
    assert output.equals(cd.refine_data(the_input, idcolname, usercolname, n))

def test_refine_data_bad():
    """Tests the refine_data function for a bad path"""
    inputs = {
        'Beer_ID': ['BeerA', 'BeerA', 'BeerA', 'BeerA', 'BeerB'],
        'review_overall' : [1.5, 3.0, 3.0, 3.0, 4.0],
        'Reviewer': ['ReviewerA', 'ReviewerB', 'ReviewerC', 'ReviewerD', 'ReviewerA']}
    the_input = pd.DataFrame(inputs)
    idcolname='Beer_IDOOPS'
    usercolname='Reviewer'
    n=3
    try:
        cd.refine_data(the_input, idcolname, usercolname, n)
        assert False
    except KeyError:
        assert True