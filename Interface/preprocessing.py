import re
import enchant
import domain_parser

def is_gibberish(word):
    """
    Checks if the given word is gibberish based on simplistic criteria.
    This function looks for patterns of repeated letters or sequences that are 
    unlikely in English words as a basic method of identifying gibberish.
    
    Args:
    word (str): The word to check.
    
    Returns:
    bool: True if the word is considered gibberish, False otherwise.
    """
    # Check for a pattern of repeated letters more than twice
    if re.search(r'(.)\1{2,}', word):
        return True
    
    # Check for a pattern of non-vowel letters repeated more than twice in a row
    if re.search(r'[^aeiou]{3,}', word):
        return True
    
    # Check for a pattern of vowels repeated more than three times in a row
    if re.search(r'[aeiou]{4,}', word):
        return True
    
    # The word does not match our basic gibberish patterns
    return False


def split_and_repeat_word(word):
    d = enchant.Dict("en_US")  # Use the English dictionary
    
    # remove digits
    for l in word:
        if l.isdigit():
            word = word.replace(l, '')
    
    # check if word is a valid dictionary word.
    if d.check(word):
        return [word]

    for i in range(3, len(word) - 2):
        # Split the word into two parts
        part1, part2 = word[:i], word[i:]
        # Check if both parts are valid words
        if d.check(part1) and d.check(part2):
            # If both parts are valid words, return them repeated
            return [part1, part2]
    
    # If no valid split is found, return the original word
    return [word]


def edit_distance(str1, str2):
    """
    Calculate the Levenshtein edit distance between two strings.
    
    Args:
    str1 (str): The first string.
    str2 (str): The second string.
    
    Returns:
    int: The edit distance between the two strings.
    """
    # Create a table to store results of subproblems
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill dp[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j  # Min. operations = j
                
            # If second string is empty, only option is to
            # remove all characters of first string
            elif j == 0:
                dp[i][j] = i  # Min. operations = i
                
            # If last characters are the same, ignore the last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
                
            # If the last character is different, consider all
            # possibilities and find the minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])      # Replace
                
    return dp[m][n]



def keywords():
    with open("../Input/keywords.txt", "r") as f:
        return [keyword[:-1] for keyword in f.readlines()]


def brand_names():
    with open("../Input/allbrands.txt", "r") as f:
        return [brand_name[:-1] for brand_name in f.readlines()]



def filter_keywords(lst):
    keywords_lst = keywords()
    return [word for word in lst if word in keywords_lst]


def filter_brands(lst):
    brands_lst = brand_names()
    return [word for word in lst if word in brands_lst]


def filter_randoms(lst):
    return [word for word in lst if is_gibberish(word)]


def filter_composes(lst):
    ret = []
    for word in lst:
        if len(word) < 7: continue
        ans = split_and_repeat_word(word)
        if len(ans) == 2:
            ret.append((word, ans))
        
    return ret


def filter_maliciouses(lst):
    ret = []
    keywords_lst = keywords()
    brands_lst = brand_names()
    legitimate_words = keywords_lst + brands_lst
    
    for word in lst:
        if len(word) <= 3 or word in legitimate_words:
            continue
        
        for key_or_brand in legitimate_words:
            ed = edit_distance(word, key_or_brand)
            if ed < 2:
                ret.append((word, key_or_brand, ed))
    
    return ret


def subtract_lists(lst1, lst2):
    for word in lst2:
        lst1.remove(word)
    
    return lst1



def pre_process(list_of_urls):
    parsed_urls = domain_parser.parse_nonlabeled_samples(list_of_urls)

    for parsed_url in parsed_urls:
        parsed_url["words_raw_for_filters"] = list(parsed_url["words_raw"]) # remove from all dicts at the end
        
        # brands
        parsed_url["brand_words"] = filter_brands(parsed_url["words_raw_for_filters"])
        parsed_url["words_raw_for_filters"] = subtract_lists(parsed_url["words_raw_for_filters"], parsed_url["brand_words"])

        # keywords
        parsed_url["keyword_words"] = filter_keywords(parsed_url["words_raw_for_filters"])
        parsed_url["words_raw_for_filters"] = subtract_lists(parsed_url["words_raw_for_filters"], parsed_url["keyword_words"])

        # randoms
        parsed_url["random_words"] = filter_randoms(parsed_url["words_raw_for_filters"])
        parsed_url["words_raw_for_filters"] = subtract_lists(parsed_url["words_raw_for_filters"], parsed_url["random_words"])

        # filter word less then 7 letters
        parsed_url["word_list"] = []
        for word in list(parsed_url["words_raw_for_filters"]):
            if len(word) <= 7:
                parsed_url["word_list"].append(word)
                parsed_url["words_raw_for_filters"].remove(word)
        
        # try to decompose the rest
        parsed_url["word_composed"] = []
        for word, composed in filter_composes(parsed_url["words_raw_for_filters"]):
            for internal_word in composed:
                if word in brand_names():
                    parsed_url["brand_words"].append(internal_word)
                
                elif word in keywords():
                    parsed_url["keyword_words"].append(internal_word)
                
                else:
                    parsed_url["word_list"].append(internal_word)
            
            parsed_url["word_composed"].append(word)
            parsed_url["words_raw_for_filters"].remove(word)

        
        # the rest is non brands, non keywords, non randoms, with len more then 7 chars
        # and no composed.
        for word in list(parsed_url["words_raw_for_filters"]):
            parsed_url["word_list"].append(word)
            parsed_url["words_raw_for_filters"].remove(word)
        

        # check the rest for maliciousness
        parsed_url["word_malicious"] = [mal_word for (mal_word, _, _) in filter_maliciouses(parsed_url["word_list"])]
        parsed_url["word_list"] = subtract_lists(parsed_url["word_list"], list(set(parsed_url["word_malicious"])))


        #now can remove the helper list 'words_raw_for_filters'
        parsed_url.pop('words_raw_for_filters')

    return parsed_urls
