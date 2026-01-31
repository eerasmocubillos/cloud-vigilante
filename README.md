# CloudVigilante 🛡️

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Linter](https://img.shields.io/badge/style-black-000000.svg)

**CloudVigilante** is a lightweight security auditing tool designed to identify misconfigurations in AWS S3 buckets. This project demonstrates the integration of Python with cloud infrastructure APIs to automate security compliance.

## 🎯 Project Overview
The goal was to build a portable tool that can scan an AWS environment (simulated via LocalStack) and detect buckets with public read access, which is one of the most common causes of data breaches in the cloud.

## 🛠️ Key Features & Technical Implementation
- **Cloud Automation:** Uses `boto3` to interact with AWS S3 Service.
- **Security Logic:** Audits Access Control Lists (ACLs) to detect public exposure (AllUsers group).
- **Environment Management:** Uses `.env` files for secure configuration and `python-dotenv` for loading.
- **Reporting:** Automatically generates a time-stamped `audit_report.json` with detailed findings.
- **Containerization:** Fully dockerized for consistent execution across different environments.
- **Code Quality:** Formatted with `Black` and linted with `Flake8` to ensure PEP 8 compliance.

## 🚀 Getting Started

### 1. Requirements
- Docker
- Python 3.11+
- AWS CLI (for local testing)

### 2. Setup Environment
```bash
# Clone the repository
git clone [https://github.com/eerasmocubillos/cloud-vigilante.git](https://github.com/eerasmocubillos/cloud-vigilante.git)
cd cloud-vigilante

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Build the image
docker build -t cloud-vigilante .

# Run the container (Assumes LocalStack is running on host)
docker run --rm --network="host" --env-file .env cloud-vigilante
```

### 3. Setup Environment
```bash
# Build the image
docker build -t cloud-vigilante .

# Run the container (Assumes LocalStack is running on host)
docker run --rm --network="host" --env-file .env cloud-vigilante
```

### 📊 Sample Output
```
--- CloudVigilante: S3 Security Scan ---
[OK] Scanned: production-data-private
[!] Scanned: public-leak-bucket
[OK] Report saved to audit_report.json
```