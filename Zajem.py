import bs4
from bs4 import BeautifulSoup
import requests
import csv
import re
import os

link = "https://www.yottachess.com"

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

def poberi_drzave():
    link = "https://www.yottachess.com/filterTable?country=USA&genre=B&ritmo=classic&games=100"
    drzave = requests.get(link).text
    soup_drzave = BeautifulSoup(drzave, "lxml")
    vse = list(re.finditer("<option value=....", drzave))
    koncnice = list(map(fst, vse))
    return list(map(zadnji_tri, koncnice))[16:-5]

poberi_drzave()

def sahisti(drzava):
    sahisti = requests.get(f"https://www.yottachess.com/filterTable?country={drzava}&genre=B&ritmo=classic&games=100").text
    soup_sahisti = BeautifulSoup(sahisti, "lxml")
    ime = soup_sahisti.find_all("h2", {"style" : "all:unset;"})
    naziv = soup_sahisti.find_all("td", {"style" : "font-weight:bold;"})
    classical = soup_sahisti.find_all("td")[4::9]
    rapid = soup_sahisti.find_all("td")[5::9]
    blitz = soup_sahisti.find_all("td")[6::9]
    leto_rojstva = soup_sahisti.find_all("td")[7::9]
    stevilo_iger = soup_sahisti.find_all("td")[8::9]

    odstrani_tag = list(map(lambda x: remove_tag(x), (ime, naziv, classical, rapid, blitz, leto_rojstva, stevilo_iger)))
    drzava_sahisti = []
    n = len(ime)


    for i in range(n):
        drzava_sahisti.append({"Ime" : odstrani_tag[0][i], "Država" : drzava ,"Naziv" : odstrani_tag[1][i], "Classical ocena" : varen_int(odstrani_tag[2][i]), 
                        "Rapid ocena" : varen_int(odstrani_tag[3][i]), "Blitz ocena" : varen_int(odstrani_tag[4][i]), "Leto rojstva" : varen_int(odstrani_tag[5][i]), 
                        "Število iger" : varen_int(odstrani_tag[6][i])})
    
    return drzava_sahisti

def zapisi_v_csv_sahisti():
    with open("Podatki_sahistov.csv", "w", encoding="utf-8") as file:
        polja = ["Ime", "Država" ,"Naziv", "Classical ocena", "Rapid ocena", "Blitz ocena", "Leto rojstva", "Število iger"]
        zapisi = csv.DictWriter(file, fieldnames=polja)
        zapisi.writeheader()
        for kon in poberi_drzave():
            zapisi.writerows(sahisti(kon))

zapisi_v_csv_sahisti()

def link2():
    stran = requests.get(link).text
    soup_stran = BeautifulSoup(stran, "lxml")
    del_linka = soup_stran.find("a", {"title" : "Ranking Chess Engines"}).get("href")
    return link + del_linka

def sah_programi():

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

    stran = requests.get(link2()).text
    soup_stran = BeautifulSoup(stran, "lxml")
    ime = remove_tag(soup_stran.find_all("h2")[1:])
    elo = remove_tag(soup_stran.find_all("td")[2::5])
    leti = remove_tag(soup_stran.find_all("td")[3::5])
    leto_izdaje = razdeli(leti)[0]
    zadnja_različica = razdeli(leti)[1]
    igre = remove_tag(soup_stran.find_all("td")[4::5])

    vse = []
    n = len(ime)
    for i in range(n):
        vse.append({"Ime" : ime[i], "ELO" : varen_int(elo[i]), "Leto izdaje" : varen_int(leto_izdaje[i]),
                    "Zadnja različica" : varen_int(zadnja_različica[i]), "Igre" : varen_int(igre[i])})

    return vse

programi = ["Ime", "ELO", "Leto izdaje", "Zadnja različica" ,"Igre"]

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        writer.writerows(slovarji)

zapisi_csv(sah_programi(), programi, "Podatki_programov.csv")