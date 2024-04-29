def lambda_handler(event, context):
    # Your code here
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }