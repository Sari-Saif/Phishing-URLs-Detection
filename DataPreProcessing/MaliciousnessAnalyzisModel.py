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
