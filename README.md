# airflow-slack-webhook
- [Create](https://api.slack.com/messaging/webhooks) a slack app with channel and incoming webhook.
- Place the slack webhook url in plaintext in your secrets manager secret with the following format:
```
https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/abcdefghijklmnopqrstuvwx
```
- Populate the environment variable for SLACK_WEBHOOK_SECRET_ID with your secret id.
- Put slack_webhook.py in your $AIRFLOW_HOME/plugins folder
- if you wish to @ the owner of the dag populate the owner argument with the slack username(s).

example:
```python
from slack_webhook import failure_callback
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'slack.username'
}

dag = DAG('test_slack_alert')

fail_task = BashOperator(
    task_id='fail_task',
    bash_command='exit 1',
    on_failure_callback=failure_callback,
    default_args=default_args,
    dag=dag,
)
```

<img src="https://github.com/GregoryWiltshire/airflow-slack-webhook/blob/main/callback.jpg?raw=true" alt="drawing" width="500"/>
 
