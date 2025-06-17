def handler(request, context):
    """
    Simple test endpoint to verify serverless function is working
    """
    return {
        'statusCode': 200,
        'body': 'Hello from Vercel serverless function!',
        'headers': {'Content-Type': 'text/plain'}
    }

app = handler 