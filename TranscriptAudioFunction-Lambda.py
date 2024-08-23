import boto3
import urllib.parse
import json
import re
import time

def lambda_handler(event, context):
    # Initialize AWS services
    transcribe = boto3.client('transcribe')
    s3 = boto3.client('s3')

    try:
        # Get the bucket and object key from the event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
        
        # Generate a safe and unique job name by replacing invalid characters and adding a timestamp
        base_job_name = re.sub(r'[^0-9a-zA-Z._-]', '_', key.split('.')[0])  # Replace invalid characters
        timestamp = int(time.time())  # Current Unix timestamp
        job_name = f"{base_job_name}_{timestamp}"  # Append timestamp to ensure uniqueness
        job_uri = f's3://{bucket}/{key}'

        # Debugging: Print debug information
        print(f"Bucket: {bucket}")
        print(f"Key: {key}")
        print(f"Job Name: {job_name}")
        print(f"Job URI: {job_uri}")

        # Start transcription job
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp3',  # Specify the format of the media file (e.g., mp3, wav, etc.)
            LanguageCode='en-US',  # Specify the language code (e.g., en-US for English)
            OutputBucketName='podcast-transcript-results-bucket'  # Specify the output bucket
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Transcription job started successfully',
                'jobName': job_name,
                'response': response  # Ensure that the response is serialized
            }, default=str)  # Use default=str to handle non-serializable objects
        }
    except Exception as e:
        # Handle serialization of error message
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed to start transcription job',
                'error': str(e)  # Ensure that any exception is converted to a string
            }, default=str)  # Use default=str to handle non-serializable objects
        }
