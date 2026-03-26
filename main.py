import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parsers.hdfs_parser import parse_hdfs_log
from ingestion.reader import read_logs
from detection.detector import detect_log_type, log_unknown
from parsers.linux_auth import parse_linux_auth
from normalization.normalizer import normalize_log
from parsers.system_parser import parse_system_log
from storage.writer import write_log  # noqa: E402
from parsers.network_parser import parse_network_log
from parsers.generic_parser import parse_generic_log
from ingestion.reader import read_logs
from adapters.csv_adapter import read_csv_logs
from storage.writer import write_raw_log


def main():
    # file_path = "data/sample.log" 
    file_path="data/sample.csv"


    # --- Detect input type ---
    if file_path.endswith(".csv"):
        log_stream = read_csv_logs(file_path)
    else:
        log_stream = read_logs(file_path)

    

    for log in log_stream:
        raw = log["raw"]
        print("ADAPTED LOG:", raw)
        write_raw_log(raw)


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
        
        elif detection["type"] == "hdfs":
            parsed = parse_hdfs_log(raw)


        if not parsed:
            parsed = parse_generic_log(raw)
            detected_type = "generic"
        else:
            detected_type = detection["type"]

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