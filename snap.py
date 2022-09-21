import boto3
import time
import sys
 
def lambda_handler(event, context):
ec2Regions = boto3.client('ec2')
awsRegions = ec2Regions.describe_regions()['Regions']
for region in awsRegions:
rds = boto3.client('rds',region_name=region['RegionName'])
try:
current_date = time.strftime("%Y-%m-%d-%H-%M-%S")
print (current_date)
print (region)
response = rds.describe_db_instances()
try:
for rdsinstance in response['DBInstances']:
if (rdsinstance['DBInstanceStatus']=='available'): 
try:
shotIdentifier = rdsinstance['DBInstanceIdentifier'].replace('_','-') + current_date
rds.create_db_snapshot(DBInstanceIdentifier = rdsinstance['DBInstanceIdentifier'],DBSnapshotIdentifier = shotIdentifier)
except Exception as e:
print ('Error::%s'%e)
else:
print ('Instance NOT available Instance State is %s and Engine is %s'%(rdsinstance['DBInstanceStatus'],rdsinstance['Engine']))
except Exception as e:
print ('Error::%s'%e)
except Exception as e:
print (e)
#lambda_handler(None,None)
