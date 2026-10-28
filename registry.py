from people import parse_line, AnketaError

class Registry:
    def __init__(self):
        self.accepted = []
        self.errors = []
        
    def add(self, person):
        self.accepted.append(person)
        
    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return False
        for i, line in enumerate(lines, start=1):
            line = line.rstrip("\n")
            if line.strip() == "":
                continue
            try:
                person = parse_line(line)
                self.add(person)
            except AnketaError as e:
                self.errors.append((i, line, str(e)))
        return True
        
    def stats_by_roles(self):
        stats = {}
        for p in self.accepted:
            r = p.role()
            stats[r] = stats.get(r, 0) + 1
        return stats
        
    def stats_by_extra(self):
        stats = {}
        for p in self.accepted:
            e = p.extra()
            stats[e] = stats.get(e, 0) + 1
        return stats
        
    def save_ok(self, filename="ok.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for p in sorted(self.accepted):
                f.write(f"{p.fio};{p.email};{p.phone};{p.extra()}\n")
                
    def save_errors(self, filename="errors.txt"):
        with open(filename, "w", encoding="utf-8") as f:
            for nomer, stroka, prichina in self.errors:
                f.write(f"строка {nomer}: {prichina}\n")
                f.write(f"{stroka}\n\n")
                
    def sort_by_name(self):
        self.accepted.sort(key=lambda x: x.fio.lower().replace("ё", "е"))

    def __iter__(self):
        return iter(self.accepted)
                
    def __len__(self):
        return len(self.accepted)