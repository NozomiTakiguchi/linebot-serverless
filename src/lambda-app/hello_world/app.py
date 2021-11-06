import json
# from ...linebot_agent import lambda_handler as handler

def lambda_handler(event, context):
    # handler(event, context)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
