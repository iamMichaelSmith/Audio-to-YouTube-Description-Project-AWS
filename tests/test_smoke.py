import pathlib


def test_lambda_files_exist():
    expected = [
        "TranscriptAudioFunction-Lambda.py",
        "GenerateYoutubeDescriptionFunction-Lambda.py",
    ]
    for name in expected:
        assert pathlib.Path(name).exists(), f"Missing required file: {name}"


def test_lambda_files_compile():
    for path in pathlib.Path(".").glob("*Lambda*.py"):
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
