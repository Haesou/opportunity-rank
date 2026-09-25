from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from collections import Counter

from models import (
    load_jobs,
    load_labels
)
from search import compute_idf
from ml import (
    extract_features,
    train_model
)


jobs = load_jobs("data/jobs.json")
labels = load_labels("data/labels.json")

labeled_jobs = [
    job for job in jobs
    if str(job.job_id) in labels
]

print(f"Evaluating on {len(labeled_jobs)} real labeled jobs")

idf_scores = compute_idf(jobs)

X = []
y = []

for job in labeled_jobs:
    X.append(
        extract_features(job, idf_scores)
    )
    y.append(labels[str(job.job_id)])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = train_model(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Test accuracy: {accuracy:.2f}")
print(f"Test set size: {len(y_test)}")

cm = confusion_matrix(y_test, predictions)
print("Confusion matrix:")
print(cm)

majority_class = Counter(y_test).most_common(1)[0][0]
baseline_accuracy = y_test.count(majority_class) / len(y_test)
print(f"Baseline (always predict {majority_class}): {baseline_accuracy:.2f}")