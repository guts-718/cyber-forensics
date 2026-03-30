def explain_prediction(features, prediction):
    """
    Generate human-readable explanation for a prediction
    """

    reasons = []

    port = int(features.get("destination_port") or 0)
    protocol = features.get("protocol")

    # --- Port-based reasoning ---
    if port > 50000:
        reasons.append(f"high destination port ({port})")

    if port in [4444, 5555, 6666, 9999]:
        reasons.append(f"suspicious port ({port})")

    if port == 53:
        reasons.append("DNS traffic")

    if port == 123:
        reasons.append("NTP traffic")

    if port == 5353:
        reasons.append("mDNS traffic")

    # --- Protocol reasoning ---
    if protocol == "udp":
        reasons.append("UDP protocol")

    if protocol == "tcp":
        reasons.append("TCP protocol")

    # --- Combine ---
    if prediction == 1:
        if reasons:
            explanation = "Anomalous due to: " + ", ".join(reasons)
        else:
            explanation = "Anomalous due to unusual pattern"
    else:
        explanation = "Normal behavior"

    return explanation