from copy import copy
from re import S
from time import sleep
import random, os, json
#Beállítások:

#Szavakat a "szavak.json" -ben tudsz hozzáadni.
#Segítségeket a segitseg függvényben.
#Képeket pedig a kep függvényben.

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Kérlek állítsd be a rendszert
windows = True
linux = False
#Kérlek állítsd be a rendszert
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

f = open('szavak.json', 'r', encoding='utf-8')
szavak = json.load(f)
maxTippek = 6
varakozas = 5 #A segítségek törlése utáni várakozási idő (mp)
alap_varakozas = 5 #--- Az eredi várakozási idő - a kód nem változtatja
szofaj_segitseg, leiras_segitseg, kepes_segitseg = True, True, True #segítségek

kategoria_valasztas = [szavak["targyak"], szavak["allatok"]]
kategoria = random.choice(kategoria_valasztas)
if kategoria == kategoria_valasztas[0]: szofaj = "Tárgy"
elif kategoria == kategoria_valasztas[1]: szofaj = "Állat"
#Beállítások vége

def kezdes():
    global szo, jelenlegi_tippek, keresett_betuk, megtalalt_betuk, rossz_betuk, eredmeny_betuk #Globális változók
    szo = random.choice(kategoria)
    jelenlegi_tippek = 0
    keresett_betuk = []
    rossz_betuk = []
    for i in szo: keresett_betuk.append(i)
    random_betu = random.choice(keresett_betuk) #Véletlenszerűen felfedett betű

    megtalalt_betuk = [random_betu]
    eredmeny_betuk = copy(keresett_betuk)
    for i in keresett_betuk:
        if i in random_betu:
            eredmeny_betuk.remove(random_betu) #Nem kell keresni a véletlenszerűen megadott betűt
    jatek() #Elindítás

def jatek():
    torles()
    while True:
        if eredmeny_betuk == []: #Ha már nincs több betű, amit ki kell találni, akkor vége
            vege(False) #A boolean itt a veszteséget jelenti (false = nyertél)
            break
        global jelenlegi_tippek, tud_torles
        akasztofa()
        szotagolas() #
        print(f"\nJelenlegi rossz tippjeid: {jelenlegi_tippek}/{maxTippek}")
        print("Segítség kéréséhez: /segitseg")
        tipp = input("\nAdj meg egy betűt: ").lower()
        if tipp == "/segítség" or tipp == "/segitseg":
            tud_torles = False
            segitseg()
        if tipp == szo: #Ha a felhasználó beírja a teljes szót, nyer
            torles()
            vege(False)
            break
        if len(tipp) > 1 and tipp != szo:
            if tipp != "/segítség" or tipp != "/segitseg" or tipp != "leiras" or tipp != "leírás" or tipp != "szófaj" or tipp != "szofaj" or tipp != "képes" or tipp != "kepes": #Ha egynél több betűt ír be:
                torles()
                print("Csak egy betűt írj be!")
            else: pass
        else:
            if tipp in megtalalt_betuk:
                torles()
                print(f"A(z) {tipp} betűt már megtaláltad!")
            else: #Ha az utolsó tippnél rosszul tippel (true = vesztett):
                if jelenlegi_tippek + 1 == maxTippek and tipp not in keresett_betuk:
                    vege(True)
                    break
                else:
                    if tipp in keresett_betuk:
                        torles()
                        print(f"{tipp} betű: Helyes! :)")
                        megtalalt_betuk.append(tipp)
                        for i in eredmeny_betuk: #Az összes hasonló betűt ki kell hogy vonja
                            if tipp in eredmeny_betuk: eredmeny_betuk.remove(tipp) 

                    else:
                        if tipp not in rossz_betuk and tipp not in megtalalt_betuk:
                            torles()
                            print(f"{tipp} betű: Helytelen! :(")
                            jelenlegi_tippek += 1
                            rossz_betuk.append(tipp)
                        elif tipp in rossz_betuk:
                            torles()
                            print(f"A(z) {tipp} betűre már tippeltél, de nem volt helyes.")

def szotagolas():
    print("A szó: ", end='')
    for i in szo:
        if i in megtalalt_betuk: print(i, end='')
        elif i not in megtalalt_betuk: print("_", end='')

def segitseg():
    global tud_torles, leiras_segitseg, szofaj_segitseg, kepes_segitseg, alap_varakozas, varakozas
    print("Milyen fajta segítséget kérsz?")
    print("- szófaj")
    print("- leírás")
    print("- képes")
    segitseg = input("\nSegítség típusa: ").lower()
    if segitseg == "szófaj" or segitseg == "szofaj" or segitseg == "1":
        if szofaj_segitseg:
            szofaj_segitseg = not szofaj_segitseg #Az ellentéte (igaz -> hamis)
            print(f"A feladvány szófaja: {szofaj}")
            sleep(2)
        else:
            print("Sajnos már elhasználtad ezt a segítséget.")
            sleep(2)
    elif segitseg == "leírás" or segitseg == "leiras" or segitseg == "2":
        if leiras_segitseg:
            leiras_segitseg = not leiras_segitseg #Az ellentéte (igaz -> hamis)
            switch(szo)
            sleep(varakozas)
            varakozas = alap_varakozas
        else:
            print("Sajnos már elhasználtad ezt a segítséget.")
            sleep(3)
    elif segitseg == "képes" or segitseg == "kepes" or segitseg == "3":
        if kepes_segitseg:
            kepes_segitseg = not kepes_segitseg
            kep()
        else:
            print("Sajnos már elhasználtad ezt a segítséget.")
            sleep(3)

def akasztofa():
    global jelenlegi_tippek
    if jelenlegi_tippek == 0:
        print('''
        ┌───┃
        │
        │
        │
        └───
        ''')
    elif jelenlegi_tippek == 1:
        print('''
        ┌───┃
        │   o
        │
        │
        └───
        ''')
    elif jelenlegi_tippek == 2:
        print('''
        ┌───┃
        │   o
        │   O
        │
        └───
        ''')
    elif jelenlegi_tippek == 3:
        print('''
        ┌───┃
        │   o
        │  \O
        │
        └───
        ''')
    elif jelenlegi_tippek == 4:
        print('''
        ┌───┃
        │   o
        │  \O/
        │
        └───
        ''')
    elif jelenlegi_tippek == 5:
        print('''
        ┌───┃
        │   o
        │  \O/
        │   /
        └───
        ''')


def kep():
    if windows:
        if szo == szavak["targyak"][0]: kep = os.system("start ./Kepek/t0.jpg")
        elif szo == szavak["targyak"][1]: kep = os.system("start ./Kepek/t1.jpg")
        elif szo == szavak["targyak"][2]: kep = os.system("start ./Kepek/t2.jpg")
        elif szo == szavak["targyak"][3]: kep = os.system("start ./Kepek/t3.jpg")
        elif szo == szavak["targyak"][4]: kep = os.system("start ./Kepek/t4.jpg")
        elif szo == szavak["allatok"][0]: kep = os.system("start ./Kepek/a0.jpg")
        elif szo == szavak["allatok"][1]: kep = os.system("start ./Kepek/a1.jpg")
        elif szo == szavak["allatok"][2]: kep = os.system("start ./Kepek/a2.jpg")
        elif szo == szavak["allatok"][3]: kep = os.system("start ./Kepek/a3.jpg")
        sleep(1)
        os.system("taskkill /IM dllhost.exe")
    else:
        if szo == szavak["targyak"][0]: kep = os.system("open ./Kepek/t0.jpg")
        elif szo == szavak["targyak"][1]: kep = os.system("open ./Kepek/t1.jpg")
        elif szo == szavak["targyak"][2]: kep = os.system("open ./Kepek/t2.jpg")
        elif szo == szavak["targyak"][3]: kep = os.system("open ./Kepek/t3.jpg")
        elif szo == szavak["targyak"][4]: kep = os.system("open ./Kepek/t4.jpg")
        elif szo == szavak["allatok"][0]: kep = os.system("open ./Kepek/a0.jpg")
        elif szo == szavak["allatok"][1]: kep = os.system("open ./Kepek/a1.jpg")
        elif szo == szavak["allatok"][2]: kep = os.system("open ./Kepek/a2.jpg")
        elif szo == szavak["allatok"][3]: kep = os.system("open ./Kepek/a3.jpg")

def switch(szo):
    global varakozas
    if szo == szavak["targyak"][0]: return print(szavak["segitsegek_a_targyakhoz"]["0"])
    elif szo == szavak["targyak"][1]: return print(szavak["segitsegek_a_targyakhoz"]["1"])
    elif szo == szavak["targyak"][2]: return print(szavak["segitsegek_a_targyakhoz"]["2"])
    elif szo == szavak["targyak"][3]: return print(szavak["segitsegek_a_targyakhoz"]["3"])
    elif szo == szavak["targyak"][4]: return print(szavak["segitsegek_az_allatokhoz"]["4"])
    elif szo == szavak["allatok"][0]: return print(szavak["segitsegek_az_allatokhoz"]["0"])
    elif szo == szavak["allatok"][1]: return print(szavak["segitsegek_az_allatokhoz"]["1"])
    elif szo == szavak["allatok"][2]: return print(szavak["segitsegek_az_allatokhoz"]["2"])
    elif szo == szavak["allatok"][3]: #Hosszú szöveg, ezért több idő kell neki.
        varakozas = 25
        return print(szavak["segitsegek_az_allatokhoz"]["3"])

def torles():
    if windows: os.system("cls")
    else: os.system("clear")

def vege(vesztettel):
    torles()
    if vesztettel:
        print('''
        ┌───┃
        │   o
        │  \O/
        │   /\\
        └─── Vesztettél!
        ''')
        print("Sajnos vesztettél.")
        print(f"Rossz tippjeid: {jelenlegi_tippek}")
        print(f"A szó a(z) {szo} volt.")
    else:
        akasztofa()
        print("Nyertél! ", end='', sep='')
        print("Gratulálok! :)")
        print(f"Rossz tippjeid: {jelenlegi_tippek}")
        print(f"Megfejtetted a(z) {szo} feladványt.")
    ujra = input("Szeretnél újra játszani? igen/nem: ").lower()
    if ujra == 'igen':
        kezdes()
    else:
        quit()

if __name__ == '__main__': kezdes()