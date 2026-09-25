import re

from models import (
    load_jobs,
    load_labels,
    save_labels,
    load_preferences,
    save_preferences
)

from ml import (
    extract_features,
    train_model
)


def get_words(text):
    return re.findall(r"[a-z]+", text.lower())


def get_matched_keywords(job, keywords):
    combined_text = f"{job.title} {job.description}".lower()
    combined_words = get_words(combined_text)

    matched = []

    for keyword in keywords:
        if " " in keyword:
            if keyword in combined_text:
                matched.append(keyword)
        else:
            if keyword in combined_words:
                matched.append(keyword)

    return matched


def matches_preferences(job, preferred_keywords):
    return len(get_matched_keywords(job, preferred_keywords)) > 0


def matches_seniority(job, seniority_keywords):
    return len(get_matched_keywords(job, seniority_keywords)) > 0


jobs = load_jobs("data/jobs.json")


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

filtered_jobs = [
    job for job in jobs
    if matches_preferences(job, preferred_keywords)
    and matches_seniority(job, seniority_keywords)
]

print(f"{len(filtered_jobs)} jobs matched your preferences.")

for job in filtered_jobs:
    job_id_str = str(job.job_id)

    if job_id_str in labels:
        continue

    matched_topic = get_matched_keywords(job, preferred_keywords)
    matched_seniority = get_matched_keywords(job, seniority_keywords)

    print(f"\n'{job.title}' at {job.company}")
    print(f"  Topic keywords found: {matched_topic}")
    print(f"  Seniority keywords found: {matched_seniority}")

    response = input("Interested? (y/n): ")

    labels[job_id_str] = 1 if response.strip().lower() == "y" else 0
    save_labels(labels, "data/labels.json")


idf_scores = None


X = []
y = []

for job in jobs:
    X.append(extract_features(job, idf_scores))

    job_id_str = str(job.job_id)

    if job_id_str in labels:
        y.append(labels[job_id_str])
    else:
        y.append(label_job(job.title))


model = train_model(X, y)

print()
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
    reverse=True
)

for job, probability in ranked[:20]:
    print(job.title, probability[1])