from utils.jsonl_reader import read_jsonl

from features.extractor import extract_features
from features.encoder import encode_features

from detection.rule_engine import rule_based_detection
from detection.statistical import statistical_detection
from detection.ml_model import train_isolation_forest, predict

from detection.supervised_model import train_rf, predict_rf

from evaluation.metrics import evaluate

from sklearn.model_selection import train_test_split
from explainability.explainer import explain_prediction
import numpy as np


def main():
    file_path = "output/network.jsonl"

    X = []
    labels = []
    rule_preds = []
    all_features = []

    # --- Load logs ---
    for log in read_jsonl(file_path):

        features = extract_features(log)
        all_features.append(features)

        label_raw = features.get("label")
        if label_raw is None:
            continue

        label_raw = str(label_raw).strip().lower()

        # --- Encode features ---
        encoded = encode_features(features)
        if encoded is None:
            continue

        X.append(encoded)

        # --- Convert label ---
        if label_raw in ["normal", "benign"]:
            labels.append(0)
        else:
            labels.append(1)

        # --- Rule prediction ---
        rule_preds.append(rule_based_detection(features))

    # --- Debug info ---
    print("\nTOTAL SAMPLES:", len(X))
    print("SAMPLE X:", X[:5])

    print("\nLabel Distribution:")
    print("Normal:", labels.count(0))
    print("Attack:", labels.count(1))

    if len(X) < 10:
        print("⚠️ Not enough data")
        return

    # --- Train/Test Split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, labels, test_size=0.2, random_state=42
    )

    # --- Align rule predictions with test set ---
    rule_test_preds = rule_preds[len(X_train):]

    # --- Statistical ---
    stat_preds = statistical_detection(X_test)

    # --- Isolation Forest ---
    iso_model = train_isolation_forest(X_train)
    ml_preds = predict(iso_model, X_test)

    # --- Random Forest (Supervised) ---
    rf_model = train_rf(X_train, y_train)
    rf_preds = predict_rf(rf_model, X_test)

    # --- Explain a few predictions ---
    print("\nSample Explanations:\n")

    for i in range(5):
        explanation = explain_prediction(all_features[i], rf_preds[i])
        print(f"Prediction: {rf_preds[i]} | Explanation: {explanation}")

    # --- Debug prediction sets ---
    print("\nPrediction Sets:")
    print("Rule:", set(rule_test_preds))
    print("Stat:", set(stat_preds))
    print("ML:", set(ml_preds))
    print("RF:", set(rf_preds))

    # --- Evaluate ---
    print("\nResults:")
    print("Rule:", evaluate(rule_test_preds, y_test))
    print("Statistical:", evaluate(stat_preds, y_test))
    print("IsolationForest:", evaluate(ml_preds, y_test))
    print("RandomForest:", evaluate(rf_preds, y_test))

    feature_names = [
        "protocol",
        "destination_port",
        "event_type",
        "has_ip",
        "is_high_port",
        "is_well_known_port",
        "is_dns",
        "is_ntp",
        "is_mdns",
        "is_udp",
        "is_tcp"
    ]

    importances = rf_model.feature_importances_

    # sort features
    indices = np.argsort(importances)[::-1]

    print("\nFeature Importance (Top Features):")
    for i in indices[:10]:
        print(f"{feature_names[i]}: {importances[i]:.4f}")


if __name__ == "__main__":
    main()