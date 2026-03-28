def extract_features(log):
    """
    Extract features from normalized log
    """

    return {
        "event_type": log["event"]["type"],
        "event_category": log["event"]["category"],
        "action": log["event"]["action"],
        "outcome": log["event"]["outcome"],

        "protocol": log["network"]["protocol"],
        "source_port": log["network"].get("source_port"),
        "destination_port": log["network"].get("destination_port"),

        "log_level": log.get("log_level"),

        "has_ip": 1 if log.get("source_ip") else 0,

        "label": log["metadata"].get("label")  # ground truth
    }