import pytest
from razminka.wordcount import chastota
@pytest.fixture
def fayl_s_textom(tmp_path):
    put = tmp_path / "text.txt"
    put.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return put
def test_slova_mama_i_rama(fayl_s_textom):
    slovar = chastota(fayl_s_textom)
    assert slovar["мама"] == 2
    assert slovar["рама"] == 2
def test_net_klyuchey_s_znakami_prepinaniya(fayl_s_textom):
    slovar = chastota(fayl_s_textom)
    assert "рама," not in slovar
    assert "раму." not in slovar
def test_vsego_chetyre_raznyh_slova(fayl_s_textom):
    slovar = chastota(fayl_s_textom)
    assert len(slovar) == 4
