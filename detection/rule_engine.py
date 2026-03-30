def rule_based_detection(features):
    port = int(features["destination_port"] or 0)
    protocol = features["protocol"]

    # Rule 1: very high ports
    if port > 50000:
        return 1

    # Rule 2: suspicious ports
    if port in [4444, 5555, 6666, 9999]:
        return 1

    # Rule 3: UDP high traffic (basic heuristic)
    if protocol == "udp" and port > 10000:
        return 1

    return 0