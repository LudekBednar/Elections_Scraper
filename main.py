import requests
from bs4 import BeautifulSoup as bs
import csv

response = requests.get("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103")

html = response.text
soup = bs(html,"html.parser")

def kandidujici_strany(adresa):
    response = requests.get(adresa)
    html = response.text
    soup = bs(html,"html.parser")
    seznam_stran = soup.find_all("td", {"class": "overflow_name"})
    strany = []
    for i in range(len(seznam_stran)):
        strany.append(str(seznam_stran[i])[48:-5])

    return strany

def jmeno_obce(adresa):
    response = requests.get(adresa)
    html = response.text
    soup = bs(html,"html.parser")
    hlavicka = soup.find_all("h3")
    # Z hlavicky odstranim znaky, tak ze zustane jen jmeno obce
    obec = hlavicka[2].text[7:-1]
    return obec

def volici_v_seznamu(adresa):
    response = requests.get(adresa)
    html = response.text
    soup = bs(html,"html.parser")
    volici = str(soup.find_all("td",{"headers": "sa2"}))
    # Z hlavicky odstranim znaky, tak aby zustal jen pocet volicu v seznamu
    pocet_volicu = volici[47:-6]
    # Pokud je cislo vetsi nez 1000, tak je potreba z vyscrapovane casti odstranit znak \xa0 ktery oddeluje tisice
    volici_cislo = ""
    if not pocet_volicu.isdigit():
        for i in pocet_volicu:
            if i.isdigit():
                volici_cislo = volici_cislo + i
    else:
        volici_cislo = pocet_volicu

    return volici_cislo

def vydane_obalky(adresa):
    response = requests.get(adresa)
    html = response.text
    soup = bs(html,"html.parser")
    obalky = str(soup.find_all("td",{"headers": "sa3"}))
    # Z hlavicky odstranim znaky, tak aby zustal jen pocet vydanych obalek
    pocet_vydanych_obalek = obalky[47:-6]
    # Pokud je cislo vetsi nez 1000, tak je potreba z vyscrapovane casti odstranit znak \xa0 ktery oddeluje tisice
    obalky_cislo = ""
    if not pocet_vydanych_obalek.isdigit():
        for i in pocet_vydanych_obalek:
            if i.isdigit():
                obalky_cislo  =  obalky_cislo  + i
    else:
         obalky_cislo  = pocet_vydanych_obalek

    return obalky_cislo


def platne_hlasy(adresa):
    response = requests.get(adresa)
    html = response.text
    soup = bs(html,"html.parser")
    hlasy = str(soup.find_all("td",{"headers": "sa6"}))
    # Z hlavicky odstranim znaky, tak aby zustal jen pocet platnych hlasu
    pocet_platnych_hlasu = hlasy[47:-6]
    # Pokud je cislo vetsi nez 1000, tak je potreba z vyscrapovane casti odstranit znak \xa0 ktery oddeluje tisice
    hlasy_cislo = ""
    if not pocet_platnych_hlasu.isdigit():
        for i in pocet_platnych_hlasu:
            if i.isdigit():
                hlasy_cislo  =  hlasy_cislo  + i
    else:
         hlasy_cislo  = pocet_platnych_hlasu

    return hlasy_cislo


def seznam_odkazu():
    odkazy = []
    for i in soup.select("td.cislo a"):
        odkazy.append(i["href"])

    for i in range(len(odkazy)):
        odkazy[i] = "https://volby.cz/pls/ps2017nss/" + odkazy[i]
    return odkazy

hlavicka =  ["Kód obce","Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy","Kandidujici strany"]

with open ("volby.csv", mode = "w") as f:
    writer = csv.writer(f)
    writer.writerow(hlavicka)
    for i in seznam_odkazu():
        kod_obce = i[62:68]
        writer.writerow(
            (
                kod_obce,
                jmeno_obce(i),
                volici_v_seznamu(i),
                vydane_obalky(i),
                platne_hlasy(i),
                kandidujici_strany(i)
            )
        )


