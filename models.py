import json


class Job:
    def __init__(self, job_id, title, company, location, description, url,
                 salary=None, employment_type=None, date_posted=None):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.url = url
        self.salary = salary
        self.employment_type = employment_type
        self.date_posted = date_posted

def load_preferences(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_preferences(preferences, filename):
    with open(filename, "w") as file:
        json.dump(preferences, file, indent=2)


def load_labels(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_labels(labels, filename):
    with open(filename, "w") as file:
        json.dump(labels, file, indent=2)

def load_jobs(filename):
    jobs = []

    with open(filename, "r") as file:
        data = json.load(file)

    for job_data in data:
        job = Job(
            job_data["id"],
            job_data["title"],
            job_data["company"],
            job_data["location"],
            job_data["description"],
            job_data["url"],
            salary=job_data.get("salary"),
            employment_type=job_data.get("employment_type"),
            date_posted=job_data.get("date_posted")
        )

        jobs.append(job)

    return jobs