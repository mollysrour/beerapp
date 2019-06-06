import argparse
import logging
import boto3
import yaml
import os

def sourcetoS3(AWS_KEY_ID=None, AWS_ACCESS_KEY=None, AWS_BUCKET=None, AWS_FILE_PATH='/beer_reviews.csv'):
    """Takes data from source (S3) and lands it in a bucket specified in config.
   Arguments:
       AWS_KEY_ID {str} -- AWS access key id
       AWS_ACCESS_KEY {str} -- AWS secret access key id
       AWS_BUCKET {str} -- AWS S3 bucket name. Should be just the name; does not need to begin with s3://
       AWS_FILE_PATH {str} -- File path for data within S3 bucket. (Default: {'/beer_reviews.csv'})
   """
    try:
        s3 = boto3.resource('s3', aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY)
    except:
        logger.error('Incorrect AWS credentials. Please re-enter them by running the EXPORT commands in the command line')
    copy_source = {'Bucket': 'beer-recommenderapp', 'Key': 'raw_data_source/beer_reviews.csv'}
    try:
        s3.meta.client.copy(copy_source, AWS_BUCKET, AWS_FILE_PATH)
        logger.info('Successfully landed source data in S3 bucket %s', AWS_BUCKET)
    except:
        logger.error('Incorrect AWS Bucket name. Please re-enter it in config.yml')
    
def S3tolocal(AWS_KEY_ID=None, AWS_ACCESS_KEY=None, AWS_BUCKET=None, AWS_FILE_PATH='beer_reviews.csv', localfilepath='data/beer_reviews.csv'):
    """Takes data from bucket specified in config and lands it in local.
   Arguments:
       AWS_KEY_ID {str} -- AWS access key id
       AWS_ACCESS_KEY {str} -- AWS secret access key id
       AWS_BUCKET {str} -- AWS S3 bucket name. Should be just the name; does not need to begin with s3://
       AWS_FILE_PATH {str} -- File path for data within S3 bucket. (Default: {'beer_reviews.csv'})
   """
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY)
    except:
        logger.error('Incorrect AWS credentials. Please re-enter them by running the EXPORT commands in the command line')
    try:
        s3.download_file(AWS_BUCKET, AWS_FILE_PATH, localfilepath)
        logger.info('Successfully landed source data in S3 bucket %s', AWS_BUCKET)
    except:
        logger.error('Incorrect AWS Bucket name or filepath name. Please re-enter it in config.yml')    
    
def run_acquire(args):
    """Runs script to acquire data.
    
    Arguments:
        args {argparse.Namespace} -- Script arguments, in this case, path to config file.
    
    Raises:
        ValueError: "Path to config yml file must be provided through --config" if args.config not specified
    """
    if args.config is not None:
        with open(args.config, "r") as f:
	        config = yaml.load(f)
        config = config['acquire_data']
    else:
        raise ValueError("Path to config yml file must be provided through --config")
    AWS_KEY_ID = os.environ.get('AWS_KEY_ID')
    if AWS_KEY_ID is not None:
        AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    else:
        logger.error('Enter your AWS Key ID in the environment using EXPORT.')
    if AWS_ACCESS_KEY is not None:
        sourcetoS3(AWS_KEY_ID, AWS_ACCESS_KEY, **config['sourcetoS3'])
        S3tolocal(AWS_KEY_ID, AWS_ACCESS_KEY, **config['S3tolocal'])
    else:
        logger.error('Enter your AWS Secret Access key in the environment using EXPORT.')
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
    logger = logging.getLogger(__file__)
    parser = argparse.ArgumentParser(description="Add config.yml in args")
    parser.add_argument('--config', default='config.yml')
    args = parser.parse_args()
    run_acquire(args)
    