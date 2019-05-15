import boto3
import config

def sourcetoS3():
    """Takes data from source (S3) and lands it in a bucket specified in config."""
    s3 = boto3.resource('s3', aws_access_key_id=config.AWS_KEY_ID,
        aws_secret_access_key=config.AWS_ACCESS_KEY)
    copy_source = {'Bucket': 'beer-recommenderapp', 'Key': 'raw_data_source/beer_reviews.csv'}
    s3.meta.client.copy(copy_source, config.AWS_BUCKET, config.AWS_FILE_PATH)

if __name__ == "__main__":

    sourcetoS3()