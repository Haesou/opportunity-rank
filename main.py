import heapq

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
                index[word] = set()

            index[word].add(job)

    return index

def search(query, index):
    query_words = tokenize(query)

    results = set()

    for word in query_words:
        if word in index:
            results.update(index[word])

    return results

def rank_jobs(query, index):
    query_words = tokenize(query)

    scores = {}

    for word in query_words:
        if word in index:
            for job in index[word]:
                if job not in scores:
                    scores[job] = 0

                scores[job] += 1

    return scores

def top_k_jobs(scores, k):
    heap = []

    for job in scores:
        heapq.heappush(heap, (scores[job], job.title, job))

        if len(heap) > k:
            heapq.heappop(heap)

    return heap

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

scores = rank_jobs("python backend", index)

for job, score in scores.items():
    print(job.title, score)

top_jobs = top_k_jobs(scores, 2)

for score, title, job in top_jobs:
    print(job.title, score)