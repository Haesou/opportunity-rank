import json


class Job:
    def __init__(self, job_id, title, company, location, description, url):
        self.job_id = job_id
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.url = url


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
            job_data["url"]
        )

        jobs.append(job)

    return jobs