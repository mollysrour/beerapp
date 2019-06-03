data/beer_reviews.csv: src/acquire_data.py src/config.yml
	python src/acquire_data.py --config=src/config.yml

raw_data: data/beer_reviews.csv

data/cleaned_beer_reviews.csv: data/beer_reviews.csv src/clean_data.py src/config.yml 
	python src/clean_data.py --config=src/config.yml --input=‘data/beer_reviews.csv' --output=‘data/cleaned_beer_reviews.csv'

cleaned_data: cleaned_beer_reviews.csv

preds.csv: data/cleaned_beer_reviews.csv src/train_model.py src/config.yml
	python src/train_model.py --config=src/config.yml --input='data/cleaned_beer_reviews.csv' --output_preds='data/preds.csv' --output_top10rows='data/top10.csv' --output_combinations='data/combinations.csv'

trained_model: preds.csv

modelscoring.txt: data/cleaned_beer_reviews.csv src/config.yml
	python src/score_model.py --config=src/config.yml --input='data/cleaned_beer_reviews.csv' --outputtxt='data/modelscoring.txt'

model_scoring: modelscoring.txt

beers.db: data/preds.csv data/top10.csv data/combinations.csv src/configure_db.py src/config.yml
	python src/configure_db.py --config=src/config.yml --input_preds='data/preds.csv' --input_top10rows='data/top10.csv' --input_combinations='data/combinations.csv'

configure_db: beers.db

all: raw_data cleaned_data trained_model model_scoring configure_db




