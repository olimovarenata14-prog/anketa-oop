import string

def chastota(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower()
    for p in string.punctuation:
        text = text.replace(p, ' ')
    slova = text.split()
    res = {}
    for s in slova:
        res[s] = res.get(s, 0) + 1
    return res
