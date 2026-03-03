# Audio to YouTube Description Project (AWS)

Automates a common content workflow:
1. Take audio input
2. Generate transcript
3. Generate YouTube-ready description text from transcript

## Architecture
- `TranscriptAudioFunction-Lambda.py` - Transcription Lambda function
- `GenerateYoutubeDescriptionFunction-Lambda.py` - Description generation Lambda function
- `GenerateYoutubeDescriptionFunction-Lambda-test.py` - manual/test helper script
- `Project Diagram.png` - architecture image
- `Project-Overview` - original project notes

## Employment-Ready Setup
This repository now includes CI, test scaffolding, and docs so teammates can onboard fast.

### Local Setup
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Quality Gate
```bash
ruff check .
black --check .
pytest -q
```

## AWS Deployment Notes
- Deploy Lambda functions with least-privilege IAM roles.
- Keep model/API keys in AWS Secrets Manager or SSM Parameter Store.
- Do not hardcode credentials in Lambda source.

## Key Environment Variables
See `.env.example` for baseline local variable names.

## Ops Docs
- `docs/ARCHITECTURE.md`
- `docs/DEPLOY_RUNBOOK.md`
- `docs/HANDOFF_CHECKLIST.md`

## License
MIT (see `LICENSE`).
