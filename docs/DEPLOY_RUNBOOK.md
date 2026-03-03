# Deploy Runbook

## 1) Prerequisites
- AWS account access to Lambda, IAM, CloudWatch Logs, and storage services in use.
- Python 3.10+ for local packaging/testing.

## 2) Local validation
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
ruff check .
black --check .
pytest -q
```

## 3) Deploy steps
1. Package function code or update via CI/CD.
2. Update Lambda environment variables from `.env.example` equivalents.
3. Confirm IAM role allows only required actions.
4. Run a smoke test with one known-good input.

## 4) Post-deploy checks
- Validate CloudWatch logs for successful execution.
- Confirm transcript and description output is written to expected destination.
- Validate output text quality against your content standard.

## 5) Rollback
- Re-deploy last known-good Lambda package/version.
- Restore previous env variable set if config regression is suspected.
