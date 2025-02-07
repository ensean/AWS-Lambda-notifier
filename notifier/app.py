import boto3
import os

from dingtalk import DingTalk
from alarm import Alarm

secretArn = os.environ['SECRET_ARN']

# Get chat bot URL includes token from Secrets Manager
secret_manager_client = boto3.client('secretsmanager')
get_secret_value_response = secret_manager_client.get_secret_value(
        SecretId=secretArn
    )
secretURL = get_secret_value_response['SecretString']

# Initial DingTalk handler
dingtalk=DingTalk(secretURL)

def lambda_handler(event, context):
    print(event)
    msg = msg_format(event)
    print(msg)

    dtAlarm = Alarm(

        description=msg,
    )

    dingtalk.send_text_msg(dtAlarm)

    response = {
        "statusCode": 200,
        "body": "Message Sent."
    }

    return response

def msg_format(event):
    try:
        #消息来源是SNS，取 $.Records[0].Sns.Message，并对字符串进行一些处理，确保发送时可以正常显示
        msg = event['Records'][0]['Sns']['Message']

        #进行字符串处理后返回，以确保IM客户端正确显示
        msg = msg.replace("\\n", "\n")
        if msg[0] == '\"' and msg[-1] == '\"' :
            msg = msg[1:-1]

        return msg
    except:
        #消息来源不是SNS，直接返回
        return event