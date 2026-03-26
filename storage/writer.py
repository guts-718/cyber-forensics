import json
import os

OUTPUT_DIR = "output"


def write_log(log, log_type):
    """
    Writes a log to a JSONL file based on its type.

    Args:
        log (dict): normalized or fallback log
        log_type (str): type of log (linux_auth, system, network, unknown)
    """

    if not log:
        return

    try:
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Sanitize log_type (important)
        safe_type = log_type if log_type else "unknown"

        file_path = os.path.join(OUTPUT_DIR, f"{safe_type}.jsonl")

        # Write as JSON line
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log, ensure_ascii=False) + "\n")

    except Exception as e:
        # Fail-safe: don't crash pipeline
        print(f"[ERROR] Failed to write log: {e}")