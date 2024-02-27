import pandas as pd

def avg_word_len(lst):
    if not lst: return 0
    lens = [len(word) for word in lst]
    return sum(lens)//len(lens)

def max_word_len(lst):
    if not lst: return 0
    return max([len(word) for word in lst])

def min_word_len(lst):
    if not lst: return 0
    return min([len(word) for word in lst])

def get_urls(list_of_dicts):
    return [d["url"] for d in list_of_dicts]

def get_ids(list_of_dicts):
    return [d["id"] for d in list_of_dicts]

def get_classes(list_of_dicts):
    return [d["class"] for d in list_of_dicts]



def get_word_raw_counts(list_of_dicts):
    return [len(d["words_raw"]) for d in list_of_dicts]

def get_word_list_counts(list_of_dicts):
    return [len(d["word_list"]) for d in list_of_dicts]

def get_word_brand_counts(list_of_dicts):
    return [len(d["brand_words"]) for d in list_of_dicts]

def get_word_keyword_counts(list_of_dicts):
    return [len(d["keyword_words"]) for d in list_of_dicts]

def get_word_random_counts(list_of_dicts):
    return [len(d["random_words"]) for d in list_of_dicts]

def get_word_composed_counts(list_of_dicts):
    return [len(d["word_composed"]) for d in list_of_dicts]

def get_word_malisious_counts(list_of_dicts):
    return [len(d["word_malicious"]) for d in list_of_dicts]



def get_avg_word_raw_len(list_of_dicts):
    return [avg_word_len(d["words_raw"]) for d in list_of_dicts]

def get_avg_word_composed_len(list_of_dicts):
    return [avg_word_len(d["word_composed"]) for d in list_of_dicts]



def get_longest_raw_lens(list_of_dicts):
    return [max_word_len(d["words_raw"]) for d in list_of_dicts]

def get_shortest_raw_lens(list_of_dicts):
    return [min_word_len(d["words_raw"]) for d in list_of_dicts]


def get_digit_counts(list_of_dicts):
    ret = []
    for d in list_of_dicts:
        sum = 0
        for i in range(10):
            sum += d["url"].count(str(i))
        ret.append(sum)
    
    return ret


def get_subdomain_lens(list_of_dicts):
    return [len(d["subdomain"]) for d in list_of_dicts]

def get_subdomain_counts(list_of_dicts):
    return [len(d["subdomain"].split('.')) if d["subdomain"] else 0 for d in list_of_dicts]

def get_url_lens(list_of_dicts):
    return [len(d["url"]) for d in list_of_dicts]

def get_word_is_in_urls(list_of_dicts, word):
    return [word in d["url"] for d in list_of_dicts]

def get_special_char_counts(list_of_dicts):
    ret = []
    for d in list_of_dicts:
        sum = 0
        for l in "-./@?&=_":
            sum += d["url"].count(l)
        ret.append(sum)
    
    return ret

def get_urls_is_https(list_of_dicts):
    return ["https" in d["url"] for d in list_of_dicts]

def get_urls_is_http(list_of_dicts):
    return ["http" in d["url"] and "https" not in d["url"] for d in list_of_dicts]

def get_known_TLD_in_domains(list_of_dicts):
    common_tlds = ["com", "org", "net", "de", "edu", "gov"]
    return [d["tld"] in common_tlds for d in list_of_dicts]


def build_df(list_of_dict):
    df = pd.DataFrame(\
    {"id": get_ids(list_of_dict), \
    "url": get_urls(list_of_dict), \
    #"class":get_classes(list_of_dict), \
    "word_raw_count":get_word_raw_counts(list_of_dict), \
    "word_brand_count": get_word_brand_counts(list_of_dict), \
    "avg_word_raw_len": get_avg_word_raw_len(list_of_dict), \
    "longest_raw_len": get_longest_raw_lens(list_of_dict), \
    "shortest_raw_len": get_shortest_raw_lens(list_of_dict), \
    "word_composed_count": get_word_composed_counts(list_of_dict), \
    "avg_word_composed_len": get_avg_word_composed_len(list_of_dict), \
    "word_keyword_count": get_word_keyword_counts(list_of_dict), \
    "word_malicious_count": get_word_malisious_counts(list_of_dict), 
    "word_random_count": get_word_random_counts(list_of_dict), 
    "word_list_count": get_word_list_counts(list_of_dict), 
    "digit_count": get_digit_counts(list_of_dict), \
    "subdomain_len": get_subdomain_lens(list_of_dict), \
    "subdomain_count": get_subdomain_counts(list_of_dict), \
    "url_len": get_url_lens(list_of_dict),
    "www": get_word_is_in_urls(list_of_dict, "www"), \
    "com": get_word_is_in_urls(list_of_dict, "com"), \
    "special_character_count": get_special_char_counts(list_of_dict), \
    "https": get_urls_is_https(list_of_dict), \
    "http": get_urls_is_http(list_of_dict), \
    "known_TLD": get_known_TLD_in_domains(list_of_dict)})

    return df

