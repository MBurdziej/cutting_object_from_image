import cv2
import numpy as np

def czarny(obraz):
    wysokosc, szerokosc, _ = obraz.shape
    obraz2 = np.zeros((wysokosc, szerokosc), dtype=np.uint8)
    for i in range(wysokosc):
        for j in range(szerokosc):
            obraz2[i][j] = 0.299 * obraz[i][j][0] + 0.587 * obraz[i][j][1] + 0.114 * obraz[i][j][2]
    return obraz2

def roznice_czarne(obraz_org, obraz_edit):
    wysokosc, szerokosc = obraz_org.shape
    obraz2 = np.zeros_like(obraz_org)
    for i in range(wysokosc):
        for j in range(szerokosc):
            obraz2[i][j] = np.abs(int(obraz_edit[i][j]) - int(obraz_org[i][j]))
    return obraz2

def binarny(obraz_czarny, prog):
    wysokosc, szerokosc = obraz_czarny.shape
    obraz2 = np.zeros_like(obraz_czarny)
    for i in range(wysokosc):
        for j in range(szerokosc):
            if int(obraz_czarny[i][j]) > prog:
                obraz2[i][j] = 255
    return obraz2

def erozja3(obraz):
    wysokosc, szerokosc = obraz.shape
    obraz2 = np.zeros_like(obraz)

    for i in range(1, wysokosc - 1):
        for j in range(1, szerokosc- 1):
            erodowany = np.min(obraz[i - 1:i + 2, j - 1:j + 2])

            obraz2[i][j] = erodowany
    return obraz2

def erozja2(obraz):
    wysokosc, szerokosc = obraz.shape
    obraz2 = np.zeros_like(obraz)

    for i in range(1, wysokosc):
        for j in range(1, szerokosc):
            erodowany = np.min(obraz[i - 1:i + 1, j - 1:j + 1])

            obraz2[i][j] = erodowany
    return obraz2

def delatacja2(obraz):
    wysokosc, szerokosc = obraz.shape
    obraz2 = np.zeros_like(obraz)

    for i in range(1, wysokosc):
        for j in range(1, szerokosc):
            delod = np.max(obraz[i - 1:i + 1, j - 1:j + 1])

            obraz2[i][j] = delod
    return obraz2

def delatacja3(obraz):
    wysokosc, szerokosc = obraz.shape
    obraz2 = np.zeros_like(obraz)

    for i in range(1, wysokosc - 1):
        for j in range(1, szerokosc- 1):
            delat = np.max(obraz[i - 1:i + 2, j - 1:j + 2])

            obraz2[i][j] = delat
    return obraz2

# Tworzenie funkcji do znalezienia obszarów punktów
def znajdz_ramki(obraz):
    wspolrzedne_ramek = []
    wysokosc, szerokosc = obraz.shape

    czy_w_obszarze = 0
    obszar = []

    for i in range(wysokosc):
        for j in range(szerokosc):
            if obraz[i][j] > 250:
                if not czy_w_obszarze:
                    czy_w_obszarze = 1
                    obszar = [(j, i)]
                else:
                    obszar.append((j, i))
            else:
                if czy_w_obszarze:
                    x_min = obszar[0][0]
                    y_min = obszar[0][1]
                    x_max = obszar[0][0]
                    y_max = obszar[0][1]
                    for point in obszar:
                        x = point[0]
                        y = point[1]
                        if x < x_min:
                            x_min = x
                        if y < y_min:
                            y_min = y
                        if x > x_max:
                            x_max = x
                        if y > y_max:
                            y_max = y

                    dodany = 0
                    for k, ramka in enumerate(wspolrzedne_ramek):
                        x1, y1, x2, y2 = ramka
                        if (abs((x1 + x2) / 2 - (x_min + x_max) / 2) < 70 and abs((y1 + y2) / 2 - (y_min + y_max) / 2) < 70):
                            wspolrzedne_ramek[k] = (min(x1, x_min), min(y1, y_min), max(x2, x_max),max(y2, y_max))
                            dodany = 1
                            break

                    if not dodany:
                        wspolrzedne_ramek.append((x_min-1, y_min-1, x_max+1, y_max+1))

                    czy_w_obszarze = 0

    return wspolrzedne_ramek

def obraz_z_ramkami(obraz_edit, ramki_wsp):
    obraz2 = np.copy(obraz_edit)

    for ramka in ramki_wsp:
        x_min, y_min, x_max, y_max = ramka
        
        for x in range(x_min, x_max + 1):
            obraz2[y_min, x] = [255, 0, 255]
            obraz2[y_max, x] = [255, 0, 255]
        
        for y in range(y_min, y_max + 1):
            obraz2[y, x_min] = [255, 0, 255]
            obraz2[y, x_max] = [255, 0, 255]
    return obraz2

def wytnij_ramke(obraz_edit, ramki_wsp):
    najwieksze_y = 0
    najwieksza_ramka = [0]*4
    for ramka in ramki_wsp:
        x_min, y_min, x_max, y_max = ramka
        temp = y_max-y_min
        if temp > najwieksze_y:
            najwieksze_y = temp
            najwieksza_ramka = ramka

    x_min2, y_min2, x_max2, y_max2 = najwieksza_ramka
    obraz2 = np.zeros((y_max2-y_min2, x_max2-x_min2, 3), dtype=np.uint8)
    wysokosc, szerokosc, _ = obraz2.shape
    for i in range(wysokosc):
        for j in range(szerokosc):
            obraz2[i][j] = obraz_edit[i+y_min2][j+x_min2]
    return obraz2

def wytnij_ramke_czarny(obraz_edit, ramki_wsp):
    najwieksze_y = 0
    najwieksza_ramka = [0]*4
    for ramka in ramki_wsp:
        x_min, y_min, x_max, y_max = ramka
        temp = y_max-y_min
        if temp > najwieksze_y:
            najwieksze_y = temp
            najwieksza_ramka = ramka

    x_min2, y_min2, x_max2, y_max2 = najwieksza_ramka
    obraz2 = np.zeros((y_max2-y_min2, x_max2-x_min2), dtype=np.uint8)
    wysokosc, szerokosc = obraz2.shape
    for i in range(wysokosc):
        for j in range(szerokosc):
            obraz2[i][j] = obraz_edit[i+y_min2][j+x_min2]
    return obraz2

def usun_tlo(wyciety_box, wyciety_box_roznice):
    wysokosc, szerokosc, _ = wyciety_box.shape
    obraz2 = np.zeros((wysokosc, szerokosc, 4), dtype=np.uint8)
    for i in range(wysokosc):
        for j in range(szerokosc):
            obraz2[i][j][:3] = wyciety_box[i][j][:3]
            if wyciety_box_roznice[i][j] == 255:
                obraz2[i][j][3] = 255
            else:
                obraz2[i][j][3] = 0
    return obraz2

obraz_org = cv2.imread('org.jpg')
obraz_edit = cv2.imread('edited.jpg')

obraz_org_czarny = czarny(obraz_org)
obraz_edit_czarny = czarny(obraz_edit)

obraz_roznice = roznice_czarne(obraz_org_czarny, obraz_edit_czarny)

obraz_binarny = binarny(obraz_roznice, 10)
erod = erozja3(obraz_binarny)
ramki_wsp = znajdz_ramki(erod)
obraz_z_boxami = obraz_z_ramkami(obraz_edit, ramki_wsp)
cv2.imwrite('obraz_z_ramkami.jpg', obraz_z_boxami)

wyciety_box = wytnij_ramke(obraz_edit, ramki_wsp)
cv2.imwrite('wyciety.jpg', wyciety_box)

wyciety_box_roznice = wytnij_ramke_czarny(obraz_roznice, ramki_wsp)

wyciety_binarny = binarny(wyciety_box_roznice, 13)

delat = delatacja2(wyciety_binarny)
delat = erozja2(delat)
delat = erozja2(delat)


bez_tla = usun_tlo(wyciety_box, delat)
cv2.imwrite('bez_tla.PNG', bez_tla)