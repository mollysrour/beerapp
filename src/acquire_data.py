import boto3
import argparse
import yaml
import logging

def sourcetoS3(AWS_KEY_ID=None, AWS_ACCESS_KEY=None, AWS_BUCKET=None, AWS_FILE_PATH='beer_reviews.csv'):
    """Takes data from source (S3) and lands it in a bucket specified in config.
   Arguments:
       AWS_KEY_ID {str} -- AWS access key id
       AWS_ACCESS_KEY {str} -- AWS secret access key id
       AWS_BUCKET {str} -- AWS S3 bucket name. Should be just the name; does not need to begin with s3://
       AWS_FILE_PATH {str} -- File path for data within S3 bucket. (Default: {'beer_reviews.csv'})
   """
    s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY)
    copy_source = {'Bucket': 'beer-recommenderapp', 'Key': 'raw_data_source/beer_reviews.csv'}
    s3.meta.client.copy(copy_source, AWS_BUCKET, AWS_FILE_PATH)

def S3tolocal(AWS_KEY_ID=None, AWS_ACCESS_KEY=None, AWS_BUCKET=None, AWS_FILE_PATH='beer_reviews.csv', localfilepath='../data/beer_reviews.csv'):
    """Takes data from bucket specified in config and lands it in local.
   Arguments:
       AWS_KEY_ID {str} -- AWS access key id
       AWS_ACCESS_KEY {str} -- AWS secret access key id
       AWS_BUCKET {str} -- AWS S3 bucket name. Should be just the name; does not need to begin with s3://
       AWS_FILE_PATH {str} -- File path for data within S3 bucket. (Default: {'beer_reviews.csv'})
   """
    s3 = boto3.client('s3', aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY)
    s3.download_file(AWS_BUCKET, AWS_FILE_PATH, localfilepath)

def run_acquire(args):
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['acquire_data']
    else:
        raise ValueError("Path to CSV for input data must be provided through --input")
    sourcetoS3(**config['sourcetoS3'])
    logger.info('Successfully transferred data to S3 bucket %s', config['sourcetoS3']['AWS_BUCKET'])
    S3tolocal(**config['S3tolocal'])
    logger.info('Successfully transferred data to local file %s', config['S3tolocal']['localfilepath'])

if __name__ == "__main__":
    logging.basicConfig(filename='beerapp_logs.log', filemode='a', level=logging.DEBUG, 
    format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml', help='config.yml')
    args = parser.parse_args()

    run_acquire(args)
    