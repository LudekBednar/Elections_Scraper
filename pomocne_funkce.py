import requests
from bs4 import BeautifulSoup as bs


def kandidujici_strany(adresa):
    """Funkce stahne seznam vsech kandidujicch stran a vrati ho jako list"""
    strany = []
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    seznam_stran = soup.find_all("td", {"class": "overflow_name"})

    for i in range(len(seznam_stran)):
        strany.append(str(seznam_stran[i])[48:-5])
    return strany


def pocet_hlasu(adresa):
    """Funkce stahne pocet hlasu pro jednotlive strany a vrati je jako list.
    Serazeni v listu je totozne jako u funkce kandidujici_strany,
    dale se tedy v programu pracuje s tim, ze strane na 1. indexu v listu kanidujici strany odpovida pocet
     hlasu opet na 1. indexu v listu pocet_hlasu"""
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    tabulka = soup.find_all("table", {"class": "table"})

    # z tabulky se pres dva for-cykly vybere potreby blok vysledku, ktery obashuje i pocet hlasu pro jednotlive strany
    blok_vysledku = []
    for i in tabulka:
        for j in i:
            blok_vysledku.append(j)

    # jednotlive hodnoty z bloku_vysledku se prevedou na list, pokud je delka listu presne 7, jedna se o radek, ktery obsahu pocet hlasu
    hlasy = []
    for i in blok_vysledku:
        if len(i.text.split("\n")) == 7:
            hlasy.append((i.text.split("\n"))[3])

    # Pokud je cislo vetsi nez 1000, tak je potreba z vyscrapovane casti odstranit znak \xa0 ktery oddeluje tisice
    ocistene_cislo = ""
    for index, cislice in enumerate(hlasy):
        if not cislice.isdigit():
            for cifra in cislice:
                if cifra.isdigit():
                    ocistene_cislo = ocistene_cislo + cifra
        else:
            ocistene_cislo = cislice
        hlasy[index] = ocistene_cislo
        ocistene_cislo = ""
    return hlasy


def jmeno_obce(adresa):
    """Funkce vraci jmeno obce"""
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    hlavicka = soup.find_all("h3")
    # Z hlavicky vystrihnu jen tu cast, ktera obsahuje jmeno obce
    index = hlavicka[2].text.find("Obec")
    obec = hlavicka[2].text[index + 5:-1]
    return obec

def volici_v_seznamu(adresa):
    """Funkce vraci pocet volicu zapsanych v seznamu"""
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    volici = str(soup.find_all("td", {"headers": "sa2"}))
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
    """Funkce vraci pocet vydanych obalek"""
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    obalky = str(soup.find_all("td", {"headers": "sa3"}))
    # Z hlavicky odstranim znaky, tak aby zustal jen pocet vydanych obalek
    pocet_vydanych_obalek = obalky[47:-6]
    # Pokud je cislo vetsi nez 1000, tak je potreba z vyscrapovane casti odstranit znak \xa0 ktery oddeluje tisice
    obalky_cislo = ""
    if not pocet_vydanych_obalek.isdigit():
        for i in pocet_vydanych_obalek:
            if i.isdigit():
                obalky_cislo = obalky_cislo + i
    else:
        obalky_cislo = pocet_vydanych_obalek

    return obalky_cislo


def platne_hlasy(adresa):
    """Funkce vraci pocet platnych hlasu"""
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    hlasy = str(soup.find_all("td", {"headers": "sa6"}))
    # Z hlavicky odstranim znaky, tak aby zustal jen pocet platnych hlasu
    pocet_platnych_hlasu = hlasy[47:-6]
    # Pokud je cislo vetsi nez 1000, tak je potreba z vyscrapovane casti odstranit znak \xa0 ktery oddeluje tisice
    hlasy_cislo = ""
    if not pocet_platnych_hlasu.isdigit():
        for i in pocet_platnych_hlasu:
            if i.isdigit():
                hlasy_cislo = hlasy_cislo + i
    else:
        hlasy_cislo = pocet_platnych_hlasu

    return hlasy_cislo


def seznam_odkazu(adresa):
    """Fuknce vraci list, ktery obsahuje vsechny odkazy na vysledky jdnotlivych obci"""
    response = requests.get(adresa)
    html = response.text
    soup = bs(html, "html.parser")
    odkazy = []
    for i in soup.select("td.cislo a"):
        odkazy.append(i["href"])

    for i in range(len(odkazy)):
        odkazy[i] = "https://volby.cz/pls/ps2017nss/" + odkazy[i]
    return odkazy


def kod_obce(adresa):
    """Fuknce vraci kod dane obce"""
    index = adresa.find("obec=")
    kod_obce = adresa[index + 5:index + 11]
    return kod_obce


def hlavicka(adresa):
    """Funkce vrati list, ktery se vyuzije jako hlavicka csv souboru"""

    # Prvnich 5 hodnot v seznamu klice je vypsano manualne, dle pozadavku zadani (automaticke stahovani by nemelo zadny smysl).Dale se for-cyklem priradi jmena vsech kandidujicich stran
    klice = ["Kód obce", "Jméno obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]
    for i in kandidujici_strany(adresa):
        klice.append(i)
    return klice


def hodnoty(adresa):
    """Funkce vrati list, ktery se vyuzije jako radek pro kazdou obec pri zapisu do csv souboru"""
    hodnoty = [kod_obce(adresa), jmeno_obce(adresa), volici_v_seznamu(adresa), vydane_obalky(adresa),
               platne_hlasy(adresa)]
    for i in pocet_hlasu(adresa):
        hodnoty.append(i)
    return hodnoty

def platne_odkazy():
    """Funkce vrati seznam,ktere obsahuje vsechny platne odkazy ktere muze uzivatel zadat"""
    response = requests.get("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
    html = response.text
    soup = bs(html, "html.parser")
    platne_odkazy = []
    # Pripavim si list headers ktery obsahuje hodnoty headers na vsechny tabulky (kraje):  "t1sa3 az t14sa3"
    headers = []
    for i in range(1, 15):
        headers.append(f"t{i}sa3")

    for i in soup.find_all("td", {"headers": headers}):
        platne_odkazy.append(i.findChild("a")["href"])

    for i in range(len(platne_odkazy)):
        platne_odkazy[i] = "https://volby.cz/pls/ps2017nss/" + platne_odkazy[i]
    return platne_odkazy
