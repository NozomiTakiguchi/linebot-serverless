import json
from test import Test


def lambda_handler(event, context):

    t = Test()
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": t.message,
            }
        ),
    }
