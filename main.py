import os
import boto3
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
    )


def check_public_access(s3_client, bucket_name):
    try:
        acl = s3_client.get_bucket_acl(Bucket=bucket_name)
        public_uri = "http://acs.amazonaws.com/groups/global/AllUsers"
        for grant in acl.get("Grants", []):
            grantee = grant.get("Grantee", {})
            if grantee.get("URI") == public_uri:
                return True
        return False
    except Exception:
        return False


def save_report(results):
    report = {
        "timestamp": datetime.now().isoformat(),
        "scan_type": "S3_Bucket_ACL",
        "findings": results,
    }

    with open("audit_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("\n[OK] Report saved to audit_report.json")


def run_audit():
    print("--- CloudVigilante: S3 Security Scan ---")
    s3 = get_s3_client()
    audit_results = []

    try:
        buckets = s3.list_buckets().get("Buckets", [])
        for bucket in buckets:
            name = bucket["Name"]
            is_public = check_public_access(s3, name)

            audit_results.append(
                {
                    "bucket_name": name,
                    "is_public": is_public,
                    "status": "DANGER" if is_public else "SECURE",
                }
            )

            status_tag = "[!]" if is_public else "[OK]"
            print(f"{status_tag} Scanned: {name}")

        save_report(audit_results)

    except Exception as e:
        print(f"[E] Error: {e}")


if __name__ == "__main__":
    run_audit()
