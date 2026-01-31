import boto3
import os
from dotenv import load_dotenv

load_dotenv()


def get_s3_client():
    """Factory to create an S3 client based on environment variables."""
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )


def check_public_access(s3_client, bucket_name):
    """
    Analyzes the Access Control List (ACL) of a bucket.
    Returns True if the 'AllUsers' group has access.
    """
    try:
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        for grant in acl.get("Grants", []):
            grantee = grant.get("Grantee", {})
            if grantee.get("URI") == "http://acs.amazonaws.com/groups/global/AllUsers":
                return True
        return False
    except Exception as e:
        print(f"Error checking ACL for {bucket_name}: {e}")
        return False


def run_audit():
    """Orchestrates the S3 auditing process."""
    print("\n--- CloudVigilante: S3 Security Scan ---")
    s3 = get_s3_client()

    try:
        buckets = s3.list_buckets().get("Buckets", [])
        if not buckets:
            print("[?] No buckets found in the account.")
            return

        for bucket in buckets:
            name = bucket["Name"]
            is_public = check_public_access(s3, name)

            status = "[!] PUBLIC" if is_public else "[OK] PRIVATE"
            print(f"{status} | Bucket: {name}")

    except Exception as e:
        print(f"[E] Critical error during scan: {e}")


if __name__ == "__main__":
    run_audit()
