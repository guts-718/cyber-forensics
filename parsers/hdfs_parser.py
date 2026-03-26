import re

def parse_hdfs_log(log):
    """
    Parses HDFS logs (semi-structured)
    """

    # Example pattern
    pattern = r'(\d{6} \d{6}) (\d+) (\w+) ([\w\.]+): (.*)'

    match = re.search(pattern, log)

    if not match:
        return None

    message = match.group(5)

    # Extract block ID if present
    block_match = re.search(r'(blk_\d+)', message)

    return {
        "timestamp": match.group(1),
        "level": match.group(3),
        "component": match.group(4),
        "event_type": "block_operation",
        "block_id": block_match.group(1) if block_match else None,
        "message": message,
        "confidence": 0.85
    }