from models import load_jobs

from search import compute_idf

from ml import (
    extract_features,
    train_model
)


jobs = load_jobs("data/jobs.json")


query = (
    "python machine learning "
    "algorithms mathematics"
)

preferred_keywords = [
    "machine learning",
    "ai engineer",
    "data scientist",
    "data engineer"
]

def label_job(title):
    title_lower = title.lower()

    for keyword in preferred_keywords:
        if keyword in title_lower:
            return 1

    return 0


idf_scores = compute_idf(jobs)


X = []
y = []

for job in jobs:
    X.append(
        extract_features(
            job,
            query,
            idf_scores
        )
    )
    y.append(label_job(job.title))


model = train_model(X, y)


print("coefficients:")
print(model.coef_)

print()

print("intercept:")
print(model.intercept_)

print()


probabilities = model.predict_proba(X)


for job, probability in zip(
    jobs,
    probabilities
):
    print(
        job.title,
        probability[1]
    )