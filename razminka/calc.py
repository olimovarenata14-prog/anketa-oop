def summa(a, b):
    return a + b

def skidka(cena, procent):
    if procent < 0 or procent > 90:
        raise ValueError()
    return round(cena * (1 - procent / 100), 2)

def srednee(spisok):
    if not spisok:
        raise ValueError()
    return sum(spisok) / len(spisok)
