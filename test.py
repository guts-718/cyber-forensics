from features.extractor import extract_features
from features.encoder import encode_features
from detection.rule_engine import rule_based_detection
from detection.statistical import statistical_detection
from detection.ml_model import train_isolation_forest, predict
from evaluation.metrics import evaluate

X = []
labels = []
rule_preds = []

for log in normalized_logs:  # load from JSONL

    features = extract_features(log)

    encoded = encode_features(features)
    X.append(encoded)

    labels.append(features["label"])

    rule_preds.append(rule_based_detection(features))


# --- Statistical ---
stat_preds = statistical_detection(X)

# --- ML ---
model = train_isolation_forest(X)
ml_preds = predict(model, X)

# --- Evaluate ---
print("Rule:", evaluate(rule_preds, labels))
print("Statistical:", evaluate(stat_preds, labels))
print("ML:", evaluate(ml_preds, labels))