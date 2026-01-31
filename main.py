import boto3


def initialize_client():
    """Initializes the S3 client for LocalStack."""
    return boto3.client(
        "s3",
        region_name="us-east-1",
        endpoint_url="http://localhost:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )


def check_public_access(s3_client, bucket_name):
    """Checks if a bucket has public access via ACL."""
    try:
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl.get("Grants", []):
            grantee = grant.get("Grantee", {})
            # Check if the 'AllUsers' group has access
            if grantee.get("URI") == "http://acs.amazonaws.com/groups/global/AllUsers":
                return True
        return False
    except Exception as e:
        print(f"Error checking ACL for {bucket_name}: {e}")
        return False


def audit_s3_buckets(s3_client):
    """Main audit logic to scan all buckets for security risks."""
    print("\n[!] Starting S3 Security Audit...")
    try:
        response = s3_client.list_buckets()
        buckets = response.get("Buckets", [])

        for bucket in buckets:
            name = bucket["Name"]
            is_public = check_public_access(s3_client, name)

            status = "🔴 PUBLIC (DANGEROUS)" if is_public else "🟢 PRIVATE (SECURE)"
            print(f"-> Bucket: {name} | Status: {status}")

    except Exception as e:
        print(f"Error during audit: {e}")


def main():
    print("--- CloudVigilante Auditor ---")
    s3 = initialize_client()
    audit_s3_buckets(s3)


if __name__ == "__main__":
    main()
