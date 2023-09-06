from fuzzywuzzy import process as fuzz_process
from fuzzywuzzy import fuzz


def get_matched_item(query: str, choice_list: list or dict, threshold: int,
                     limit: int, fuzzy_scorer=fuzz.token_sort_ratio):
    """
    extract the best matched items from list
    @param fuzzy_scorer: decide the scorer, default is fuzz.token_sort_ratio
    @param query: query string
    @param choice_list: string list to be compared
    @param threshold: the threshold of matching score
    @param limit: the number of items to be extracted
    @return: item list with matching score beyond threshold
    """

    return fuzz_process.extractBests(query=query, choices=choice_list, scorer=fuzzy_scorer,
                                     score_cutoff=threshold, limit=limit)
