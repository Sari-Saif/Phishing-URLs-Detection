
def keywords():
    with open("../Input/keywords.txt", "r") as f:
        return [keyword[:-1] for keyword in f.readlines()]


def brand_names():
    with open("../Input/allbrands.txt", "r") as f:
        return [brand_name[:-1] for brand_name in f.readlines()]


