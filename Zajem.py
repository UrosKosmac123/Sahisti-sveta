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
        drzava_sahisti.append({"Ime" : odstrani_tag[0][i], "Država" : drzava ,"Naziv" : odstrani_tag[1][i], "Classical ocena" : odstrani_tag[2][i], 
                        "Rapid ocena" : odstrani_tag[3][i], "Blitz ocena" : odstrani_tag[4][i], "Leto rojstva" : odstrani_tag[5][i], 
                        "Število iger" : odstrani_tag[6][i]})
    
    return drzava_sahisti

def zapisi_v_csv():
    with open("Podatki.csv", "w", newline="") as file:
        polja = ["Ime", "Država" ,"Naziv", "Classical ocena", "Rapid ocena", "Blitz ocena", "Leto rojstva", "Število iger"]
        zapisi = csv.DictWriter(file, fieldnames=polja)
        for kon in poberi_drzave():
            zapisi.writerows(sahisti(kon))

def link2():
    stran = requests.get(link).text
    soup_stran = BeautifulSoup(stran, "lxml")
    del_linka = soup_stran.find("a", {"title" : "Ranking Chess Engines"}).get("href")
    return link + del_linka

#def sah_programi():

stran = requests.get(link2()).text
soup_stran = BeautifulSoup(stran, "lxml")
ime = remove_tag(soup_stran.find_all("h2")[1:])
elo = remove_tag(soup_stran.find_all("td")[2::5])
leti = remove_tag(soup_stran.find_all("td")[3::5])
igre = remove_tag(soup_stran.find_all("td")[4::5])

n = len(ime)
