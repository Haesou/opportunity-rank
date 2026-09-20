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


idf_scores = compute_idf(jobs)


X = []

for job in jobs:
    X.append(
        extract_features(
            job,
            query,
            idf_scores
        )
    )


y = [
    1,  # Software Engineering
    1,  # Backend Engineering
    1,  # Machine Learning
    1,  # Data Science
    0,  # Frontend
    1,  # AI Research
    1,  # Systems Software
    1,  # Quantitative Research
    0,  # Cybersecurity
    1,  # Full Stack
    1,  # NLP
    0   # Product Management
]


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