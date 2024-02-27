from RandomWordDetectionModel import is_gibberish
from WordDecomposerMoodle import split_and_repeat_word
from MaliciousnessAnalyzisModel import edit_distance


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


#print(filter_keywords(["hey", "admin", "google", "bye", "zxcv", "securelogin", "piretebay"]))
#print(filter_brands(["hey", "admin", "google", "bye", "zxcv", "securelogin", "piretebay"]))
#print(filter_randoms(["hey", "admin", "google", "bye", "zxcv" ,"securelogin", "piretebay"]))
#print(filter_composes(["hey", "admin", "google", "bye", "zxcv" ,"securelogin", "piretebay"]))
#print(filter_malicious(["hey", "admin", "google", "bye", "zxcv" ,"securelogin","piretebay"]))
