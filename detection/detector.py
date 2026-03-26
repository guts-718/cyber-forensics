import re

def detect_log_type(log, source_hint=None):
    text = log.lower()

    # --- 1. Use dataset hint (strong signal) ---
    if source_hint == "hdfs":
        return {"type": "hdfs", "confidence": 0.95}

    if source_hint == "network":
        return {"type": "network", "confidence": 0.95}

    # --- 2. Linux Auth Logs ---
    if "sshd" in text and "failed password" in text:
        return {"type": "linux_auth", "confidence": 0.95}

    if "sshd" in text and "accepted password" in text:
        return {"type": "linux_auth", "confidence": 0.90}

    # --- 3. Network Logs ---
    if "src=" in text or "dst=" in text:
        return {"type": "network", "confidence": 0.85}

    # --- 4. HDFS Logs ---
    if "blk_" in text or "dfs" in text:
        return {"type": "hdfs", "confidence": 0.80}

    # --- 5. Generic system logs ---
    if re.search(r'\w{3} \d{1,2} \d{2}:\d{2}:\d{2}', log):
        return {"type": "system", "confidence": 0.60}

    # --- fallback ---
    return {"type": "unknown", "confidence": 0.0}


def log_unknown(log, filepath="detection/unknown_logs.txt"):
    with open(filepath, "a") as f:
        f.write(log + "\n")