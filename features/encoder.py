def encode_features(features):
    protocol_map = {
        "tcp": 1,
        "udp": 2,
        "icmp": 3
    }

    event_map = {
        "network_connection": 1,
        "login_failure": 2,
        "login_success": 3,
        "system_event": 4,
        "block_operation": 5,
        "generic_event": 6
    }

    return [
        protocol_map.get(features["protocol"], 0),
        int(features["destination_port"] or 0),
        event_map.get(features["event_type"], 0),
        features["has_ip"],

        # NEW FEATURES
        features["is_high_port"],
        features["is_well_known_port"],
        features["is_dns"],
        features["is_ntp"],
        features["is_mdns"],
        features["is_udp"],
        features["is_tcp"],
    ]