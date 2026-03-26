import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ingestion.reader import read_logs
from detection.detector import detect_log_type, log_unknown
from parsers.linux_auth import parse_linux_auth
from normalization.normalizer import normalize_log
from parsers.system_parser import parse_system_log
from storage.writer import write_log  # noqa: E402
from parsers.network_parser import parse_network_log

def main():
    file_path = "data/sample.log"

    for log in read_logs(file_path):
        raw = log["raw"]
        detection = detect_log_type(raw)

        parsed = None

        if detection["type"] == "unknown":
            log_unknown(log["raw"])
            continue

        parsed = None

        if detection["type"] == "linux_auth":
            parsed = parse_linux_auth(log["raw"])

        elif detection["type"] == "system":
            parsed = parse_system_log(log["raw"])
        
        elif detection["type"] == "network":
            parsed = parse_network_log(raw)
        

        if not parsed:
            write_log(
                {
                    "raw_log": raw,
                    "reason": "parse_failed",
                    "detected_type": detection["type"]
                },
                "unknown"
            )

            continue
        normalized = normalize_log(
            parsed,
            raw_log=log["raw"],
            detected_type=detection["type"],
            detection_conf=detection["confidence"]
        )
        write_log(normalized, detection["type"])
        print(normalized)


if __name__ == "__main__":
    main()