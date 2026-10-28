from razminka.calc import summa, skidka, srednee
import pytest
def test_summa_polozhitelnye():
    assert summa(2, 3) == 5
def test_summa_s_nulem():
    assert summa(0, 7) == 7
def test_skidka_10_procentov_ot_1000():
    assert skidka(1000, 10) == 900.0
def test_skidka_slishkom_bolshaya():
    with pytest.raises(ValueError):
        skidka(1000, 95)
def test_srednee_pustoy_spisok():
    with pytest.raises(ValueError):
        srednee([])
@pytest.mark.parametrize("dannye, ozhidaemoe", [
    ([5], 5),
    ([2, 4], 3),
    ([1, 2, 3, 4], 2.5),
    ([-2, 2], 0),
])
def test_srednee(dannye, ozhidaemoe):
    assert srednee(dannye) == ozhidaemoe
