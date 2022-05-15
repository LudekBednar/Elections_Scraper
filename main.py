import csv
import sys
from pomocne_funkce import *


def hlavni():
    # Zajistim, ze soubor se spusti, pouze pokud jsou zadany presne 2 argumenty,
    # prvni argument obsahuje platny odkaz a druhy argument ma koncovku csv
    if len(sys.argv) != 3:
        print("""Zadej přesně 2 argumenty ("odkaz na uzemní celek" a jméno výstupního souboru.csv)""")
    elif sys.argv[1] not in platne_odkazy():
        print("Zadaný odkaz musí směřovat na výběr obce ze stránky: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ ")
    elif sys.argv[2][-3:] != "csv":
        print("Jméno výstupního soboru musí mít koncovku .csv")

    else:
        with open(sys.argv[2], mode="w") as f:
            zapisovac = csv.writer(f)
            zapisovac.writerow(hlavicka(seznam_odkazu(sys.argv[1])[0]))
    # For-cyklem projdu pres vsechny stazene odkazy a zapisu potrebne udaje
        for i in seznam_odkazu(sys.argv[1]):
            with open(sys.argv[2], mode="a") as f:
                zapisovac = csv.writer(f)
                zapisovac.writerow(hodnoty(i))


if __name__ == "__main__":
    hlavni()
