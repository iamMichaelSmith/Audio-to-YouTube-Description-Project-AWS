import json
import boto3
import os

# Initialize AWS services
s3 = boto3.client('s3')
bedrock = boto3.client('bedrock')  # Ensure Amazon Bedrock client is properly set up

def lambda_handler(event, context):
    try:
        # Check if 'Records' key is present
        if 'Records' not in event:
            raise ValueError("Missing 'Records' in event")

        # Extract the S3 bucket name and object key from the event triggered by the transcription file upload
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        # Ignore .temp files
        if object_key.endswith('.temp') or object_key.endswith('.tmp'):
            print(f"Ignoring temporary file: {object_key}")
            return {
                'statusCode': 200,
                'body': json.dumps('Temporary file ignored.')
            }

        # Retrieve the transcription JSON file from S3
        transcription_object = s3.get_object(Bucket=bucket_name, Key=object_key)
        transcription_content_type = transcription_object['ContentType']

        # Check if the content type is JSON
        if transcription_content_type != 'application/json':
            raise ValueError(f"Unexpected content type: {transcription_content_type}. Expected 'application/json'.")

        transcription_text = transcription_object['Body'].read().decode('utf-8')

        # Generate the prompt to send to Claude 3 Sonnet via Bedrock
        prompt = f"Generate a YouTube bio that highlights the main topics and keywords from the following podcast transcript:\n\n{transcription_text}"

        # Call the Bedrock API with Claude 3 Sonnet model
        response = bedrock.invoke_model(
            modelId='claude-3-sonnet',  # Use the correct model ID for Claude 3 Sonnet
            body={
                'prompt': prompt,
                'max_tokens_to_sample': 150,  # Adjust based on required response length
                'temperature': 0.7  # Control creativity level
            }
        )
        
        # Extract the generated YouTube bio from the response
        youtube_bio = response.get('completion', 'No completion found')

        # Define the S3 bucket and key to store the generated YouTube bio
        output_bucket_name = 'podcast-youtube-description-bucket'  # Updated destination bucket name
        output_key = f'bios/{os.path.splitext(object_key)[0]}_youtube_bio.txt'

        # Save the generated bio to the output S3 bucket
        s3.put_object(Bucket=output_bucket_name, Key=output_key, Body=youtube_bio)

        return {
            'statusCode': 200,
            'body': json.dumps('YouTube bio generated and stored successfully!')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error processing the file',
                'error': str(e)
            })
        }
