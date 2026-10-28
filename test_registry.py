import pytest
from registry import Registry

@pytest.fixture
def zhurnal(tmp_path):
    f = tmp_path / "ankety.txt"
    f.write_text(
        "s; Иванов Иван; ivan@mail.ru; 89000000000; ИУ7-11Б\n"
        "s; Петров Пётр; petr@mail.ru; 89000000001; ИУ7-12Б\n"
        "t; Сидоров Сидор; sid@mail.ru; 89000000002; доцент\n"
        "s; Плохой; bad-mail; 123; \n"
        "x; Кто-то; kto@mail.ru; 89000000003; X\n"
        "s; Иванов Иван\n",
        encoding="utf-8",
    )
    r = Registry()
    r.load(str(f))
    return r

def test_pustoy_zhurnal_dlina_nol():
    assert len(Registry()) == 0

def test_posle_zagruzki_tri_ankety(zhurnal):
    assert len(zhurnal) == 3

def test_tri_zapisi_braka(zhurnal):
    assert len(zhurnal.errors) == 3

def test_nomera_strok_braka(zhurnal):
    nomera = [n for n, _, _ in zhurnal.errors]
    assert nomera == [4, 5, 6]

def test_net_suschestvuyuschego_fayla():
    r = Registry()
    assert r.load("net_takogo_fayla_12345.txt") is False

def test_schetchik_roley(zhurnal):
    assert zhurnal.stats_by_roles() == {"студент": 2, "преподаватель": 1}

def test_schetchik_grupp_tolko_studenty(zhurnal):
    assert zhurnal.stats_by_extra() == {"иу7-11б": 1, "иу7-12б": 1, "доцент": 1}

def test_save_ok_odna_stroka_na_cheloveka(zhurnal, tmp_path):
    out = tmp_path / "ok.txt"
    zhurnal.save_ok(str(out))
    assert len(out.read_text(encoding="utf-8").strip().splitlines()) == 3

def test_save_errors_pishet_prichinu(zhurnal, tmp_path):
    out = tmp_path / "err.txt"
    zhurnal.save_errors(str(out))
    text = out.read_text(encoding="utf-8")
    assert "bad-mail" in text or "почта неверная" in text