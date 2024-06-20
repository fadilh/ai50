import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    all_pages = list(corpus.keys())
    linked_pages = corpus[page]
    prob_dist = {}

    for page in all_pages:
        prob_dist[page] = 0

    if len(linked_pages) == 0:
        for page in all_pages:
            prob_dist[page] += 1 / len(all_pages)
        return prob_dist

    for page in prob_dist:
        prob_dist[page] += (1 - damping_factor) / len(all_pages)
        prob_dist[page] += damping_factor / len(linked_pages) if page in linked_pages else 0
    
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    all_pages = list(corpus.keys())
    sample_page = random.choice(all_pages)
    
    for page in all_pages:
        page_rank[page] = 0

    for _ in range(0, n-1):
        prob_dist = transition_model(corpus=corpus, page=sample_page, damping_factor=damping_factor)
        rand_prob = random.random()
        tot_prob = 0
        for page, prob in prob_dist.items():
            tot_prob += prob
            if rand_prob <= tot_prob:
                sample_page = page
                break
        page_rank[sample_page] += 1

    for page, num_visits in page_rank.items():
        page_rank[page] = num_visits / n

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}
    N = len(corpus)
    for page in corpus:
        page_rank[page] = 1 / N
    
    changed = True
    while changed:
        changed = False
        for page in page_rank:
            summation = 0
            for i in page_rank:
                if len(corpus[i]) == 0:
                    summation += page_rank[i] / N
                elif page in corpus[i]:
                    summation += page_rank[i] / len(corpus[i])
            new_pr = ((1 - damping_factor) / N) + (damping_factor * summation) 
            changed = True if abs(page_rank[page] - new_pr) > 0.001 else changed
            page_rank[page] = new_pr

    return page_rank
            

if __name__ == "__main__":
    main()