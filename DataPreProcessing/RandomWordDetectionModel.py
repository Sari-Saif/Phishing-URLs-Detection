import re

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

# Example usage
print(is_gibberish("gibberish"))  # Might return False as "gibberish" is a real word
print(is_gibberish("aabbccddeeff"))  # Might return True due to repetition
print(is_gibberish("hello"))  # Likely returns False
print(is_gibberish("xqwr"))  # Might return True due to unusual sequence
