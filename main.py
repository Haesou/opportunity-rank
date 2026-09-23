from models import load_jobs
from search import compute_idf

from models import (
    load_jobs,
    load_labels,
    save_labels,
    load_preferences,
    save_preferences
)

from search import (
    compute_idf,
    rank_jobs_tfidf
)

from ml import (
    extract_features,
    train_model
)


jobs = load_jobs("data/jobs.json")

query = input("What kind of job are you looking for? ")


preferences = load_preferences("data/preferences.json")

if preferences is None:
    seniority_input = input(
        "What seniority keywords are you interested in? (comma-separated, e.g. intern,new grad): "
    )
    topic_input = input(
        "What topic keywords are you interested in? (comma-separated, e.g. machine learning,backend): "
    )

    preferences = {
        "seniority_keywords": [
            word.strip().lower()
            for word in seniority_input.split(",")
        ],
        "preferred_keywords": [
            word.strip().lower()
            for word in topic_input.split(",")
        ]
    }

    save_preferences(preferences, "data/preferences.json")

seniority_keywords = preferences["seniority_keywords"]
preferred_keywords = preferences["preferred_keywords"]

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

labels = load_labels("data/labels.json")

scores = rank_jobs_tfidf(query, jobs)
top_jobs = sorted(
    scores.items(),
    key=lambda item: item[1],
    reverse=True
)[:10]

for job, score in top_jobs:
    job_id_str = str(job.job_id)

    if job_id_str in labels:
        continue

    response = input(
        f"Interested in '{job.title}' at {job.company}? (y/n): "
    )
    labels[job_id_str] = 1 if response.strip().lower() == "y" else 0

save_labels(labels, "data/labels.json")

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

    job_id_str = str(job.job_id)

    if job_id_str in labels:
        y.append(labels[job_id_str])
    else:
        y.append(label_job(job.title))


model = train_model(X, y)

print("coefficients:")
print(model.coef_)

print()

print("intercept:")
print(model.intercept_)

print()


probabilities = model.predict_proba(X)

ranked = sorted(
    zip(jobs, probabilities),
    key=lambda pair: pair[1][1],
    reverse = True
)

for job, probability in ranked[:20]:
    print(
        job.title,
        probability[1]
    )