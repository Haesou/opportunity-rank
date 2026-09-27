# opportunity-rank

A personalized computer science related job/internship recommendation system that goes beyond keyword search by learning individual preferences within an already-filtered eligible pool of real job postings.

## Why?

I am currently in the process of searching for a software engineering internship. From my experience, looking through a specific company's job postings through their career page was complicated and time exhaustive. Websites that congregate job postings, such as earlycareerradar.com, are useful to some extent but inevitably are built to serve job seekers broadly. With breadth comes a cost: the more industries a search engine tries to cover, the less it can tailor to a user's specific needs or interests. I wanted to build something narrow enough to actually reflect what I was looking for.

## What it does

1. Pulls real job postings from 8 companies (Stripe, Airbnb, Figma, Anthropic, Databricks, Coinbase, Cloudflare, Lyft) via the Greenhouse public API
2. Filters ~670 postings down to a small eligible pool based on the user's stated seniority, topic, and coding language preferences
3. Asks the user to label jobs in that eligible pool as interested/not interested (in practice, this will look more like an interested/uninterested button next to a job posting)
4. Trains a logistic regression model on those real labels (falling back to a keyword rule for anything unlabeled)
5. Ranks *all* jobs — including ones never manually reviewed — by predicted interest

## Architecture

import_jobs.py → fetches, filters, cleans real postings → data/jobs.json
models.py → Job schema; load/save for jobs, labels, preferences
preprocessing.py→ tokenization (stopwords, stemming)
search.py → TF-IDF, cosine similarity (used for future live-search features)
ml.py → feature extraction (25 features) + logistic regression training
main.py → orchestrates: filter → label → train → rank
evaluate.py → train/test split, accuracy, confusion matrix, baseline comparison

## Key design decisions

**Eligibility filtering vs. personalization are different problems.** Searching for jobs is a very binary process. There are hard eligibility constraints (topic, seniority, language) that bar candidates from applying at all. Early versions of opportunity-rank conflated eligibility with preferences by training the model on every job in the dataset, regardless of whether the user was actually eligible for it. This sometimes lead to the system recommending jobs that scored well on preference-related features but that the user wasn't qualified for. This was fixed by introducing an eligibility filter before training, so the model only ever learns from and ranks jobs the user is actually eligible to apply to.

**Eligibility significantly overpowers personal prefernces.** Beggars can't be choosers. Candidates cannot be dissuaded from applying just because of preferences because the job market, especially jobs related to computer science, are really competative. Thus the introduction of the eligibility filter brought on a significant design flaw: most people would mark "interested" in a job that they are eligible for. This meant that the regression model could not learn much about a user's preferences. Yet a candidate cannot possibly apply for every single job posting they are eligible in the world. So the real question was never just eligibility, it's priority. This led to a conclusion: users shouldn't label jobs based on whether they're "interested," but on whether they're "really interested". Reserving a "yes" for jobs worth prioritizing over other eligible options, not just ones they'd technically take.

## Current features (25 total)

- Topic keyword matches (python, machine learning, algorithms, statistics, backend, frontend, etc.)
- Seniority (entry / mid / staff+, one-hot)
- Company (one-hot across 8 companies)
- Region (US West Coast / East Coast flags)
- Team/product area (payments/billing, infrastructure/platform, security/risk, data/ML/AI — derived from real keyword frequency, non-exclusive)

## Known limitations

- Real labeled data is still small (~30-60 examples), so specific learned weights should be treated as directionally suggestive, not reliable
- Seniority currently collapses "intern" and "new grad" into one feature, despite being separate stated preferences
- No live UI — everything runs via terminal prompts
- Salary/employment_type fields exist in the schema but are almost always null from Greenhouse and unused in features

## Possible future work

- Richer NLP (semantic similarity instead of exact keyword matches)
- Remote/flexibility as a ranking feature
- Real behavioral signals (clicks/saves/applies) instead of manual labeling
- An actual UI, so labeling and browsing aren't terminal prompts