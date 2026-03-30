def extract_features(log):
    port = int(log["network"].get("destination_port") or 0)
    protocol = log["network"].get("protocol")

    return {
        "event_type": log["event"]["type"],
        "event_category": log["event"]["category"],
        "action": log["event"]["action"],
        "outcome": log["event"]["outcome"],

        "protocol": protocol,
        "source_port": log["network"].get("source_port"),
        "destination_port": port,

        "log_level": log.get("log_level"),
        "has_ip": 1 if log.get("source_ip") else 0,

        # 🔥 NEW FEATURES
        "is_high_port": 1 if port > 50000 else 0,
        "is_well_known_port": 1 if port < 1024 else 0,
        "is_dns": 1 if port == 53 else 0,
        "is_ntp": 1 if port == 123 else 0,
        "is_mdns": 1 if port == 5353 else 0,

        "is_udp": 1 if protocol == "udp" else 0,
        "is_tcp": 1 if protocol == "tcp" else 0,

        "label": log["metadata"].get("label")
    }