def normalize_log(parsed, raw_log, detected_type, detection_conf):
    """
    Converts parsed log into unified schema
    """

    if not parsed:
        return None

    # --- Event mapping ---
    event_type = parsed.get("event_type")

    if event_type == "login_failure":
        category = "authentication"
        action = "login"
        outcome = "failed"
    elif event_type == "login_success":
        category = "authentication"
        action = "login"
        outcome = "success"
    else:
        category = "unknown"
        action = "unknown"
        outcome = "unknown"

    return {
        "timestamp": parsed.get("timestamp"),
        "source": "linux" if detected_type == "linux_auth" else "unknown",

        "event": {
            "type": event_type,
            "category": category,
            "action": action,
            "outcome": outcome
        },

        "user": {
            "name": parsed.get("user"),
            "id": None
        },

        "source_ip": parsed.get("source_ip"),
        "destination_ip": None,

        "device": {
            "hostname": None,
            "os": "linux"
        },

        "process": {
            "name": parsed.get("process"),
            "pid": None
        },

        "file": {
            "path": None,
            "action": None
        },

        "network": {
            "protocol": None,
            "port": None
        },

        "metadata": {
            "raw_log": raw_log,
            "parser": detected_type,
            "detection_confidence": detection_conf,
            "parsing_confidence": parsed.get("confidence")
        }
    }