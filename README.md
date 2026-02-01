# CloudVigilante

CloudVigilante is a security auditing tool written in Python. It helps detect public S3 buckets in AWS environments to prevent data leaks.

## Features
- S3 Public Access Detection: Identifies buckets with public read permissions.
- JSON Reporting: Generates detailed audit findings with timestamps.
- Containerized: Ready to run with Docker for consistent results.
- Clean Code: Follows PEP 8 standards with Black and Flake8.

## Requirements
- Docker
- Python 3.11+
- LocalStack (for local simulation)

## Setup and Usage

1. Clone the repository:
```bash
   git clone https://github.com/eerasmocubillos/cloud-vigilante.git
```

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Run with Docker:
```bash
   docker build -t cloud-vigilante .
   docker run --rm --network="host" --env-file .env cloud-vigilante
```