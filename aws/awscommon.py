import config
import boto3
import datetime

class AWS:
    """
    AWS base class containing common attributes for AWS services.
    """
    def __init__(self):
        # Credentials
        self.key = config.KEY
        self.secret = config.SECRET

        # Redshift Configuration
        self.dwh_cluster_type = config.DWH_CLUSTER_TYPE
        self.dwh_num_nodes = config.DWH_NUM_NODES
        self.dwh_node_type = config.DWH_NODE_TYPE
        self.dwh_cluster_identifier = config.DWH_CLUSTER_IDENTIFIER
        self.dwh_db = config.DWH_DB
        self.dwh_db_user = config.DWH_DB_USER
        self.dwh_db_password = config.DWH_DB_PASSWORD
        self.dwh_port = config.DWH_PORT

        # Security Group
        self.group_name = config.GROUP_NAME
        self.group_description = config.GROUP_DESCRIPTION

        # Ingress Rules
        self.cidr_ip = config.CIDR_IP
        self.ingress_description = config.INGRESS_DESCRIPTION
        self.ip_protocol = config.IP_PROTOCOL
        self.from_port = config.FROM_PORT
        self.to_port = config.TO_PORT

        # Cluster Connection Details
        self.host = config.HOST
        self.db_name = config.DB_NAME
        self.db_user = config.DB_USER
        self.db_password = config.DB_PASSWORD
        self.db_port = config.DB_PORT

        # IAM Role
        self.iam_role_name = config.IAM_ROLE_NAME
        self.iam_policy_arn = config.IAM_POLICY_ARN
        self.iam_role_description = config.IAM_ROLE_DESCRIPTION
        self.iam_arn = config.IAM_ARN

        # S3
        self.log_data = config.LOG_DATA
        self.log_jsonpath = config.LOG_JSONPATH
        self.song_data = config.SONG_DATA

def get_boto3_client(service_name, region_name='us-east-1'):
    """
    General function to get any AWS service client.

    :param service_name: The name of the AWS service (e.g., 'ec2', 's3', 'iam', 'redshift').
    :param region_name: AWS region name (default: 'us-west-2').
    :return: boto3 client for the specified service.
    """
    return boto3.client(
        service_name,
        region_name=region_name,
        aws_access_key_id=config.KEY,
        aws_secret_access_key=config.SECRET
    )

def get_boto3_resource(service_name, region_name='us-east-1'):
    """
    General function to get any AWS service resource (only for services like S3).

    :param service_name: The name of the AWS service (e.g., 's3').
    :param region_name: AWS region name (default: 'us-west-2').
    :return: boto3 resource for the specified service.
    """
    return boto3.resource(
        service_name,
        region_name=region_name,
        aws_access_key_id=config.KEY,
        aws_secret_access_key=config.SECRET
    )

def get_datetime_now():
    """
    Returns the current datetime.

    :return: Current datetime object.
    """
    return datetime.datetime.now()
