

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def main():
    print("=" * 65)
    print("AI/ML PRACTICAL: k-NN CLASSIFICATION MODEL EVALUATION")
    print("=" * 65)

 
    X_train = [
        [1, 1],
        [2, 2],
        [3, 2],
        [6, 5],
        [7, 6],
        [8, 7]
    ]
    y_train = [
        "Fail",
        "Fail",
        "Fail",
        "Pass",
        "Pass",
        "Pass"
    ]

 
    X_test = [
        [2, 1],
        [3, 3],
        [6, 6],
        [7, 5]
    ]
    y_true = [
        "Fail",
        "Fail",
        "Pass",
        "Pass"
    ]

    print("[INFO] Dataset loaded successfully.")
    print(f" -> Training Samples: {len(X_train)}")
    print(f" -> Testing Samples : {len(X_test)}")


    k_value = 3
    model = KNeighborsClassifier(n_neighbors=k_value)


    model.fit(X_train, y_train)
    print(f"[INFO] KNeighborsClassifier initialized and trained (k={k_value}).")


    y_pred = model.predict(X_test)

    print("\n" + "-" * 55)
    print("INDIVIDUAL SAMPLE PREDICTION COMPARISON")
    print("-" * 55)
    for idx, (features, actual, predicted) in enumerate(zip(X_test, y_true, y_pred), start=1):
        status = "Correct" if actual == predicted else "X Incorrect"
        print(f"Sample {idx} | Input Features: {features} | Actual: {actual:<5} | Predicted: {predicted:<5} | {status}")


    accuracy = accuracy_score(y_true, y_pred)
    conf_matrix = confusion_matrix(y_true, y_pred, labels=["Fail", "Pass"])

    print("\n" + "-" * 55)
    print("QUANTITATIVE PERFORMANCE METRICS")
    print("-" * 55)
    print(f"Accuracy Score : {accuracy:.4f} ({accuracy * 100:.1f}%)")
    print("\nConfusion Matrix:")
    print("              Predicted Fail  Predicted Pass")
    print(f"Actual Fail [ {conf_matrix[0][0]:^14} {conf_matrix[0][1]:^14} ]")
    print(f"Actual Pass [ {conf_matrix[1][0]:^14} {conf_matrix[1][1]:^14} ]")

    print("\nDetailed Classification Report:")
    print("-" * 35)
    print(classification_report(y_true, y_pred, labels=["Fail", "Pass"], zero_division=0))
    print("=" * 65)

if __name__ == "__main__":
    main()
