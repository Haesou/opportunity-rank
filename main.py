import heapq
import math

class Job:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description

STOP_WORDS = {
    "a", "an", "the", "and", "or", "for",
    "with", "in", "on", "to", "of", "is",
    "are", "student", "looking", "seeking"
}

def tokenize(text):
    text = text.lower()
    words = text.split()

    cleaned_words = []

    for word in words:
        cleaned_word = ""

        for char in word:
            if char.isalnum():
                cleaned_word += char

        if cleaned_word and cleaned_word not in STOP_WORDS:
            cleaned_words.append(cleaned_word)

    return cleaned_words

def compute_tf(job):
    tf = {}
    words = tokenize(job.description)

    for word in words:
        if word not in tf:
            tf[word] = 0
        tf[word] += 1

    for word in tf:
        tf[word] = tf[word]/len(words)

    return tf

def compute_idf(jobs):
    idf_scores = {}
    index = build_inverted_index(jobs)

    for word in index:
        idf_scores[word] = math.log(len(jobs) / len(index[word]))

    return idf_scores

def compute_tfidf(job, idf_scores):
    tfidf = {}
    tf_scores = compute_tf(job)

    for word in tf_scores:
        tfidf[word] = tf_scores[word] * idf_scores[word]

    return tfidf

def build_inverted_index(jobs):
    index = {}

    for job in jobs:
        words = tokenize(job.description)

        for word in words:
            if word not in index:
                index[word] = set()

            index[word].add(job)

    return index

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

def compute_query_tfidf(query, idf_scores):
    words = tokenize(query)
    query_tfidf = {}
    tf_score = {}

    for word in words:
        if word not in tf_score:
            tf_score[word] = 0
        tf_score[word] += 1

    for word in tf_score:
        tf_score[word] = tf_score[word]/len(words)

    for word in tf_score:
        if word in idf_scores:
            query_tfidf[word] = tf_score[word] * idf_scores[word]

    return query_tfidf

def dot_product(vector1, vector2):
    dot_product_value = 0

    for word in vector1:
        if word in vector2:
            dot_product_value += vector1[word] * vector2[word]

    return dot_product_value

def magnitude(vector):
    magnitude_value = 0

    for word in vector:
        magnitude_value += vector[word] ** 2

    return magnitude_value ** (1/2)

def cosine_similarity(vector1, vector2):
    magnitude_vector1 = magnitude(vector1)
    magnitude_vector2 = magnitude(vector2)
    
    if magnitude_vector1 == 0 or magnitude_vector2 == 0:
        return 0

    return (dot_product(vector1, vector2))/(magnitude_vector1 * magnitude_vector2)


    

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