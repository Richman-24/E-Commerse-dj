import re

dom = "http://google.com"

pattern1 = r"(https://|http://|www.)(.+)\.[a-z]"
pattern2 = r"(.+)\.[a-z]"

try:
    print(re.search(pattern1, dom))
except TypeError:
    print(re.search(pattern2, dom))