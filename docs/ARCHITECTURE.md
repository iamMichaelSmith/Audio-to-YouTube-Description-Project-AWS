# Architecture

## Goal
Convert source audio into useful YouTube description copy using AWS Lambda stages.

## Pipeline
1. **Input Stage**: audio source arrives in input storage/event trigger.
2. **Transcription Stage** (`TranscriptAudioFunction-Lambda.py`): generates transcript text.
3. **Description Stage** (`GenerateYoutubeDescriptionFunction-Lambda.py`): builds YouTube-ready description output.
4. **Output Stage**: save generated description for publishing workflow.

## Reliability Principles
- Keep functions idempotent when possible.
- Log request IDs and processing status for each job.
- Isolate credentials in AWS-managed secret stores.
