def rule_based_detection(features):
    """
    Simple baseline rules
    """

    # Rule 1: Suspicious high port
    if features["destination_port"]:
        if int(features["destination_port"]) > 50000:
            return 1  # anomaly

    # Rule 2: Failed authentication
    if features["outcome"] == "failed":
        return 1

    # Rule 3: Suspicious protocol (example)
    if features["protocol"] == "icmp":
        return 1

    return 0  # normal