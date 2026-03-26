import re

def parse_network_log(log):
    """
    Parses network logs with key=value format
    """

    # Extract key=value pairs
    pairs = re.findall(r'(\w+)=([^\s]+)', log)

    if not pairs:
        return None

    data = dict(pairs)

    return {
        "event_type": "network_connection",
        "source_ip": data.get("SRC"),
        "destination_ip": data.get("DST"),
        "source_port": data.get("SPT"),
        "destination_port": data.get("DPT"),
        "protocol": data.get("PROTO"),
        "action": data.get("ACTION"),
        "message": log,
        "confidence": 0.90
    }