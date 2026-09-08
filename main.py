class Job:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description

def tokenize(text):
    text = text.lower()
    words = text.split()

    cleaned_words = []

    for word in words:
        cleaned_word = ""

        for char in word:
            if char.isalnum():
                cleaned_word += char

        if cleaned_word:
            cleaned_words.append(cleaned_word)

    return cleaned_words

def build_inverted_index(jobs):
    index = {}

    for job in jobs:
        words = tokenize(job.description)

        for word in words:
            if word not in index:
                index[word] = []

            index[word].append(job)

    return index

job1 = Job(
    "Software Engineering Intern",
    "Example Corp",
    "Looking for a student with Python, algorithms, and backend experience."
)

job2 = Job(
    "Backend Engineering Intern",
    "Another Corp",
    "Seeking a student with Java, backend systems, and database experience."
)

jobs = [job1, job2]

index = build_inverted_index(jobs)

for job in index["backend"]:
    print(job.title)