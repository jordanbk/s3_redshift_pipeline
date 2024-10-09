import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    def __init__(self):
        # AWS Credentials
        self.aws_key = os.getenv('AWS_KEY')
        self.aws_secret = os.getenv('AWS_SECRET')

        # DWH Configuration
        self.dwh_cluster_type = os.getenv('DWH_CLUSTER_TYPE')
        self.dwh_num_nodes = os.getenv('DWH_NUM_NODES')
        self.dwh_node_type = os.getenv('DWH_NODE_TYPE')

        self.dwh_cluster_identifier = os.getenv('DWH_CLUSTER_IDENTIFIER')
        self.dwh_db = os.getenv('DWH_DB')
        self.dwh_db_user = os.getenv('DWH_DB_USER')
        self.dwh_db_password = os.getenv('DWH_DB_PASSWORD')
        self.dwh_port = os.getenv('DWH_PORT')

    def __repr__(self):
        return f"Config(AWS_KEY={self.aws_key}, DWH_CLUSTER_TYPE={self.dwh_cluster_type})"

# Usage Example
config = Config()
print(config)
