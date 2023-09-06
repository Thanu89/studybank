import os
import utils
from fuzzywuzzy import fuzz


def read_txt2dict(txt_file):
    with open(txt_file, 'r') as sf:
        raw_data = sf.readlines()
    dict_data = {}
    tokens_num = 0
    for i in range(len(raw_data)):
        sent_key = str(i)
        dict_data[sent_key] = raw_data[i].strip()
        tokens_num += len(raw_data[i].strip().split())
    os.remove(txt_file)
    return tokens_num, dict_data


def plag_check(paths: list, threshold: int = 70):
    """
    checking plagiarism between two txt files
    :param threshold: threshold of similarity between two strings, default is 70
    :param paths: two txt files to be compared
    :return: plagiarism and plagiarized sentences between origin and target
    """
    result_data = {
        "source_percent": 0,
        "target_percent": 0,
        "matched_text": "",
        "matches": []
    }
    print("\n----------------------------------------")
    print("Comparing two files...")
    source_tokens, source_data = read_txt2dict(paths[0])
    target_tokens, target_data = read_txt2dict(paths[1])
    plagiarized_sentences = []
    for _, target_sent in target_data.items():
        partial_match = utils.get_matched_item(query=target_sent,
                                               choice_list=source_data,
                                               threshold=threshold,
                                               limit=20,
                                               fuzzy_scorer=fuzz.WRatio)
        if partial_match == []:
            continue
        partial_match_dict = {}
        for sent, score, key in partial_match:
            partial_match_dict[key] = sent
        best_match_sent = utils.get_matched_item(query=target_sent,
                                                 choice_list=partial_match_dict,
                                                 threshold=threshold,
                                                 limit=1,
                                                 fuzzy_scorer=fuzz.ratio)
        if best_match_sent != []:
            matched_sent, score, _ = best_match_sent[0]
            sentence = {
                "source_sent": matched_sent,
                "target_sent": target_sent,
                "match_score": score
            }
            plagiarized_sentences.append(sentence)

    if plagiarized_sentences == []:
        return result_data

    matched_target_token = 0
    matched_source_token = 0
    matched_target_list = []
    for sent in plagiarized_sentences:
        matched_target_token += len(sent["target_sent"].split())
        matched_source_token += len(sent["source_sent"].split())
        matched_target_list.append(sent["target_sent"])
    result_data["source_percent"] = matched_source_token / source_tokens
    result_data["target_percent"] = matched_target_token / target_tokens
    result_data["matched_text"] = "\n".join(matched_target_list)
    result_data["matches"] = plagiarized_sentences
    return result_data
