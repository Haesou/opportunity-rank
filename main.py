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
    "Nova Systems",
    "Looking for a student with Python, algorithms, data structures, and backend development experience."
)

job2 = Job(
    "Backend Engineering Intern",
    "CloudForge",
    "Seeking a student with Java, backend systems, APIs, databases, and distributed systems experience."
)

job3 = Job(
    "Machine Learning Intern",
    "Visionary AI",
    "Looking for a student with Python, machine learning, statistics, scikit-learn, and data analysis experience."
)

job4 = Job(
    "Data Science Intern",
    "QuantLeaf",
    "Seeking a student with Python, pandas, statistics, data visualization, machine learning, and SQL experience."
)

job5 = Job(
    "Frontend Engineering Intern",
    "PixelWorks",
    "Looking for a student with JavaScript, HTML, CSS, React, and frontend web development experience."
)

job6 = Job(
    "AI Research Intern",
    "DeepMind Labs",
    "Seeking a student interested in artificial intelligence, Python, neural networks, machine learning, and research."
)

job7 = Job(
    "Systems Software Intern",
    "CoreStack",
    "Looking for a student with C++, operating systems, algorithms, data structures, and low-level programming experience."
)

job8 = Job(
    "Quantitative Research Intern",
    "AlphaBridge",
    "Seeking a student with Python, mathematics, probability, statistics, algorithms, and quantitative modeling experience."
)

job9 = Job(
    "Cybersecurity Intern",
    "SecureNet",
    "Looking for a student with Python, networking, Linux, security, cryptography, and systems experience."
)

job10 = Job(
    "Full Stack Engineering Intern",
    "LaunchPad",
    "Seeking a student with Python, JavaScript, APIs, databases, backend development, and frontend development experience."
)

job11 = Job(
    "NLP Engineering Intern",
    "LanguageWorks",
    "Looking for a student with Python, natural language processing, machine learning, embeddings, and text analysis experience."
)

job12 = Job(
    "Product Management Intern",
    "BuildFlow",
    "Seeking a student with communication, product strategy, user research, project management, and business analysis experience."
)

jobs = [
    job1, job2, job3, job4, job5, job6,
    job7, job8, job9, job10, job11, job12
]

index = build_inverted_index(jobs)

scores = rank_jobs("python backend", index)

# for job, score in scores.items():
#     print(job.title, score)

top_jobs = top_k_jobs(scores, 5)

top_jobs.sort(reverse=True)

for score, title, job in top_jobs:
    print(job.title, score)