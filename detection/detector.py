import re

def detect_log_type(log):
    text = log.lower()

    # --- 1. Linux Auth Logs ---
    if "sshd" in text and ("failed password" in text or "accepted password" in text):
        return "linux_auth"

    # --- 2. Network Logs ---
    if "src=" in text or "dst=" in text:
        return "network"

    # --- 3. HDFS Logs ---
    if "blk_" in text or "dfs" in text:
        return "hdfs"

    # --- 4. Generic System Logs ---
    if re.search(r'\w{3} \d{1,2} \d{2}:\d{2}:\d{2}', log):
        return "system"

    # --- fallback ---
    return "unknown"