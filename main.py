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

seniority_keywords = [
    "intern"
]

preferred_keywords = [
    "software engineer",
    "backend engineer",
    "full stack engineer",
    "machine learning",
    "ai engineer",
    "ml engineer"
]

def label_job(title):
    title_lower = title.lower()

    is_entry_level = any(
        keyword in title_lower
        for keyword in seniority_keywords
    )

    matches_topic = any(
        keyword in title_lower
        for keyword in preferred_keywords
    )

    return 1 if (is_entry_level and matches_topic) else 0


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

print(y)

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