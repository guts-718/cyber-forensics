from ingestion.reader import read_logs
from detection.detector import detect_log_type, log_unknown
from parsers.linux_auth import parse_linux_auth
from normalization.normalizer import normalize_log


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

        normalized = normalize_log(
            parsed,
            raw_log=log["raw"],
            detected_type=detection["type"],
            detection_conf=detection["confidence"]
        )

        print(normalized)


if __name__ == "__main__":
    main()