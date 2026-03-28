import csv

def read_csv_logs(file_path):
    """
    Reads CSV and converts each row into a log-like string
    """

    with open(file_path, newline='', encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.DictReader(csvfile)

        for idx, row in enumerate(reader, start=1):

            # --- Convert row → log string ---
            log = adapt_row_to_log(row)

            yield {
                "line_number": idx,
                "raw": log
            }


def adapt_row_to_log(row):
    """
    Converts a CSV row into a log-like format
    (customizable per dataset)
    """

    parts = []

    # Common mappings (CICIDS-like datasets)
    if "Src IP" in row:
        parts.append(f"SRC={row['Src IP']}")

    if "Dst IP" in row:
        parts.append(f"DST={row['Dst IP']}")

    if "Protocol" in row:
        parts.append(f"PROTO={row['Protocol']}")

    if "Src Port" in row:
        parts.append(f"SPT={row['Src Port']}")

    if "Dst Port" in row:
        parts.append(f"DPT={row['Dst Port']}")

    if "Label" in row:
        parts.append(f"LABEL={row['Label']}")  # useful later
    
    if "Label" in row:
        parts.append(f"LABEL={row['Label']}")

    # fallback (important)
    if not parts:
        parts.append("RAW=" + " ".join([f"{k}={v}" for k, v in row.items()]))

    return " ".join(parts)