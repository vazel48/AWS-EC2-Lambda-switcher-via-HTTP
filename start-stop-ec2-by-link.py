import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-central-1')  # Регіон зашитий у коді
    instance_id = 'i-0123456789abcdef0'  # Залишаємо інстанс ID у коді

    # Отримуємо шлях (route path) із події
    path = event.get('rawPath', '')

    if path == '/start':
        action = 'start'
    elif path == '/stop':
        action = 'stop'
    elif path == '/status':
        action = 'status'
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid action. Use "/start", "/stop", or "/status".')
        }

    try:
        # Отримуємо поточний статус інстансу
        current_status = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]['State']['Name']
        logger.info(f'Current status of instance {instance_id}: {current_status}')

        if action == 'start':
            if current_status == 'stopped':
                ec2.start_instances(InstanceIds=[instance_id])
                logger.info(f'Starting instance {instance_id}.')
                return {
                    'statusCode': 200,
                    'body': json.dumps(f'Instance {instance_id} started successfully.')
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps(f'Instance {instance_id} is already in state {current_status}.')
                }

        elif action == 'stop':
            if current_status == 'running':
                ec2.stop_instances(InstanceIds=[instance_id])
                logger.info(f'Stopping instance {instance_id}.')
                return {
                    'statusCode': 200,
                    'body': json.dumps(f'Instance {instance_id} stopped successfully.')
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps(f'Instance {instance_id} is already in state {current_status}.')
                }

        elif action == 'status':
            # Повертаємо поточний статус інстансу
            return {
                'statusCode': 200,
                'body': json.dumps(f'Instance {instance_id} is currently in state {current_status}.')
            }

    except Exception as e:
        logger.error(f'Error managing instance: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error managing instance: {str(e)}')
        }
