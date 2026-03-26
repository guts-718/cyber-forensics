from ingestion.reader import read_logs
from detection.detector import detect_log_type, log_unknown
from parsers.linux_auth import parse_linux_auth

def main():
    file_path = "data/sample.log"

    for log in read_logs(file_path):
        detection = detect_log_type(log["raw"])

        if detection["type"] == "unknown":
            log_unknown(log["raw"])
            continue

        parsed = None

        if detection["type"] == "linux_auth":
            parsed = parse_linux_auth(log["raw"])

        print({
            "line": log["line_number"],
            "detected_type": detection["type"],
            "parsed": parsed,
            "raw": log["raw"]
        })

if __name__ == "__main__":
    main()