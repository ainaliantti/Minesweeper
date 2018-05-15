import random
from copy import deepcopy
import datetime

def lue_int(kehoite = "\n> ", virheilmoitus = "Virhe."):
    '''
    Tarkastaa onko luku kokonaisluku. Ottaa parametreina kehoite- ja virheilmoitustekstit. Palauttaa kokonaisluvun.
    '''
    while True:
        try:
            kokonaisluku = int(input(kehoite))
        except (ValueError, EOFError):
            print(virheilmoitus)
        else:
            return kokonaisluku

def tilastoon_tallentaminen(ajankohta, aika, minuutit, sekunnit, vuorot, tulos, pituus, leveys, miinat):
    '''
    Tallentaa tietoja pelistä tekstitiedostoon.
    '''
    tiedosto = "tilastot.txt"
    try:
        with open(tiedosto, "a") as kohde:
            kohde.write(ajankohta.strftime("%d.%m.%Y "))
            kohde.write("{}:{} ".format(aika.hour, aika.minute))
            kohde.write("{}:{} {} {} {}x{} {}\n".format(minuutit, sekunnit, vuorot, tulos, pituus, leveys, miinat))
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tilaston tallennus epäonnistui.")
    kohde.close()

def tilaston_naytto():
    '''
    Lukee tekstitiedostosta tilastoja pelatuista peleistä.
    '''
    tiedosto = "tilastot.txt"
    try:
        with open(tiedosto) as lahde:
            pelitiedot = []
            for rivi in lahde.readlines():
                ajankohta, klo, aika, vuorot, tulos, koko, miinat = rivi.split(" ")
                pelitiedot.append(rivi)
                osat = rivi.split(" ")
            for i, asia in enumerate(pelitiedot):
                pelitiedot[i] = asia.strip()
            pituus = len(pelitiedot)
            j = 0
            print("\nTilastot:\n")
            while j < pituus:
                ajankohta, klo, aika, vuorot, tulos, koko, miinat = pelitiedot[j].split(" ")
                print("Pvm: {}\nKlo: {}\nKesto (m:s): {}\nKesto vuoroissa: {}\nTulos: {}\nKentän koko (pit x lev): {}\nMiinojen lkm: {}\n".format(ajankohta, klo, aika, vuorot, tulos, koko, miinat))
                j += 1
            lahes_merkitykseton_muuttuja = input("Paina enteriä.\n> ")
    except (ValueError, EOFError):
            print("Virhe.")
    except IOError:
            print("Tiedoston avaaminen ei onnistunut.")
    lahde.close()
    

def pelivalinnat():
    '''
    Kysytään käyttäjältä peliruudukon korkeus ja leveys sekä miinojen määrä.
    '''
    kehoite_pituus = "Syötä peliruudukon pituus.\n> "
    kehoite_leveys = "Syötä peliruudukon leveys.\n> "
    kehoite_miinat = "Syötä miinojen lukumäärä.\n> "
    virheilmoitus = "Syötä kokonaisluku."
    while True:
        pituus = lue_int(kehoite_pituus, virheilmoitus)
        if pituus > 50:
            print("Maksimipituus on 50.")
            continue
        elif pituus <= 0:
            print("Montako miinaa meinasit tuon pituiselle kentälle laittaa...")
            continue
        break
    while True:
        leveys = lue_int(kehoite_leveys, virheilmoitus)
        if leveys > 100:
            print("Maksimileveys on 100.")
            continue
        elif pituus <= 0:
            print("Montako miinaa meinasit tuon levyiselle kentälle laittaa...")
            continue
        break
    while True:
        miinat = lue_int(kehoite_miinat, virheilmoitus)
        if miinat > (pituus * leveys):
            print("Miinoja ei voi olla enempää kuin peliruutuja.")
            continue
        elif miinat <= 0:
            print("Laita nyt edes yksi miina.")
            continue
        elif miinat > (pituus * leveys / 2):
            print("Onnea vaan matkaan!")
        break
    kentan_luonti(pituus, leveys, miinat)

def kentan_luonti(pituus, leveys, miinat):
    '''
    Luo kentän. Luo listan kentän koordinaattipareista.
    '''
    kentta = []
    for rivi in range(pituus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append("_")

    koordinaattiparit = []
    for x in range(leveys):
        for y in range(pituus):
            koordinaattiparit.append((x, y))
    
    for i in range(miinat):
        x, y = miinoitus(kentta, koordinaattiparit, pituus, leveys)
    pelin_pyoritys(pituus, leveys, miinat, kentta)

def miinoitus(kenttalista, eimiinojakoordinaatit, pituus, leveys):
    '''
    Miinoittaa pelikentän.
    '''
    x = 0
    y = 0
    while True:
        x = random.randint(0, leveys - 1)
        y = random.randint(0, pituus - 1)
        if kenttalista[y][x] == "_":
            kenttalista[y][x] = "x"
            eimiinojakoordinaatit.remove((x, y))
            return x, y

def ruudun_valinta(leveys, pituus):
    '''
    Kysyy käyttäjältä koordinaatit ruudun avausta varten.
    '''
    while True:
        try:
            koordinaatit = input("Anna koordinaatit.\n> ")
            x, y = koordinaatit.split(" ", 1)
            x = int(x)
            y = int(y)
            tottavaitarua = tarkista_koordinaatit(x, y, leveys, pituus)
            if tottavaitarua == False:
                print("Koordinaatit ovat ruudukon ulkopuolella.")
                continue
        except (IndexError):
            print("Anna kaksi koordinaattia välilyönnillä erotettuina.")
        except (ValueError, EOFError):
            print("Anna koordinaatit kokonaislukuina välilyönnillä erotettuina.")
        else:
            return x, y

def tarkista_koordinaatit(x, y, leveys, pituus):
    '''
    Tarkistaa, ovatko annetut koordinaatit rajojen sisällä.
    '''
    if x > (leveys - 1) or y > (pituus - 1) or x < 0 or y < 0:
        return False
    else:
        return True

def tulvataytto(kentta, x, y):
    '''
    Tarkistaa onko ruutu avaamaton. Tyhjät ruudut avataan flood fill -algoritmilla.
    '''
    aloituspiste = []
    aloituskoordinaatit = (x, y)
    aloituspiste.append(aloituskoordinaatit)
    if x >= len(kentta[0]) or x < 0 or y >= len(kentta) or y < 0:
        print("Koordinaatit ovat kentän ulkopuolella.")
    elif kentta[y][x] == "0" or kentta[y][x] == "1" or kentta[y][x] == "2" or kentta[y][x] == "3" or kentta[y][x] == "4" or kentta[y][x] == "5" or kentta[y][x] == "6" or kentta[y][x] == "7" or kentta[y][x] == "8":
        print("Numeroruudulle ei voi tehdä mitään, se kertoo montako miinaa sen ympärillä on.")
    elif kentta[y][x] == "x":
        return True
    elif kentta[y][x] == "_":
        kentta[y][x] = str(laske_miinat(x, y, kentta))
        if kentta[y][x] == "0":
            while True:
                if not aloituspiste:
                    break            
                x = aloituspiste[0][0]
                y = aloituspiste[0][1]
                if y - 1 >= 0:
                    if kentta[y-1][x] == "_":
                        kentta[y-1][x] = str(laske_miinat(x, y-1, kentta))
                        if kentta[y-1][x] == "0":
                            aloituspiste.append((x, y-1))
                if y + 1 < len(kentta):
                    if kentta[y+1][x] == "_":
                        kentta[y+1][x] = str(laske_miinat(x, y+1, kentta))
                        if kentta[y+1][x] == "0":
                            aloituspiste.append((x, y+1))
                if x - 1 >= 0:
                    if kentta[y][x-1] == "_":
                        kentta[y][x-1] = str(laske_miinat(x-1, y, kentta))
                        if kentta[y][x-1] == "0":
                            aloituspiste.append((x-1, y))
                if x + 1 < len(kentta[0]):
                    if kentta[y][x+1] == "_":
                        kentta[y][x+1] = str(laske_miinat(x+1, y, kentta))
                        if kentta[y][x+1] == "0":
                            aloituspiste.append((x+1, y))
                if y - 1 >= 0 and x - 1 >= 0:
                    if kentta[y-1][x-1] == "_":
                        kentta[y-1][x-1] = str(laske_miinat(x-1, y-1, kentta))
                        if kentta[y-1][x-1] == "0":
                            aloituspiste.append((x-1, y-1))
                if y - 1 >= 0 and x + 1 < len(kentta[0]):
                    if kentta[y-1][x+1] == "_":
                        kentta[y-1][x+1] = str(laske_miinat(x+1, y-1, kentta))
                        if kentta[y-1][x+1] == "0":
                            aloituspiste.append((x+1, y-1))
                if y + 1 < len(kentta) and x - 1 >= 0:
                    if kentta[y+1][x-1] == "_":
                        kentta[y+1][x-1] = str(laske_miinat(x-1, y+1, kentta))
                        if kentta[y+1][x-1] == "0":
                            aloituspiste.append((x-1, y+1))
                if y + 1 < len(kentta) and x + 1 < len(kentta[0]):
                    if kentta[y+1][x+1] == "_":
                        kentta[y+1][x+1] = str(laske_miinat(x+1, y+1, kentta))
                        if kentta[y+1][x+1] == "0":
                            aloituspiste.append((x+1, y+1))
                del aloituspiste[0]
    else:
        print("Ei tehty mitään.")

def laske_miinat(x, y, kentta):
    '''
    Laskee ruutua ympäröivät miinat.
    '''
    miinat_lkm = 0
    tottavaitarua = tarkista_koordinaatit(x-1, y, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y][x-1] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x+1, y, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y][x+1] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x, y-1, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y-1][x] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x, y+1, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y+1][x] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x-1, y-1, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y-1][x-1] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x+1, y+1, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y+1][x+1] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x+1, y-1, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y-1][x+1] == "x":
            miinat_lkm += 1
    tottavaitarua = tarkista_koordinaatit(x-1, y+1, len(kentta[0]), len(kentta))
    if tottavaitarua == True:
        if kentta[y+1][x-1] == "x":
            miinat_lkm += 1
    return miinat_lkm

def pelin_pyoritys(pituus, leveys, miinat, kentta):
    '''
    Pyörittää peliä, kunnes se loppuu.
    '''
    loppu = False
    vuorot = 0
    print("Peli alkaa nyt!")
    tulosta_kentta2(kentta)
    print("Koordinaatit syötetään välilyönnillä eroteltuina (esim. 3 5).")
    aika = datetime.datetime.now()
    ajankohta = datetime.date.today()
    tunnit = aika.hour
    while True:
        x, y = ruudun_valinta(leveys, pituus)
        vuorot += 1
        loppu = tulvataytto(kentta, x, y)
        if loppu == True:
            tulosta_kentta(kentta)
            print("Osuit miinaan! Hävisit pelin.")
            aika2 = datetime.datetime.now()
            minuutit = aika2.minute - aika.minute
            if minuutit < 0:
                minuutit = minuutit + 60
            sekunnit = aika2.second - aika.second
            if sekunnit < 0:
                sekunnit = sekunnit + 60
                minuutit = minuutit - 1
            print("Pelin kesto: {minuutit} minuuttia ja {sekunnit} sekuntia.".format(minuutit=minuutit, sekunnit=sekunnit))
            kesto = aika2 - aika
            #print(kesto)#ajan testausta varten
            tulos = "häviö"
            tilastoon_tallentaminen(ajankohta, aika, minuutit, sekunnit, vuorot, tulos, pituus, leveys, miinat)
            break
        else:
            kentta2 = deepcopy(kentta)
            for i in range(len(kentta2)):
                for j in range(len(kentta2[0])):
                    if kentta2[i][j] == "x":
                        kentta2[i][j] = "_"            
            tyhjat_ruudut = sum(rivi.count("_") for rivi in kentta2)
            if tyhjat_ruudut == miinat:
                tulosta_kentta(kentta)
                print("Miinat raivattu! Voitit pelin.")
                aika2 = datetime.datetime.now()
                minuutit = aika2.minute - aika.minute
                if minuutit < 0:
                    minuutit = minuutit + 60
                sekunnit = aika2.second - aika.second
                if sekunnit < 0:
                    sekunnit = sekunnit + 60
                    minuutit = minuutit - 1
                print("Pelin kesto: {minuutit} minuuttia ja {sekunnit} sekuntia.".format(minuutit=minuutit, sekunnit=sekunnit))
                kesto = aika2 - aika
                #print(kesto)#ajan testausta varten
                tulos = "voitto"
                tilastoon_tallentaminen(ajankohta, aika, minuutit, sekunnit, vuorot, tulos, pituus, leveys, miinat)
                break
            tulosta_kentta2(kentta)

def tulosta_kentta(kentta):
    '''
    Tulostaa pelikentän miinat mukaanlukien.
    '''
    pituus = len(kentta)
    i = 0
    print()
    while i != pituus:
        print(" ".join(kentta[i]))
        i = i + 1

def tulosta_kentta2(kentta):
    '''
    Tulostaa pelikentän niin, että miinat on muutettu tulostuksessa tyhjiksi pelaajan näkymää varten.
    ''' 
    print()
    kentta2 = deepcopy(kentta)
    for i in range(len(kentta2)):
        for j in range(len(kentta2[0])):
            if kentta2[i][j] == "x":
                kentta2[i][j] = "_"
    
    pituus = len(kentta2)
    i = 0
    while i != pituus:
        print(" ".join(kentta2[i]))
        i = i + 1
    #alla oleva laittaa numerot vasemmalle puolen kenttää
    #for l, ruutu in enumerate(kentta2):
        #print(l, " ".join(ruutu))

'''
Main-funktio. Näyttää valikon.
'''
print("\nMIINAHARAVA\nTehnyt: Mikko Pulli 2016")
while True:
    print("(U)usi peli")
    print("(T)ilastot")
    print("(L)opetus")
    valinta = input("> ").strip().lower()
    if valinta == "u":
        pelivalinnat()
    elif valinta == "t":
        tilaston_naytto()
    elif valinta == "l":
        break
    else:
        print("Väärä komento. Kirjoita u, t tai l ja paina enteriä.")