# extract something from every log.
# without this - logs -> unknown -> wasted
# with this - even messy logs -> usable..
import re

def parse_generic_log(log):
    """
    Fallback parser for unknown / unstructured logs
    """

    # Try extract timestamp (best effort)
    timestamp_match = re.search(r'\w{3} \d{1,2} \d{2}:\d{2}:\d{2}', log)

    timestamp = timestamp_match.group(0) if timestamp_match else None

    return {
        "timestamp": timestamp,
        "event_type": "generic_event",
        "message": log,
        "confidence": 0.30
    }