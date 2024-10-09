import aws
from . import aws_common
from .iam import IAM
from .awscommon import get_datetime_now

class Redshift(aws_common.AWS):

    def create_rs_cluster(self, rs_client, iam_client, vpc_security_group_id):
        """
        :param rs_client: redshift client
        :param iam_client: IAM client
        :param vpc_security_group_id: Security Group ID

        :return None
        """
        try:
            aws.logger.info("Creating Cluster...")
            iam_role = IAM.get_IAM_ARN_role(iam_client, self.iam_role_name)
            start_time = get_datetime_now()

            create_cluster_resp = rs_client.create_cluster(
                ClusterType=self.dwh_cluster_type,
                NodeType=self.dwh_node_type,
                NumberOfNodes=int(self.dwh_num_nodes),
                DBName=self.dwh_db,
                ClusterIdentifier=self.dwh_cluster_identifier,
                MasterUsername=self.dwh_db_user,
                MasterUserPassword=self.dwh_db_password,
                VpcSecurityGroupIds=[vpc_security_group_id],
                IamRoles=[iam_role]
            )

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Cluster created in {elapsed_time} ms, Status Code: {create_cluster_resp['ResponseMetadata']['HTTPStatusCode']}")
        except Exception as exp:
            aws.logger.error(f"Error creating Redshift cluster: {exp}")

    @staticmethod
    def get_rs_cluster_status(rs_client, cluster_identifier):
        """
        :param rs_client: Redshift Client object
        :param cluster_identifier: Redshift Cluster Identifier

        :return string of Redshift cluster status if found, else return None
        """
        try:
            return rs_client.describe_clusters(ClusterIdentifier=cluster_identifier)['Clusters'][0]['ClusterStatus']
        except Exception as exp:
            aws.logger.error(f"Error retrieving Redshift Cluster: {exp}")
            return None

    def delete_rs_cluster(self, rs_client, cluster_id=None):
        """
        :param rs_client: Redshift Client object
        :param cluster_id: (optional) Redshift Cluster Identifier.

        :return None
        """
        cluster_identifier = cluster_identifier or self.dwh_cluster_identifier

        try:
            aws.logger.info("Deleting Cluster...")
            start_time = get_datetime_now()

            delete_cluster_resp = rs_client.delete_cluster(
                ClusterIdentifier=cluster_identifier,
                SkipFinalClusterSnapshot=True
            )

            elapsed_time = (get_datetime_now() - start_time).microseconds / 1000.0
            aws.logger.info(f"Cluster deleted in {elapsed_time} ms, Status Code: {delete_cluster_resp['ResponseMetadata']['HTTPStatusCode']}")
        except Exception as exp:
            aws.logger.error(f"Error deleting Redshift cluster: {exp}")
