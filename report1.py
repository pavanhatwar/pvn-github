import boto3
import csv
from datetime import datetime, timedelta
import time










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


time.sleep(5)
session = boto3.Session(profile_name=a  )
client = session.client('ec2', region_name='us-east-2')
ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
with open( 'file.csv','w') as csvfile:
    fieldnames = ['Sr.N', 'Region', 'InstanceId', 'Name-Tag', 'InstanceType', 'State', 'Timestamp', 'AVG-CPU', 'Timestamp', 'MIN-CPU', 'Timestamp',
                  'MAX-CPU', 'Timestamp', 'AVG-N-IN(kb)', 'Timestamp', 'MIN-N-IN(kb)',  'Timestamp','MAX-N-IN(kb)', 'Timestamp', 'AVG-N-OUT(kb)', 'Timestamp', 'MIN-N-OUT(kb)', 'Timestamp', 'MAX-N-OUT(kb)', 'Timestamp', 'Mem-used(MB)', 'Timestamp', 'Mem-avail(MB)',  'Timestamp','Mem-uti(MB)', 'Timestamp','Disksp-uti(MB)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    dict = {'Sr.N': '', 'Region': '', 'InstanceId': '', 'Name-Tag': '', 'InstanceType': '', 'State': '', 'Timestamp': '', 'AVG-CPU': '', 'Timestamp': '', 'MIN-CPU': '', 'Timestamp': '',
            'MAX-CPU': '', 'Timestamp': '', 'AVG-N-IN(kb)': '', 'Timestamp': '', 'MIN-N-IN(kb)': '', 'Timestamp': '',
            'MAX-N-IN(kb)': '', 'Timestamp': '', 'AVG-N-OUT(kb)': '', 'Timestamp': '', 'MIN-N-OUT(kb)': '', 'Timestamp': '', 'MAX-N-OUT(kb)': '', 'Timestamp': '', 'Mem-used(MB)': '', 'Timestamp': '', 'Mem-avail(MB)': '', 'Timestamp': '',
             'Mem-uti(MB)': '', 'Timestamp': '', 'Disksp-uti(MB)': ''}
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
                dict['InstanceId'] = a
                dict['InstanceType'] = b
                dict['State'] = c
                dict['Timestamp'] = 0
                dict['AVG-CPU'] = 0
                dict['MIN-CPU'] = 0
                dict['MAX-CPU'] = 0
                dict['AVG-N-IN(kb)'] = 0
                dict['MIN-N-IN(kb)'] = 0
                dict['MAX-N-IN(kb)'] = 0
                dict['AVG-N-OUT(kb)'] = 0
                dict['MIN-N-OUT(kb)'] = 0
                dict['MAX-N-OUT(kb)'] = 0
                dict['Name-Tag'] = z
                dict['Mem-used(MB)'] = 0
                dict['Mem-avail(MB)'] = 0
                dict['Mem-uti(MB)'] = 0
                dict['Disksp-uti(MB)'] = 0


########MetricsAVErage cpu

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Average'],
                    Unit='Percent'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        p = cpu["Timestamp"]
                        print(p)
                        dict['Timestamp'] = p
                    if 'Average' in cpu:
                        k = cpu['Average']
                        dict['AVG-CPU'] = k
                    else:
                        dict['AVG-CPU'] = 0
                    writer.writerow(dict)

########Metrics Minimum cpu

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Minimum'],
                    Unit='Percent'
                )
                print('\n')
                print(response)
                print('\n')

                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        q = cpu["Timestamp"]
                        print()
                        dict['Timestamp'] = q
                    if 'Minimum' in cpu:
                        k = cpu['Minimum']
                        dict['MIN-CPU'] = k
                    else:
                        dict['MIN-CPU'] = 0
                    writer.writerow(dict)
########Metrics Maximum cpu

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='CPUUtilization',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Maximum'],
                    Unit='Percent'
                )
                print('\n')

                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        r = cpu["Timestamp"]
                        print(r)
                        dict['Timestamp'] = r
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']

                        dict['MAX-CPU'] = k
                    else:
                        dict['MAX-CPU'] = 0
                    writer.writerow(dict)
#######Metrics   AVErage NetworkIn

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='NetworkIn',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Average'],
                    Unit='Bytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        o = cpu["Timestamp"]
                        print(o)
                        dict['Timestamp'] = o
                    if 'Average' in cpu:
                        k = cpu['Average']
                        print(k)

                        dict['AVG-N-IN(kb)'] = k
                    else:
                        dict['AVG-N-IN(kb)'] = 0
                    writer.writerow(dict)
######Metrics  Minimum NetworkIn

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='NetworkIn',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Minimum'],
                    Unit='Bytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        s = cpu["Timestamp"]
                        print(s)
                        dict['Timestamp'] = s
                    if 'Minimum' in cpu:
                        k = cpu['Minimum']
                        print(k)
                        dict['MIN-N-IN(kb)'] = k
                    else:
                        dict['MIN-N-IN(kb)'] = 0
                    writer.writerow(dict)
######Metrics  Maximum Networkin

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='NetworkIn',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Maximum'],
                    Unit='Bytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        t = cpu["Timestamp"]
                        print(t)
                        dict['Timestamp'] = t
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['MAX-N-IN(kb)'] = k
                    else:
                        dict['MAX-N-IN(kb)'] = 0

                    writer.writerow(dict)
######Metrics  Average NetworkOut

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='NetworkOut',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Average'],
                    Unit='Bytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        u = cpu["Timestamp"]
                        print(u)
                        dict['Timestamp'] = u
                    if 'Average' in cpu:
                        k = cpu['Average']
                        print(k)

                        dict['AVG-N-OUT(kb)'] = k
                    else:
                        dict['AVG-N-OUT(kb)'] = 0
                    writer.writerow(dict)

######Metrics  Minimum NetworkOut

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='NetworkOut',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Maximum'],
                    Unit='Bytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        v = cpu["Timestamp"]
                        print(v)
                        dict['Timestamp'] = v
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['MIN-N-OUT(kb)'] = k
                    else:
                        dict['MIN-N-OUT(kb)'] = 0

                    writer.writerow(dict)
######Metrics  Maximum NetworkOut

                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='AWS/EC2',
                    MetricName='NetworkOut',
                    Dimensions=[
                        {
                            'Name': 'InstanceId',
                            'Value': a
                        },
                    ],
                    StartTime=datetime(year, month, day),
                    EndTime=datetime(year2, month2, day2),
                    Period=granularity,
                    Statistics=['Maximum'],
                    Unit='Bytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        w = cpu["Timestamp"]
                        print(w)
                        dict['Timestamp'] = w
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['MAX-N-OUT(kb)'] = k
                    else:
                        dict['MAX-N-OUT(kb)'] = 0

                    writer.writerow(dict)
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
                        dict['Mem-uti(MB)'] = k
                    else:
                        dict['Mem-uti(MB)'] = 0

                    writer.writerow(dict)

######Metrics MemoryUsed
                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='System/Linux',
                    MetricName='MemoryUsed',
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
                    Unit='Megabytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        y = cpu["Timestamp"]
                        print(y)
                        dict['Timestamp'] = y
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['Mem-used(MB)'] = k
                    else:
                        dict['Mem-used(MB)'] = 0
                    writer.writerow(dict)


#####Metrics MemoryAvailable
                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='System/Linux',
                    MetricName='MemoryAvailable',
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
                    Unit='Megabytes'
                )
                print('\n')
                print(response)
                print('\n')
                for cpu in response['Datapoints']:
                    if 'Timestamp' in cpu:
                        z = cpu["Timestamp"]
                        print(z)
                        dict['Timestamp'] = z
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['Mem-avail(MB)'] = k
                    else:
                        dict['Mem-avail(MB)'] = 0
                    writer.writerow(dict)
#####Metrics DiskUtilization
                client = boto3.client('cloudwatch')
                response = client.get_metric_statistics(
                    Namespace='System/Linux',
                    MetricName='DiskSpaceUtilization',
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
                        n = cpu["Timestamp"]
                        print(n)
                        dict['Timestamp'] = n
                    if 'Maximum' in cpu:
                        k = cpu['Maximum']
                        print(k)
                        dict['Disksp-uti(MB)'] = k
                    else:
                        dict['Disksp-uti(MB)'] = 0

                    writer.writerow(dict)



                writer.writerow(dict)
                print('\n')
print("success")
