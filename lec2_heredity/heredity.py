import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1]) # dict with parent info

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people:dict, one_gene:set, two_genes:set, have_trait:set) -> float:
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    prob = []
    for person in people:
        mother = people[person]["mother"] # mother's name
        father = people[person]["father"]

        if mother == None and father == None: # no info of parents, use unconditional probabilities
            if person in one_gene:
                if person in have_trait:
                    prob.append(PROBS["gene"][1] * PROBS["trait"][1][True])
                else:
                    prob.append(PROBS["gene"][1] * PROBS["trait"][1][False])
            elif person in two_genes:
                if person in have_trait:
                    prob.append(PROBS["gene"][2] * PROBS["trait"][2][True])
                else:
                    prob.append(PROBS["gene"][2] * PROBS["trait"][2][False])
            else:
                if person in have_trait:
                    prob.append(PROBS["gene"][0] * PROBS["trait"][0][True])
                else:
                    prob.append(PROBS["gene"][0] * PROBS["trait"][0][False])
        else: # with info of parents
            p_mom = inherit(parent=mother, one_gene=one_gene, two_genes=two_genes)
            p_dad = inherit(parent=father, one_gene=one_gene, two_genes=two_genes)
            if person in one_gene: # person has one gene
                # mom inherits and dad doesn't inherit, OR, dad inherits and mom doesn't
                prob.append(p_mom*(1-p_dad) + p_dad*(1-p_mom))
                if person in have_trait:
                    prob[-1] *= PROBS["trait"][1][True]
                else:
                    prob[-1] *= PROBS["trait"][1][False]
            elif person in two_genes: # person has two genes
                prob.append(p_mom*p_dad) # both mom and dad inherit
                if person in have_trait:
                    prob[-1] *= PROBS["trait"][2][True]
                else:
                    prob[-1] *= PROBS["trait"][2][False]
            else: # person has no gene
                prob.append((1-p_mom) * (1-p_dad)) # both mom and dad don't inherit
                if person in have_trait:
                    prob[-1] *= PROBS["trait"][0][True]
                else:
                    prob[-1] *= PROBS["trait"][0][False]
    joint_p = 1
    for p in prob: # multiply all persons probability to get the joint probability
        joint_p *= p
    return joint_p



def inherit(parent:str, one_gene:set, two_genes:set) -> float:
    """
    Compute the probability that a person would inherit the gene from parent
    """
    if parent in one_gene:
        return 0.5
    elif parent in two_genes:
        return 1 - PROBS["mutation"]
    else:
        return PROBS["mutation"]



def update(probabilities:dict, one_gene:set, two_genes:set, have_trait:set, p:float):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        num_gene = 1 if person in one_gene else 2 if person in two_genes else 0 # num of genes
        trait = True if person in have_trait else False # trait
        probabilities[person]["gene"][num_gene] += p # update gene field probability
        probabilities[person]["trait"][trait] += p # update trait field probability



def normalize(probabilities:dict):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # sum of p of different gene number
        gene_all = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + \
            probabilities[person]["gene"][2]
        # sum of p of different trait
        trait_all = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        for num_gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][num_gene] /= gene_all
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= trait_all

if __name__ == "__main__":
    main()
