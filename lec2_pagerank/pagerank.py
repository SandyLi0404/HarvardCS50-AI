import os
import random
import re
import sys

DAMPING = 0.85 # damping factor
SAMPLES = 10000 # number of samples use to estimate PageRank

# run: python lec2_pagerank\pagerank.py "D:\cs50\projects\lec2_pagerank\corpus0"

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


def transition_model(corpus:dict, page:str, damping_factor:float) -> dict:
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    outgoing = corpus[page]
    distribution = {}
    # if no outgoing page, choose randomly among all pages
    if outgoing is None:
        for key in corpus:
            distribution[key] = 1/len(corpus)
    # if page has outgoing page
    else:
        outgoing_p = damping_factor/len(outgoing) + (1-damping_factor)/len(corpus) # probability for a linked page
        other_p = (1-damping_factor)/len(corpus) # probability of choosing a unlinked page 
        for key in corpus:
            if key in outgoing:
                distribution[key] = outgoing_p
            else:
                distribution[key] = other_p
    return distribution


def sample_pagerank(corpus:dict, damping_factor:float, n:int) -> dict:
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {} # dict to return
    start = random.randint(0, len(corpus)-1) # random starting page
    sample = None
    for index, key in enumerate(corpus): # initialize pagerank dict with num of samples
        if (index == start):
            pagerank[key] = 1
            sample = key
        else:
            pagerank[key] = 0
    count = n # tracking loop times
    while(count > 0):
        distr = transition_model(corpus=corpus, page=sample, damping_factor=damping_factor)
        keys = [] # list of all keys in the corpus
        p = [] # list of probabilities of all keys in the corpus
        for k in distr:
            keys.append(k)
            p.append(distr[k])
        sample = random.choices(keys, weights=p, k=1)[0] # generate 1 sample based on the distribution
        pagerank[sample] += 1
        count -= 1
    for key in pagerank:
        pagerank[key] /= n # transform to proportion
    return pagerank

def iterate_pagerank(corpus:dict, damping_factor:float) -> dict:
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {}
    n = len(corpus)
    for key in corpus: # initialize pagerank to 1 / N
        pagerank[key] = 1 / n
    loop = True # change of pagerank value > 0.001
    while (loop):
        pagerank_old = pagerank.copy() # store old pagerank values
        for p in pagerank:
            pagerank[p] = (1 - damping_factor) / n
            for i in corpus:
                if (p in corpus[i]) or (len(corpus[i]) == 0): # i is an incoming page of p
                    num_links = len(corpus[i]) # the number of links on page key
                    if (num_links == 0): # the page has no links = having 1 link for every page
                        num_links = n
                    pagerank[p] += (damping_factor * pagerank[i] / num_links)
        loop = False
        for key in pagerank:
            if (abs(pagerank[key] - pagerank_old[key]) > 0.001): # if not converge, repeat
                loop = True
                break
    return pagerank


if __name__ == "__main__":
    main()
