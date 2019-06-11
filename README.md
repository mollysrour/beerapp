# Beer Recommender App!

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure AWS Credentials for S3 and RDS](#2-configure-aws-credentials-for-s3-and-rds)
  * [3. Data Pipeline](#3-data-pipeline)
  * [4. Launch App](#3-launch-app)
  

<!-- tocstop -->

## Project Charter 

**Vision**: To enable beer-novices and craft beer enthusiasts alike to discover new beers that fit their interests. The craft beer industry has been exploding over the last 10 years, and it could be considered daunting to try to navigate the huge variety in beer styles to find one that is appealing. Users will explore new beers and gain a greater appreciation of the options of beer available.  After visiting this app, users will be more likely to buy more beer and frequent a wider range of breweries.  Breweries can encourage customers to rate beers positively on the app so more users will be exposed to their beer.  

**Mission**: The app will be easy to navigate and will allow users to explore 10 diverse categories of beer and give targeted recommendations of specific beers in each category.  Users will choose a category, name beers they find appealing, and be compared to a database of over 1.5 million total reviews of beer to find their perfect brew. Their information, including a unique username, will be logged and included into the database to ensure accurate predictions in the future. Users can return and rate beers that were previously recommended to them and get a more accurate recommendation. Users who return to the same category of beer and request a new recommendation must rate the beers previously recommended to them first.  The addition of returning users' ratings will create a dynamically updatable dataset that will give more comprehensive recommendations as the userbase increases.

**Success criteria**:

Machine Learning Criteria: The main metric which will be used to evaluate app performance is **accuracy**. For first time users, an accuracy of 0.4 (2 of the 5 recommended beers) will be achieved. For second time users, we hope to achieve 0.6 accuracy and for third time users and above we will achieve 0.8 accuracy. We define a second time user as a user who has come back to the app and rated beers that were previously recommended to them. A user who visits the app once and gets recommendations for multiple categories of beer is still considered a first time user.  

Business Success Criteria:  The app will be considered successful from a business standpoint if 80% of first time users return to the app to log their ratings of their recommended beers and gain new recommendations.  Additionally, the app will be successful if 10,000 new users use the app in the first 3 months.  Users will need to specify a username to be added to the database, and this username will be used to track user return and userbase size.


## Backlog 

** means it will be completed in the next two weeks.

***Theme 1: Targeted Beer Recommendation System***

Business outcome for theme 1: App gives targeted recommendations based on individual tastes.

   **Epic 1: Data Organization and Cleaning**
   
   Story 1: Research and Data Cleaning- Research beer styles and evaluate whether all beers in the dataset can be categorized into one of the 11 broad categories. Beers that do not fit into any categories will be eliminated from the dataset. 1 point ** COMPLETED
   
   Story 2: Beer Categorization - Beer styles will be binned into 10 broad categories: Porter, Stout, Wheat Ale, IPA, Pale Ale, Sour Ale, Strong Ale, Dark Lager, Pilsner / Pale Lager, and Brown Ale. The dataset will be split into 11 smaller dataframes based on these category designations. The large (1.5 million rows, 1 row per review) dataset will become more manageable when broken down in this way, and users will pick a category and get recommendations on one category at a time. 2 points ** COMPLETED
   
   Story 3: Sparse Matrices -  Create sparse rating matrices (columns as users, rows as beers and values as rating), one for each beer              category. These will be the main datasets used for prediction. 2 Points** COMPLETED

   **Epic 2: Python-Based Model**: 
     
   Story 2: Introductory Model Building - create collaborative filtering recommendation system based on rating matrices using the Python package Scikit-Surprise. 4 points **
     
   Story 3: Test Model - Predict given sample users and estimate prediction accurracy. 2 Points **
     
   Story 4: User Input functions - refine prediction function to include user interface. 4 Points **
      
   Story 5: Unit Tests - QA testing on Python model. 8 Points **

***Theme 2: Model Communication with App and User Interface***

Business Outcome for Theme 2: App is easy to use and gives quick results to users.

  **Epic 1: S3 and RDS - Linking Model with App**
  
  Story 1: S3 - Put Model and Sparse Matrices in S3. 8 points
  
  Story 2: RDS - Put Database in RDS. 8 points
  
  Story 3: Configure Flask App. 8 points
  
  Story 4: Create YAML and MakeFile. 8 points
  
  **Epic 2: User Interface**
  
  Story 1: Use HTML and CSS to create user interface template. 4 points **
  
  Story 2: Use HTML and CSS to create buttons for separate categories, link to interface for separate categories. 4 points

***Theme 3: Dynamically Updatable Dataset***
Business Outcome for Theme 3: Users can come back to the app and rate beers that were previously recommended.  

**Epic 1: S3 and RDS**

Story 1: Use S3 and RDS to store user information and recommendations so they can rate previously recommended beers. 8 points

## Icebox

***Theme 1: GPS Locator of Recommended Beers***
Business value: Users can find where a beer is that has been recommended. 8 points

**Epic 1: Link to Beer Locator Website**

**Epic 2: Link to Description of Beer on Brewery Website**

## Repo structure 

```
├── README.md                         <- You are here
├── data                              <- Folder that contains data used or generated. 
├── deliverables                      <- Folder that contains deliverables for AVC project
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
├── src                               <- Source data for the project 
│   ├── config.yml                    <- Configuration file for model pipeline
|   ├── acquire_data.py               <- Script for getting data from my S3 bucket to your S3 bucket and finally to your local path
|   ├── clean_data.py                 <- Script for cleaning data
|   ├── train_model.py                <- Script for training model on 450 different test users and creating predictions, top 10 beers for each beer type, and test user combinations
|   ├── score_model.py                <- Script for scoring model performance on a subset of the data
│   ├── configure_db.py               <- Script for creating db in RDS or Sqlite and adding rows from the three tables
│   ├── getdata_s3.py                 <- Script for getting source data from my S3 bucket and landing it in your S3 bucket
│   ├── test_clean_data.py            <- Unit tests of the clean_data script
│   ├── test_train_model.py           <- Unit tests of the train_model script
│   ├── test_score_model.py           <- Unit tests of the score_model script
├── static                            <- Static CSS folder
│   ├── basic.css                     <- CSS for the app
├── templates                         <- HTML templates for the app
│   ├── first.html                    <- HTML Landing page for the app, user chooses type
│   ├── recommender.html              <- HTML page where user inputs beers they like from top ten list
│   ├── results.html                  <- HTML page where user receives results
├── application.py                    <- Script for running the Flask application
├── flask_config.py                   <- Configurations for Flask app
├── Makefile                          <- File to link together and create necessary files, models, etc 
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Running the application 

#### If you do not have pip on your computer:

```bash

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

```
#### Once pip is installed:

### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv beerapp

source beerapp/bin/activate

```
#### With `conda`

```bash
conda create -n beerapp python=3.7
conda activate beerapp

```

Then you must install the required python packages, which are stored in the requirements.txt file. 

However, due to an issue with the surprise package, you will need to install numpy first separately.

Documented here: https://github.com/NicolasHug/Surprise/issues/188

Please run this first:

```bash
pip install numpy
```

Then run thic command:

```bash
pip install -r requirements.txt
```

### 2. Configure AWS Credentials for S3 and RDS

1.  Set your AWS environment variables by running the following commands, entering your AWS key and secret key, all must be in quotes:
    ```bash
    export AWS_KEY_ID=""
    export AWS_ACCESS_KEY=""
    
    ```

2.  If you are using RDS, set your RDS MYSQL environment variables by running the following commands, entering your relevant RDS info, all must be in quotes:
    ```bash
    export MYSQL_USER=""
    export MYSQL_PASSWORD=""
    export MYSQL_HOST=""
    export MYSQL_PORT=""
    ```
  Additionally, if you are using RDS, also run this command:
  
  ```bash
  export localorRDS="RDS"
  ```
  If you are NOT using RDS and are configuring the app locally, run the following command:
  
  ```bash
  export localorRDS="local"
  ```
    
### 3. Data Pipeline
Change the configurations in `src/config.yml` to your desired configurations. Mandatory changes include:

  Within the acquire_data section of the config, change AWS_BUCKET to the name of your AWS bucket, change AWS_FILE_PATH to the file path within your bucket that you would like the raw data to be landed, and change localfilepath to the filepath in your local folder you would like the raw data to be landed.
  Within the configure_db section of the config, if you are configuring the app locally, you must change SQLITELOCALENGINE to the appropriate path for the SQLite database. This MUST be of the format 'sqlite:///filepath/databasename.db' . For example, if you are in your beerapp folder and wish the db to be stored in the data folder as beers.db, then the appropriate format of the SQLITELOCALENGINE is 'sqlite:///data/beers.db'.  If you are using RDS, you must configure MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB, and MYSQL_SQLTYPE to your appropriate RDS settings.

Go into the makefile and change the data paths appropriately to where you would like the data to be stored.
   
Run  `make all`

### 4. Launch App

`flask_config.py` holds the configurations for the Flask app. If you are configuring the app locally, you must change the SQLALCHEMY_DATABASE_URI to the same path that you specified in SQLITELOCALENGINE in the config for your database. If you are configuring the app using RDS, you should not need to change anything in flask_config.py since the os environment variables are used.  HOWEVER, if your database is not called msia423 and your connection type is not mysql+pymysql, you must change those to their appropriate settings within flask_config.py.

Run `python application.py`
