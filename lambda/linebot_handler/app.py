import json
from test_handler import test_handler


def lambda_handler(event, context):

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": test_handler(),
            }
        ),
    }
