
import boto3
import operator

ACCOUNT = '760154870506'


def copy_latest_snapshot():
    client = boto3.client('rds', 'us-east-1')
    uat_client = boto3.client('rds', 'us-east-1')
    
    response = client.describe_db_snapshots(
          DBInstanceIdentifier='mysqltestdb',
          SnapshotType='manual',
          IncludeShared=False,
          IncludePublic=False
          )

    if len(response['DBSnapshots']) == 0:
        raise Exception("No snapshots found")

    snapshots_per_project = {}
    for snapshot in response['DBSnapshots']:
        if snapshot['Status'] != 'available':
            continue

        if snapshot['DBInstanceIdentifier'] not in snapshots_per_project.keys():
            snapshots_per_project[snapshot['DBInstanceIdentifier']] = {}

        snapshots_per_project[snapshot['DBInstanceIdentifier']][snapshot['DBSnapshotIdentifier']] = snapshot[
            'SnapshotCreateTime']

    for project in snapshots_per_project:
        sorted_list = sorted(snapshots_per_project[project].items(), key=operator.itemgetter(1), reverse=True)

        copy_name = project + "-cp-" + sorted_list[0][1].strftime("%Y-%m-%d")

        try:
               uat_client.describe_db_snapshots(
               DBSnapshotIdentifier=copy_name
            )
        except:
            response1 = uat_client.copy_db_snapshot(
                SourceDBSnapshotIdentifier='arn:aws:rds:us-east-1:760154870506:snapshot:my1snapshot-mysqltestdb-2019-03-04-12-7-40lambda-snap',
                TargetDBSnapshotIdentifier=copy_name,
                CopyTags=True
            )
            print("Copied " + copy_name)

            continue
        
def lambda_handler(event, context):
    copy_latest_snapshot()
    
if __name__ == '__main__':
    lambda_handler(None, None)
