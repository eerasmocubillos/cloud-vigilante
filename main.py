import boto3

def initialize_client():
    """Initialize the S3 client for AWS."""
    return boto3.client('s3', region_name='us-east-1')

def main():
    print("--- CloudVigilante Auditor ---")
    client = initialize_client()
    print("Client initialized succesfully.")

if __name__ == "__main__":
    main()