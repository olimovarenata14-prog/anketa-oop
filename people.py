class AnketaError(Exception):
    """Своё исключение для ошибок в анкетах."""
    pass

class Person:
    def __init__(self, fio, email, phone):
        self.fio = self.check_fio(fio)
        self.email = self.check_email(email)
        self.phone = self.check_phone(phone)
        
    @staticmethod
    def check_fio(fio):
        parts = fio.split()
        if len(parts) < 2:
            raise AnketaError("В ФИО меньше двух слов")
        parts = [p.title() for p in parts]
        return " ".join(parts)
        
    @staticmethod
    def check_email(email):
        email = email.strip().lower()
        if " " in email:
            raise AnketaError(f"почта неверная: {email}")
        if email.count("@") != 1:
            raise AnketaError(f"почта неверная: {email}")
        levo, pravo = email.split("@")
        if levo == "" or pravo == "":
            raise AnketaError(f"почта неверная: {email}")
        if "." not in pravo:
            raise AnketaError(f"почта неверная: {email}")
        if pravo.startswith(".") or pravo.endswith("."):
            raise AnketaError(f"почта неверная: {email}")
        return email
        
    @staticmethod
    def check_phone(phone):
        digits = "".join([ch for ch in phone if ch.isdigit()])
        if len(digits) != 11:
            raise AnketaError(f"телефон неверный: {phone.strip()}")
        if digits[0] not in "78":
            raise AnketaError(f"телефон неверный: {phone.strip()}")
        return "+7" + digits[1:]
        
    def masked_phone(self):
        return f"+7 ({self.phone[2:5]}) ***-*-{self.phone[-2:]}"
        
    def short_fio(self):
        parts = self.fio.split()
        if len(parts) >= 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        return f"{parts[0]} {parts[1][0]}."
        
    def role(self):
        return "неизвестно"
        
    def extra(self):
        return "неизвестно"
        
    def __str__(self):
        return f"{self.fio} ({self.role()})"
        
    def __lt__(self, other):
        return self.fio < other.fio

class Student(Person):
    def __init__(self, fio, email, phone, group):
        super().__init__(fio, email, phone)
        group = group.replace(" ", "").lower()
        if group == "":
            raise AnketaError("пустая группа")
        self.group = group
        
    def role(self):
        return "студент"
        
    def extra(self):
        return self.group

class Teacher(Person):
    def __init__(self, fio, email, phone, kafedra):
        super().__init__(fio, email, phone)
        kafedra = kafedra.strip()
        if kafedra == "":
            raise AnketaError("пустая кафедра")
        self.kafedra = kafedra
        
    def role(self):
        return "преподаватель"
        
    def extra(self):
        return self.kafedra

def parse_line(line):
    parts = [p.strip() for p in line.split(";")]
    if len(parts) != 5:
        raise AnketaError(f"полей {len(parts)}, а нужно 5")
    typ, fio, email, phone, last_field = parts
    if typ == "s":
        return Student(fio, email, phone, last_field)
    elif typ == "t":
        return Teacher(fio, email, phone, last_field)
    else:
        raise AnketaError(f"неизвестный тип: {typ}")