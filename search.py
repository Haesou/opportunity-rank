import heapq
import math

from preprocessing import tokenize


def compute_tf(job):
    tf = {}
    words = tokenize(job.description)

    for word in words:
        if word not in tf:
            tf[word] = 0

        tf[word] += 1

    for word in tf:
        tf[word] = tf[word] / len(words)

    return tf


def build_inverted_index(jobs):
    index = {}

    for job in jobs:
        words = tokenize(job.description)

        for word in words:
            if word not in index:
                index[word] = set()

            index[word].add(job)

    return index


def compute_idf(jobs):
    idf_scores = {}

    index = build_inverted_index(jobs)

    for word in index:
        idf_scores[word] = math.log(
            len(jobs) / len(index[word])
        )

    return idf_scores


def compute_tfidf(job, idf_scores):
    tfidf = {}

    tf_scores = compute_tf(job)

    for word in tf_scores:
        tfidf[word] = (
            tf_scores[word] * idf_scores[word]
        )

    return tfidf


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
        heapq.heappush(
            heap,
            (scores[job], job.title, job)
        )

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
        tf_score[word] = (
            tf_score[word] / len(words)
        )

    for word in tf_score:
        if word in idf_scores:
            query_tfidf[word] = (
                tf_score[word]
                * idf_scores[word]
            )

    return query_tfidf


def dot_product(vector1, vector2):
    dot_product_value = 0

    for word in vector1:
        if word in vector2:
            dot_product_value += (
                vector1[word]
                * vector2[word]
            )

    return dot_product_value


def magnitude(vector):
    magnitude_value = 0

    for word in vector:
        magnitude_value += vector[word] ** 2

    return magnitude_value ** (1 / 2)


def cosine_similarity(vector1, vector2):
    magnitude_vector1 = magnitude(vector1)
    magnitude_vector2 = magnitude(vector2)

    if (
        magnitude_vector1 == 0
        or magnitude_vector2 == 0
    ):
        return 0

    return (
        dot_product(vector1, vector2)
        / (
            magnitude_vector1
            * magnitude_vector2
        )
    )


def rank_jobs_tfidf(query, jobs):
    final_scores = {}

    global_idf = compute_idf(jobs)

    query_tfidf = compute_query_tfidf(
        query,
        global_idf
    )

    for job in jobs:

        job_tfidf = compute_tfidf(
            job,
            global_idf
        )

        cosine_similarity_value = (
            cosine_similarity(
                query_tfidf,
                job_tfidf
            )
        )

        final_scores[job] = (
            cosine_similarity_value
        )

    return final_scores