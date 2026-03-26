import re

def parse_linux_auth(log):
    """
    Parses Linux SSH authentication logs
    Returns structured dict + confidence
    """

    # Failed login
    failed_pattern = r'(\w{3} \d+ \d+:\d+:\d+).*sshd\[\d+\]: Failed password for (\w+) from ([\d.]+)'

    # Successful login
    success_pattern = r'(\w{3} \d+ \d+:\d+:\d+).*sshd\[\d+\]: Accepted password for (\w+) from ([\d.]+)'

    match_failed = re.search(failed_pattern, log)
    match_success = re.search(success_pattern, log)

    if match_failed:
        return {
            "timestamp": match_failed.group(1),
            "event_type": "login_failure",
            "user": match_failed.group(2),
            "source_ip": match_failed.group(3),
            "process": "sshd",
            "status": "failed",
            "message": log, 
            "confidence": 0.95
        }

    if match_success:
        return {
            "timestamp": match_success.group(1),
            "event_type": "login_success",
            "user": match_success.group(2),
            "source_ip": match_success.group(3),
            "process": "sshd",
            "status": "success",
            "message": log, 
            "confidence": 0.90
        }

    # Partial match fallback
    if "sshd" in log:
        return {
            "raw_partial": log,
            "event_type": "unknown_auth",
            "message": log, 
            "confidence": 0.50
        }

    return None