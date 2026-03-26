def read_logs(file_path):
    """
    Generator that yields logs line by line.
    Handles encoding issues and large files.
    """
    with open(file_path, "r", errors="ignore") as f:
        for line_number, line in enumerate(f, start=1):
            yield {
                "line_number": line_number,
                "raw": line.strip()
            }