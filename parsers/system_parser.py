import re

def parse_system_log(log):
    """
    Generic parser for system logs (syslog-style, BGL-like)
    Extracts partial structured info
    """

    # Pattern: timestamp hostname process: message
    pattern = r'^(\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (\S+) (\w+): (.*)'

    match = re.search(pattern, log)

    if match:
        return {
            "timestamp": match.group(1),
            "device": match.group(2),
            "process": match.group(3),
            "event_type": "system_event",
            "message": match.group(4),
            "confidence": 0.75
        }

    # weaker fallback: try just timestamp
    partial_pattern = r'^(\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) (.*)'

    match_partial = re.search(partial_pattern, log)

    if match_partial:
        return {
            "timestamp": match_partial.group(1),
            "event_type": "system_event",
            "message": match_partial.group(2),
            "confidence": 0.50
        }

    return None