import json
from test_handler import test_handler
from linebot_agent import bot_lambda_handler


def lambda_handler(event, context):
    bot_lambda_handler(event, context)
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps(
    #         {
    #             "message": test_handler(),
    #         }
    #     ),
    # }
