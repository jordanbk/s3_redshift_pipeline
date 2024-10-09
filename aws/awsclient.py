from . import redshift, s3, iam, ec2

class AWSClient(redshift.Redshift, s3.S3, iam.IAM, ec2.EC2):
    def __str__(self):
        return 'AWSClient object'

    def __repr__(self):
        return 'AWSClient()'