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
    proto = data.get("PROTO")

    protocol_map = {
        "6": "tcp",
        "17": "udp",
        "1": "icmp"
    }

    protocol = protocol_map.get(proto, str(proto).lower()) if proto else None

    print("PARSED:", data)

    return {
        "event_type": "network_connection",
        "source_ip": data.get("SRC"),
        "destination_ip": data.get("DST"),
        "source_port": data.get("SPT"),
        "destination_port": data.get("DPT"),
        "protocol" : protocol,
        "action": data.get("ACTION"),
        "label": data.get("LABEL"),
        "message": log,
        "confidence": 0.90
    }