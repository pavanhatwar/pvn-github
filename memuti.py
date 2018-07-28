import boto3
import csv
from datetime import datetime, timedelta
import time
import json









time.sleep(1)

dict = {}
num = 0
print('\n')
print('\033[5419;30;47m\t\t\t\t****<<< Enter the Details for the Report creation >>>****                                              \033[1;m')

print('\033[1;31m\n Enter the specified profile from the list :\n\n 1 - default \n 2 - pavan \n\n\033[1;m')
a =raw_input("Type profile_name : ")



time.sleep(1)
print('\n')
print('\033[1;32m\t\t$$$....Enter the starting date from....$$$ :\033[1;m')
time.sleep(1)
print('\n')
year = int(input("###....Enter the year (allowed* <4digit>)....### : "))
#time.sleep(2)
#print('\n')
month = int(input("###....Enter the month. (allowed* <1-12>)....### : "))
#time.sleep(2)
#print('\n')
day = int(input("###....Enter the day (allowed* <1-31>)........###    : "))
#time.sleep(2)
print('\n')
print('\033[1;32m\t\t$$$....Enter the ending date to....$$$ :\033[1;m')
time.sleep(1)
print('\n')
year2 = int(input("###....Enter the year (allowed* <4digit>)....### : "))
#time.sleep(2)
#print('\n')
month2 = int(input("###....Enter the month (allowed* <1-12>)....###  : "))
#time.sleep(2)
#print('\n')
day2 = int(input("###....Enter the day (allowed* <1-31>)....###    : "))
time.sleep(2)
print('\n')
print('\033[1;32m\t\t$$$....Enter the Granularitu....$$$ :\033[1;m')
print("\n")
granularity = int(input("###....Granularity allowed <mult of 60*>....### : "))
time.sleep(2)
print('\n')
#time.sleep(2)

print("\033[1;33mYou Entered the following Details : \n\t  \033[1;m")
print("\033[1;34m\n\tProfile Name : \033[1;m",str(a))
print("\033[1;34m\tStartdate From : \033[1;m " ,+day ,"/",+month ,"/",+year )
print("\033[1;34m\tEnding date to : \033[1;m",+day2,"/",+month2,"/",+year2 )
print("\033[1;34m\tGranularity    : \033[1;m",+granularity)
print("\n")

y = int(input('\033[1;31mTo continue press "1" or "0" for exit  : \033[1;m'))
if y == 1:
    print("\033[1;36m\n\t\tNow a Report will generate  : file \033[1;m")
else:
    exit()
time.sleep(2)
session = boto3.Session(profile_name=a  )
client = session.client('ec2', region_name='us-east-2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
with open( 'file.csv','w') as csvfile:
    fieldnames = ['Sr.N', 'Region','Name-Tag', 'InstanceId', 'InstanceType', 'State', 'Timestamp', 'MemoryUtilization']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    dict = {'Sr.N': '', 'Region': '', 'Name-Tag': '', 'InstanceId': '', 'InstanceType': '', 'State': '', 'Timestamp': '',
            'MemoryUtilization': ''}
    writer.writeheader()
    for region in ec2_regions:
        client = session.client('ec2', region_name=region)
        response = client.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                a = instance["InstanceId"]
                b = instance["InstanceType"]
                c = instance["State"]["Name"]
                for tags in instance["Tags"]:
                    z = tags["Value"]

                print('\n')
                print(a, b, region, c)
                print('\n')
                dict['Sr.N'] = num = num + 1
                dict['Region'] = region
                dict['Name-Tag'] = z
                dict['InstanceId'] = a
                dict['InstanceType'] = b
                dict['State'] = c
                dict['Timestamp'] = 0
                dict['MemoryUtilization'] = 0






######Metrics MemoryUtilization
                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='System/Linux',
                    MetricName='MemoryUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),



                    #StartTime=datetime(2018, 6, 29) - timedelta(seconds=600),
                #    EndTime=datetime(2018, 6, 30),
                    Period=granularity,
                    Statistics=['Maximum'],
                    Unit='Percent'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        x = cpu["Timestamp"]
                        print(x)
                        dict['Timestamp'] = x
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['MemoryUtilization'] = k
                    else:
                        dict['MemoryUtilization'] = 0

                    writer.writerow(dict)


                writer.writerow(dict)
                print('\n')
print("success")
