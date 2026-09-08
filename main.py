class Job:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description


job1 = Job(
    "Software Engineering Intern",
    "Example Corp",
    "Looking for a student with Python, algorithms, and backend experience."
)

print(job1.title)
print(job1.company)
print(job1.description)