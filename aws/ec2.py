import aws
from .. import awscommon
from .iam import IAM
from .awscommon import get_datetime_now

class EC2(awscommon.AWS):
    def __str__(self):
        return 'EC2 object'

    def __repr__(self):
        return 'EC2()'

    def get_security_groups(self, ec2_client):
        """
        Retrieve EC2 security groups.

        :param ec2_client: EC2 Client object.
        :return: A list of security groups if found, else None.
        """
        try:
            security_groups = ec2_client.describe_security_groups()["SecurityGroups"]
            return security_groups if security_groups else None
        except Exception as exp:
            aws.logger.error(f"Error retrieving security groups: {exp}")
            return None

    def security_group_exists(self, ec2_client, group_name=None):
        """
        Check if the given security group exists.

        :param ec2_client: EC2 Client object.
        :param group_name: Name of the security group to search for.
        :return: True if found, False otherwise.
        """
        try:
            group_name = group_name or self.group_name
            security_groups = self.get_security_groups(ec2_client)
            if security_groups:
                return any(group['GroupName'] == group_name for group in security_groups)
            return False
        except Exception as exp:
            aws.logger.error(f"Error checking security group existence: {exp}")
            return False

    def create_security_group(self, ec2_client, authorize_group=True):
        """
        Create a security group and add ingress rules.

        :param ec2_client: EC2 Client object.
        :param authorize_group: Whether to authorize ingress rules after creation.
        :return: None.
        """
        if self.security_group_exists(ec2_client, self.group_name):
            aws.logger.info(f"Security group {self.group_name} already exists.")
            return

        try:
            aws.logger.info("Creating Security Group...")
            start_time = get_datetime_now()
            vpc_id = ec2_client.describe_vpcs().get('Vpcs', [{}])[0].get('VpcId', '')

            response = ec2_client.create_security_group(
                GroupName=self.group_name,
                Description=self.group_description,
                VpcId=vpc_id
            )
            security_group_id = response['GroupId']

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Security group created in {elapsed_time} ms. Group ID: {security_group_id}")

            if authorize_group:
                self.authorize_security_group(ec2_client, security_group_id)

        except Exception as exp:
            aws.logger.error(f"Error creating security group: {exp}")

    def authorize_security_group(self, ec2_client, security_group_id):
        """
        Authorize ingress rules for the security group.

        :param ec2_client: EC2 Client object.
        :param security_group_id: Security Group ID.
        :return: None.
        """
        if self.security_group_exists(ec2_client, self.group_name):
            aws.logger.info(f"Security group {self.group_name} already exists.")
            return

        try:
            aws.logger.info(f"Authorizing Security Group {security_group_id}...")
            start_time = get_datetime_now()

            response = ec2_client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpProtocol=self.ip_protocol,
                FromPort=int(self.from_port),
                ToPort=int(self.to_port),
                CidrIp=self.cidr_ip
            )

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Ingress rules authorized in {elapsed_time} ms. Status: {response['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error authorizing security group: {exp}")

    def delete_security_group(self, ec2_client):
        """
        Delete an EC2 security group.

        :param ec2_client: EC2 Client object.
        :return: None.
        """
        security_group = self.get_security_groups(ec2_client)
        if not security_group:
            aws.logger.info(f"Security group {self.group_name} not found.")
            return

        try:
            aws.logger.info(f"Deleting Security Group {security_group[0]['GroupId']}...")
            start_time = get_datetime_now()

            response = ec2_client.delete_security_group(
                GroupId=security_group[0]['GroupId'],
                GroupName=self.group_name
            )

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Security group deleted in {elapsed_time} ms. Status: {response['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error deleting security group: {exp}")
