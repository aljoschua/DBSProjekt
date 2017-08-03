"""
Select distance function by setting 'function':
Edit-Distance: "edit"
Difference in length of string: "lenS"
Longest common substring: "lcs"
Difference in number of digits and letters: "d&l"
"""
function = "edit"


def d(a,b):
    if function == "lcs":
        #https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Longest_common_substring#Python_2
        m = [[0] * (1 + len(b)) for i in xrange(1 + len(a))]
        longest, x_longest = 0, 0
        for x in xrange(1, 1 + len(a)):
            for y in xrange(1, 1 + len(b)):
                if a[x - 1] == b[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
        else:
            m[x][y] = 0
        return len(a[x_longest - longest: x_longest]) # used to be without len(  )
    if function == "lenS":
        return abs(len(a)-len(b))            
    if function == "d&l":
        import re
        lettersa = len(re.findAll("[a-zA-Z]", a))
        numbersa = len(re.findAll("[0-9]", a))
        lettersb = len(re.findAll("[a-zA-Z]", b))
        numbersb = len(re.findAll("[0-9]", b))
        return abs(lettersa-lettersb)+abs(numbersa-numbersb)
    if function == "edit": 
        short = min(len(a), len(b))
        diff = max(len(a), len(b)) - short
        for i in range(short):
            if a[i] != b[i]:
                diff += 1
        return diff
    

