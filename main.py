import sys
from pathlib import Path

# --- Fix imports ---
sys.path.insert(0, str(Path(__file__).parent))

# --- Ingestion ---
from ingestion.reader import read_logs
from adapters.csv_adapter import read_csv_logs

# --- Detection ---
from detection.detector import detect_log_type, log_unknown

# --- Parsers ---
from parsers.linux_auth import parse_linux_auth
from parsers.system_parser import parse_system_log
from parsers.network_parser import parse_network_log
from parsers.hdfs_parser import parse_hdfs_log
from parsers.generic_parser import parse_generic_log

# --- Processing ---
from normalization.normalizer import normalize_log

# --- Storage ---
from storage.writer import write_log, write_raw_log

# --- Debug / Features ---
from features.extractor import extract_features
from detection.rule_engine import rule_based_detection


def main():
    file_path = "data/sample-main-mon-plus.csv"
    file_path = "data/friday_plus.csv"

    # --- Choose ingestion method ---
    if file_path.endswith(".csv"):
        log_stream = read_csv_logs(file_path)
    else:
        log_stream = read_logs(file_path)
    count = 0
    for log in log_stream:
        count += 1
        raw = log["raw"]

        # --- DEBUG: show adapted log ---
        # print("\nRAW:", raw)

        # --- Optional: store adapted logs ---
        write_raw_log(raw)

        # --- Detection ---
        detection = detect_log_type(raw)
        # print("DETECTED:", detection)

        # --- Handle unknown detection ---
        if detection["type"] == "unknown":
            log_unknown(raw)
            write_log({"raw_log": raw}, "unknown")
            continue

        # --- Parsing ---
        parsed = None

        if detection["type"] == "linux_auth":
            parsed = parse_linux_auth(raw)

        elif detection["type"] == "system":
            parsed = parse_system_log(raw)

        elif detection["type"] == "network":
            parsed = parse_network_log(raw)

        elif detection["type"] == "hdfs":
            parsed = parse_hdfs_log(raw)

        # --- Fallback parser ---
        if not parsed:
            parsed = parse_generic_log(raw)
            detected_type = "generic"
        else:
            detected_type = detection["type"]

        # print("PARSED:", parsed)

        # --- Normalization ---
        normalized = normalize_log(
            parsed,
            raw_log=raw,
            detected_type=detected_type,
            detection_conf=detection["confidence"]
        )

        # print("NORMALIZED:", normalized)

        # --- Storage ---
        write_log(normalized, detected_type)

        # --- Feature extraction (debug) ---
        features = extract_features(normalized)
        # print("FEATURES:", features)

        # --- Rule-based detection (debug) ---
        prediction = rule_based_detection(features)
        # print("RULE RESULT:", prediction)
    print(f"\nProcessed {count} logs.")


if __name__ == "__main__":
    main()