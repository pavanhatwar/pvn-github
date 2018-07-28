import boto3
import csv
from datetime import datetime, timedelta
session = boto3.Session()
client = session.client('rds', region_name='ap-south-1')
ec2_regions = [region['ap-south-1'] for region in client.describe_regions()['ap-south-1']]
for region in ec2_regions:
    client = session.client('rds', region_name=region)
    response = client.describe_db_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            a = instance["InstanceId"]
            print(a)

            client = boto3.client('cloudwatch')
            response = client.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'InstanceId',
                        'Value': a
                    },
                ],
                StartTime=datetime(2018, 7, 14) - timedelta(seconds=600),
                EndTime=datetime(2018, 7, 17),
                Period=259200,
                Statistics=['Maximum'],
                Unit='Percent'
            )

            for cpu in response['Datapoints']:
                if 'Timestamp' in cpu:
                    k = cpu["Timestamp"]
                    print(k)
