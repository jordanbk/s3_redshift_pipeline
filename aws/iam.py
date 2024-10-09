import json
import aws
from .. import awscommon
from .awscommon import get_datetime_now

class IAM(awscommon.AWS):
    def __str__(self):
        return 'IAM object'

    def __repr__(self):
        return 'IAM()'

    def create_iam_role(self, iam_client):
        """
        Create a new IAM role and attach a role policy based on configuration.
        
        :param iam_client: IAM Client object.
        :return: None
        """
        try:
            aws.logger.info("Creating IAM Role...")
            start_time = get_datetime_now()

            create_resp = iam_client.create_role(
                Path='/',
                RoleName=self.iam_role_name,
                Description=self.iam_role_description,
                AssumeRolePolicyDocument=json.dumps({
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Effect': 'Allow',
                            'Principal': {'Service': 'redshift.amazonaws.com'},
                            'Action': 'sts:AssumeRole'
                        }
                    ]
                })
            )

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"IAM Role created in {elapsed_time} ms. Status: {create_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error while creating IAM Role: {exp}")
            return

        self.attach_role_policy(iam_client)

    def attach_role_policy(self, iam_client):
        """
        Attach a policy to the IAM role.
        
        :param iam_client: IAM Client object.
        :return: None
        """
        try:
            aws.logger.info("Attaching Role Policy...")
            start_time = get_datetime_now()

            attach_resp = iam_client.attach_role_policy(
                RoleName=self.iam_role_name,
                PolicyArn=self.iam_policy_arn
            )

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Role Policy attached in {elapsed_time} ms. Status: {attach_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error while attaching IAM Role Policy: {exp}")

    @staticmethod
    def get_iam_role_arn(iam_client, iam_role_name):
        """
        Retrieve the ARN for a given IAM role.
        
        :param iam_client: IAM Client object.
        :param iam_role_name: Name of the IAM role.
        :return: ARN of the IAM role or None if not found.
        """
        try:
            return iam_client.get_role(RoleName=iam_role_name)['Role']['Arn']
        except Exception as exp:
            aws.logger.error(f"Error retrieving IAM Role ARN: {exp}")
            return None

    def delete_iam_role(self, iam_client, iam_role_name=None, policy_arn=None):
        """
        Detach policy and delete IAM role.
        
        :param iam_client: IAM Client object.
        :param iam_role_name: (optional) IAM role to delete. Defaults to configured role.
        :param policy_arn: (optional) Policy ARN to detach. Defaults to configured policy.
        :return: None
        """
        iam_role_name = iam_role_name or self.iam_role_name
        policy_arn = policy_arn or self.iam_policy_arn

        if not self.detach_role_policy(iam_client, iam_role_name, policy_arn):
            return

        try:
            aws.logger.info(f"Deleting IAM Role: {iam_role_name}...")
            start_time = get_datetime_now()

            delete_resp = iam_client.delete_role(RoleName=iam_role_name)

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"IAM Role deleted in {elapsed_time} ms. Status: {delete_resp['ResponseMetadata']['HTTPStatusCode']}")

        except Exception as exp:
            aws.logger.error(f"Error while deleting IAM Role: {exp}")

    def detach_role_policy(self, iam_client, iam_role_name, policy_arn):
        """
        Detach a policy from the IAM role.
        
        :param iam_client: IAM Client object.
        :param iam_role_name: Name of the IAM role.
        :param policy_arn: Policy ARN to detach.
        :return: True if successful, False otherwise.
        """
        try:
            aws.logger.info(f"Detaching Role Policy from {iam_role_name}...")
            start_time = get_datetime_now()

            detach_resp = iam_client.detach_role_policy(RoleName=iam_role_name, PolicyArn=policy_arn)

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Role Policy detached in {elapsed_time} ms. Status: {detach_resp['ResponseMetadata']['HTTPStatusCode']}")
            return True

        except Exception as exp:
            aws.logger.error(f"Error while detaching IAM Role Policy: {exp}")
            return False
