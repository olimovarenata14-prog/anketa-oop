import pytest
from people import Person, Student, Teacher, AnketaError, parse_line

@pytest.mark.parametrize("vhod, ozhidaemo", [
    ("иванов иван", "Иванов Иван"),
    ("ИВАНОВ ИВАН", "Иванов Иван"),
    ("  иванов   иван  ", "Иванов Иван"),
    ("иВаНоВ иВаН", "Иванов Иван"),
    ("петров-водкин кузьма", "Петров-Водкин Кузьма"),
])
def test_fio_privoditsya_k_odnomu_vidu(vhod, ozhidaemo):
    a = Student(vhod, "ivan@mail.ru", "+7 900 000-00-00", "ИУ7-11Б")
    assert a.fio == ozhidaemo

def test_fio_iz_odnogo_slova_otklonyaetsya():
    with pytest.raises(AnketaError):
        Student("Иванов", "ivan@mail.ru", "+7 900 000-00-00", "ИУ7-11Б")

@pytest.mark.parametrize("vhod, ozhidaemo", [
    ("IVAN@MAIL.RU", "ivan@mail.ru"),
    ("Ivan.Petrov@Mail.Ru", "ivan.petrov@mail.ru"),
])
def test_pochta_k_nizhnemu_registru(vhod, ozhidaemo):
    a = Student("Иванов Иван", vhod, "+7 900 000-00-00", "ИУ7-11Б")
    assert a.email == ozhidaemo

@pytest.mark.parametrize("plohaya", [
    "iv anov@mail.ru",
    "ivanovmail.ru",
    "@mail.ru",
    "ivan@",
])
def test_plohaya_pochta_otklonyaetsya(plohaya):
    with pytest.raises(AnketaError):
        Student("Иванов Иван", plohaya, "+7 900 000-00-00", "ИУ7-11Б")

@pytest.mark.parametrize("vhod", [
    "+7 900 000-00-00",
    "8 900 000 00 00",
    "89000000000",
    "+79000000000",
])
def test_telefon_privoditsya_k_odnomu_vidu(vhod):
    a = Student("Иванов Иван", "ivan@mail.ru", vhod, "ИУ7-11Б")
    assert a.phone == "+79000000000"

@pytest.mark.parametrize("plohoy", [
    "123",
    "телефон",
    "+7 900 000-00",
])
def test_plohoy_telefon_otklonyaetsya(plohoy):
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "ivan@mail.ru", plohoy, "ИУ7-11Б")

def test_telefon_s_maskoy():
    a = Student("Иванов Иван", "ivan@mail.ru", "89000000000", "ИУ7-11Б")
    assert a.masked_phone() == "+7 (900) ***-*-00"

def test_fio_sokrashchaetsya_do_inicialov():
    a = Student("Иванов Иван", "ivan@mail.ru", "89000000000", "ИУ7-11Б")
    assert a.short_fio() == "Иванов И."

def test_student_i_prepodavatel_otvechayut_po_raznomu():
    s = Student("Иванов Иван", "ivan@mail.ru", "89000000000", "ИУ7-11Б")
    t = Teacher("Петров Пётр", "petr@mail.ru", "89000000001", "доцент")
    assert s.role() != t.role()
    assert s.role() == "студент"
    assert t.role() == "преподаватель"

def test_student_bez_gruppy_otklonyaetsya():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "ivan@mail.ru", "89000000000", "")

def test_stroka_studenta_razbiraetsya():
    a = parse_line("s; Иванов Иван; ivan@mail.ru; 89000000000; ИУ7-11Б")
    assert isinstance(a, Student)
    assert a.fio == "Иванов Иван"

def test_stroka_prepodavatelya_razbiraetsya():
    a = parse_line("t; Петров Пётр; petr@mail.ru; 89000000001; доцент")
    assert isinstance(a, Teacher)
    assert a.fio == "Петров Пётр"

@pytest.mark.parametrize("stroka", [
    "x; Иванов Иван; ivan@mail.ru; 89000000000; ИУ7-11Б",
    "s; Иванов Иван",
    "",
])
def test_plohaya_stroka_otklonyaetsya(stroka):
    with pytest.raises(AnketaError):
        parse_line(stroka)
