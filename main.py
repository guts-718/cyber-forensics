from ingestion.reader import read_logs
from detection.detector import detect_log_type

def main():
    file_path = "data/sample.log"

    for log in read_logs(file_path):
        log_type = detect_log_type(log["raw"])

        print({
            "line": log["line_number"],
            "type": log_type,
            "raw": log["raw"]
        })

if __name__ == "__main__":
    main()