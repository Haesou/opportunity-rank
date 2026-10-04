import re
import html
import json
import requests


RELEVANT_KEYWORDS = [
    "software engineer",
    "software engineering",
    "backend engineer",
    "frontend engineer",
    "full stack engineer",
    "data scientist",
    "data engineer",
    "machine learning engineer",
    "machine learning",
    "ml engineer",
    "ai engineer",
    "security engineer",
    "cybersecurity"
]


def fetch_job_list(company_slug):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"

    response = requests.get(url)

    if response.status_code != 200:
        print(f"  Skipping {company_slug}: HTTP {response.status_code}")
        return []

    return response.json().get("jobs", [])


def is_relevant(title):
    title_lower = title.lower()

    for keyword in RELEVANT_KEYWORDS:
        if keyword in title_lower:
            return True

    return False


def map_job(raw_job, company_slug):
    location = (raw_job.get("location") or {}).get("name")

    return {
        "id": raw_job["id"],
        "title": raw_job["title"],
        "company": raw_job["company_name"],
        "company_slug": company_slug,
        "location": location,
        "url": raw_job["absolute_url"],
        "date_posted": raw_job["updated_at"],
        "description": None,
        "salary": None,
        "employment_type": None
    }


def strip_html_tags(text):
    return re.sub(r"<[^>]+>", " ", text)


def clean_description(raw_html):
    unescaped = html.unescape(raw_html)
    text_only = strip_html_tags(unescaped)
    return text_only.strip()


def fetch_description(company_slug, job_id):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs/{job_id}?content=true"

    response = requests.get(url)
    data = response.json()

    return clean_description(data["content"])


def save_jobs(jobs, filename):
    with open(filename, "w") as file:
        json.dump(jobs, file, indent=2)


COMPANY_SLUGS = [
    "stripe", "airbnb", "figma", "anthropic", "databricks",
    "coinbase", "cloudflare", "lyft",
    "andurilindustries", "gleanwork", "gallup", "dvtrading",
    "togetherai", "spacex", "pdtpartners", "astranis",
    "affirm", "imc", "scaleai", "doordashusa", "drweng",
    "aquaticcapitalmanagement"
]


all_mapped_jobs = []

for company_slug in COMPANY_SLUGS:
    print(f"Fetching jobs for {company_slug}...")

    jobs = fetch_job_list(company_slug)

    filtered_jobs = [
        job for job in jobs
        if is_relevant(job["title"])
    ]

    mapped_jobs = [map_job(job, company_slug) for job in filtered_jobs]

    for job in mapped_jobs:
        try:
            job["description"] = fetch_description(
                company_slug,
                job["id"]
            )
        except Exception:
            job["description"] = ""

    all_mapped_jobs.extend(mapped_jobs)

    print(f"  -> {len(mapped_jobs)} relevant jobs found")


save_jobs(all_mapped_jobs, "data/jobs.json")
print(f"\nSaved {len(all_mapped_jobs)} total jobs to data/jobs.json")