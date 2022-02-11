import os
import boto3
# from dotenv import load_dotenv
from collections import namedtuple
from datetime import datetime, timedelta, timezone

account_profiles = ['devopsadmin-mono-prod', 'devopsadmin-k8s-prod', 'devopsadmin-k8s-stage', 'devopsadmin-sandbox', 'devopsadmin-de','devopsadmin-networking', 'devopsadmin-security', 'devopsadmin-ops-prod', 'devopsadmin-payments-prod', 'devopsadmin-payments-stage']

for account_profile in account_profiles:
    
    session = boto3.Session(profile_name=account_profile, region_name='us-east-1')
    iam = session.client('iam')

    retentionDate = datetime.now() - timedelta(days=90)
    format = '%Y-%m-%d'

    # load_dotenv()
    
    file_name = "iam_user_audit.txt"
    User = namedtuple('User', 'user arn user_creation_time password_enabled password_last_used password_last_changed password_next_rotation mfa_active access_key_1_active access_key_1_last_rotated access_key_1_last_used_date access_key_1_last_used_region access_key_1_last_used_service access_key_2_active access_key_2_last_rotated access_key_2_last_used_date access_key_2_last_used_region access_key_2_last_used_service cert_1_active cert_1_last_rotated cert_2_active cert_2_last_rotated')

    generate_creds_report = iam.generate_credential_report()
    response = iam.get_credential_report()
    body = response['Content'].decode('utf-8')
    # print(body)
    lines = body.split('\n')
    print(lines)
    users = [User(*line.split(',')) for line in lines[1:]]
    with open(file_name, 'a') as out:
        out.write("-----------" + account_profile + "---------------------" + '\n')
        for user in users:
            if (user.access_key_1_last_rotated != 'N/A' and datetime.strptime(user.access_key_1_last_rotated[:10], format) < retentionDate) or (user.access_key_2_last_rotated != 'N/A' and datetime.strptime(user.access_key_2_last_rotated[:10], format) < retentionDate and (user.access_key_1_active or user.access_key_2_active)):
                    # out.write('IAM Username: ' + user.user + ' ' + 'Creation date: ' + user.user_creation_time + ' Password enabled?: ' + user.password_enabled + ' Needs rotated or deleted' + '\n')
                    out.write('IAM Username: ' + user.user + ' ' +  'Needs rotated or deleted' + '\n')
                    out.close
                    # print(user.user + " " + user.user_creation_time)

                     