import boto3
from os import environ
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

secret_id = environ['SLACK_WEBHOOK_SECRET_ID']
client = boto3.client('secretsmanager')
slack_webhook_url = client.get_secret_value(SecretId=secret_id)['SecretString']


def send_message(context, msg):
    message = SlackWebhookOperator(
        webhook_token=slack_webhook_url,
        message=msg,
        task_id=context['task_instance'].task_id
    )
    return message.execute(context=context)


def failure_callback(context):
    owners = str(context['dag'].owner).split(',')
    ats = ''.join([f'<@{owner}> ' for owner in owners])
    msg = f"""Task Failed.\n
Dag: {context['task_instance'].dag_id}
Task: {context['task_instance'].task_id}
Execution Time: {context['execution_date']}
<{context['task_instance'].log_url}|View Log>
{ats}
"""
    send_message(context, msg)
