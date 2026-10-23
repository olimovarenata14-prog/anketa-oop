from registry import Registry
def main():
    reg = Registry()
    if not reg.load("anketa.txt"):
        print("Файл anketa.txt не найден. Работа завершена.")
        return
    print(f"{'№':<3} {'ФИО':<30} {'Роль':<15} {'Группа/кафедра':<18} {'Телефон'}")
    print("-" * 85)
    sorted_accepted = sorted(reg.accepted)
    for i, p in enumerate(sorted_accepted, start=1):
        fio = p.fio
        if len(fio) > 29:
            fio = fio[:26] + "..."
        print(f"{i:<3} {fio:<30} {p.role():<15} {p.extra():<18} {p.masked_phone()}")
    print()
    print(f"Принято: {len(reg)} | Отклонено: {len(reg.errors)}")
    print("\nПо ролям:")
    for role, count in reg.stats_by_roles().items():
        print(f"  {role}: {count}")
    print("\nПо группам/кафедрам:")
    for extra, count in reg.stats_by_extra().items():
        print(f"  {extra}: {count}")
    print("\n=== БРАК ===")
    for nomer, stroka, prichina in reg.errors:
        print(f"строка {nomer}: {prichina}")
        print(f"  {stroka}")
    print()
    reg.save_ok()
    reg.save_errors()
    print("Сохранено: ok.txt и errors.txt")
if __name__ == "__main__":
    main()