from sklearn.linear_model import LogisticRegression

from preprocessing import tokenize
from search import (
    compute_tfidf,
    compute_query_tfidf,
    cosine_similarity
)


def extract_features(
    job,
    query,
    idf_scores
):
    job_tfidf = compute_tfidf(
        job,
        idf_scores
    )

    query_tfidf = compute_query_tfidf(
        query,
        idf_scores
    )

    cosine_similarity_val = (
        cosine_similarity(
            job_tfidf,
            query_tfidf
        )
    )

    words = tokenize(job.description)

    return [
        cosine_similarity_val,
        1 if "python" in words else 0,
        1 if "machin" in words else 0,
        1 if "learn" in words else 0,
        1 if "algorithm" in words else 0,
        1 if "mathemat" in words else 0,
        1 if "statist" in words else 0,
        1 if "backend" in words else 0,
        1 if "frontend" in words else 0
    ]


def train_model(X, y):
    model = LogisticRegression()

    model.fit(X, y)

    return model