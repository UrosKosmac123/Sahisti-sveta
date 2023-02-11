import csv

def remove_tag(sez):
    return list(map(lambda x: x.string, sez))

def zadnji_tri(str):
    return str[-3:]

def fst(element):
    return element[0]

def varen_int(val, default=None):
        try:
            return int(val)
        except ValueError:
            return default

def razdeli(sez):
        pomozna = list(map(lambda x: x.split("/"), sez))
        leto_idaje = []
        zadnja_različica = []
        for i in pomozna:
            if len(i) == 2:
                zadnja_različica += [i[0]]
                leto_idaje += [i[1]]
            elif len(i) == 1:
                leto_idaje += [i[0]]
                zadnja_različica += [""]
            else:
                leto_idaje += [""]
                zadnja_različica += [""]
        return leto_idaje, zadnja_različica

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        writer.writerows(slovarji)
