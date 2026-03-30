import csv

def read_csv_logs(file_path):
    with open(file_path, newline='', encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)

        for idx, row in enumerate(reader, start=1):
            log = adapt_row_to_log(row)

            yield {
                "line_number": idx,
                "raw": log
            }


def adapt_row_to_log(row):
    # normalize keys
    row = {k.strip().lower(): v for k, v in row.items()}

    parts = []

    src_ip = row.get("src ip") or row.get("src ip dec")
    dst_ip = row.get("dst ip") or row.get("dst ip dec")

    src_port = row.get("src port")
    dst_port = row.get("dst port")

    protocol = row.get("protocol")
    label = row.get("label")

    if src_ip:
        parts.append(f"SRC={src_ip}")

    if dst_ip:
        parts.append(f"DST={dst_ip}")

    if protocol:
        parts.append(f"PROTO={protocol}")

    if src_port:
        parts.append(f"SPT={src_port}")

    if dst_port:
        parts.append(f"DPT={dst_port}")

    if label:
        parts.append(f"LABEL={label}")

    if not parts:
        parts.append("RAW=" + " ".join([f"{k}={v}" for k, v in row.items()]))

    return " ".join(parts)