from sklearn.linear_model import LogisticRegression
import re

from preprocessing import tokenize
from search import (
    compute_tfidf,
    compute_query_tfidf,
    cosine_similarity
)


COMPANIES = [
    "stripe",
    "airbnb",
    "figma",
    "anthropic",
    "databricks",
    "coinbase",
    "cloudflare",
    "lyft"
]

WEST_COAST_KEYWORDS = [
    "san francisco",
    "sf",
    "seattle",
    "bay area"
]

EAST_COAST_KEYWORDS = [
    "new york",
    "nyc",
    "ny"
]

TEAM_AREA_KEYWORDS = {
    "payments_billing": ["payments", "billing", "money movement"],
    "infrastructure_platform": ["infrastructure", "platform", "cloud", "distributed systems"],
    "security_risk": ["security", "risk", "fraud", "trust", "safety"],
    "data_ml_ai": ["data", "machine learning", "ai", "ml"]
}

def get_team_area_flags(job):
    combined_text = f"{job.title} {job.description}".lower()

    flags = []

    for area, keywords in TEAM_AREA_KEYWORDS.items():
        matched = any(keyword in combined_text for keyword in keywords)
        flags.append(1 if matched else 0)

    return flags

def get_title_words(title):
    return re.findall(r"[a-z]+", title.lower())

def extract_features(
    job,
    idf_scores=None,
    query=None
):
    words = tokenize(job.description)
    job_words = get_title_words(job.title)

    is_entry = (
        "intern" in job_words
        or "new" in job_words and "grad" in job_words
    )

    is_staff_plus = (
        "staff" in job_words
        or "principal" in job_words
    )

    is_mid = not is_entry and not is_staff_plus

    company_lower = job.company.lower()
    company_flags = [
        1 if company_lower == company else 0
        for company in COMPANIES
    ]

    location_lower = (job.location or "").lower()

    is_west_coast = any(
        keyword in location_lower
        for keyword in WEST_COAST_KEYWORDS
    )

    is_east_coast = any(
        keyword in location_lower
        for keyword in EAST_COAST_KEYWORDS
    )

    team_area_flags = get_team_area_flags(job)

    features = []

    if query is not None:
        job_tfidf = compute_tfidf(job, idf_scores)
        query_tfidf = compute_query_tfidf(query, idf_scores)
        cosine_similarity_val = cosine_similarity(job_tfidf, query_tfidf)
        features.append(cosine_similarity_val)

    features.extend([
        1 if "python" in words else 0,
        1 if "machin" in words else 0,
        1 if "learn" in words else 0,
        1 if "algorithm" in words else 0,
        1 if "mathemat" in words else 0,
        1 if "statist" in words else 0,
        1 if "backend" in words else 0,
        1 if "frontend" in words else 0,
        1 if is_entry else 0,
        1 if is_mid else 0,
        1 if is_staff_plus else 0,
        *company_flags,
        1 if is_west_coast else 0,
        1 if is_east_coast else 0,
        *team_area_flags
    ])

    return features


def train_model(X, y):
    model = LogisticRegression()

    model.fit(X, y)

    return model