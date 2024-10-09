import config
from . import aws_common

class S3(aws_common.AWS):
    def __str__(self):
        return 'S3 object'

    def __repr__(self):
        return 'S3()'