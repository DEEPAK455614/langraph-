"""Production entrypoint that refuses to boot unless Gemini works end-to-end."""
from workflow import ask_question

_probe = ask_question("Reply with exactly this text and nothing else: GRAPHMIND_OK")
if "GRAPHMIND_OK" not in str(_probe):
    raise RuntimeError(f"Gemini startup verification failed: {_probe!r}")

from production_app import app  # noqa: E402
