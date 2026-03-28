def evaluate(predictions, labels):
    """
    Compute basic metrics
    """

    tp = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == "Attack")
    tn = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == "Normal")
    fp = sum(1 for p, l in zip(predictions, labels) if p == 1 and l == "Normal")
    fn = sum(1 for p, l in zip(predictions, labels) if p == 0 and l == "Attack")

    precision = tp / (tp + fp + 1e-6)
    recall = tp / (tp + fn + 1e-6)
    f1 = 2 * precision * recall / (precision + recall + 1e-6)

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1
    }