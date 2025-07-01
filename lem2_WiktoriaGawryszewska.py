import pandas as pd

# Funkcja wczytująca dane z pliku
def wczytaj_dane(sciezka):
    df = pd.read_csv(sciezka, sep=" ", header=None)  # Wczytanie danych
    kolumny = [f'a{i+1}' for i in range(df.shape[1]-1)] + ['decyzja']  # Nazwy kolumn oraz ostatnia jako 'decyzja'
    df.columns = kolumny  # Ustawienie nazw kolumn
    return df

# Funkcja znajdująca najczęściej występujący atrybut-wartość w zadanym zbiorze obiektów i atrybutów
def znajdz_najczestszy(df, indeksy, atrybuty):
    licznik = {}
    for atr in atrybuty:
        wartosci = df.loc[indeksy, atr]
        for val in wartosci:
            licznik[(atr, val)] = licznik.get((atr, val), 0) + 1
    return max(licznik.items(), key=lambda x: x[1])[0]  # Zwraca parę (atrybut, wartość) z największą liczbą wystąpień

# Funkcja zwracająca indeksy obiektów spełniających wszystkie warunki (lista par atrybut-wartość)
def obiekty_spelniajace(df, warunki):
    filt = df.index
    for atr, val in warunki:
        filt = filt.intersection(df.index[df[atr] == val])
    return set(filt)

# Budowanie jednej reguły pokrywającej obiekty danej klasy (klasa) wśród niepokrytych obiektów
def zbuduj_regule(df, klasa, atrybuty, niepokryte):
    start = znajdz_najczestszy(df, list(niepokryte), atrybuty)  # Startujemy od najczęstszej pary (atrybut, wartość)
    warunki = [start]

    while True:
        dopasowane = obiekty_spelniajace(df, warunki)  # Obiekty spełniające dotychczasowe warunki
        if all(df.loc[i, 'decyzja'] == klasa for i in dopasowane):  # Jeśli wszystkie mają tę samą klasę, kończymy
            break

        kandydaci = dopasowane & niepokryte  # Obiekty jeszcze niepokryte, które spełniają obecne warunki
        if not kandydaci:
            break

        wybrany = df.loc[min(cand for cand in kandydaci)]  # Wybór pierwszego (o najmniejszym indeksie) niepokrytego obiektu
        kandydatury = []

        for atr in atrybuty:
            propozycja = (atr, wybrany[atr])
            if propozycja not in warunki:  # Dodajemy tylko nowe warunki
                tymczasowe = warunki + [propozycja]
                dop = obiekty_spelniajace(df, tymczasowe)
                pokrycie = sum(df.loc[i, 'decyzja'] == klasa for i in dop)
                kandydatury.append((propozycja, pokrycie))

        if not kandydatury:
            break

        # Sortujemy kandydatów: najpierw po największym pokryciu, potem po kolejności atrybutów
        kandydatury.sort(key=lambda x: (-x[1], list(atrybuty).index(x[0][0])))
        warunki.append(kandydatury[0][0])  # Dodajemy najlepszy warunek

    pokryte = obiekty_spelniajace(df, warunki) & niepokryte  # Obiekty pokryte przez regułę
    return warunki, klasa, len(pokryte), pokryte  # Zwracamy regułę (warunki, klasa), jej support i pokryte obiekty

# Główna funkcja implementująca algorytm LEM2
def lem2_algorytm(df):
    atrybuty = df.columns[:-1]  # Wszystkie kolumny oprócz decyzja
    klasy = sorted(df['decyzja'].unique())  # Lista unikalnych klas decyzyjnych
    reguly = []

    for k in klasy:
        pozostale = set(df.index[df['decyzja'] == k])  # Indeksy obiektów danej klasy
        while pozostale:
            warunki, klasa, sup, pokryte = zbuduj_regule(df, k, atrybuty, pozostale)
            reguly.append((warunki, klasa, sup))
            pozostale -= pokryte  # Usuwamy pokryte obiekty

    return reguly  # Zwraca listę reguł

# Funkcja łącząca reguły o tych samych warunkach ale różnych klasach
def scal_reguly(reguly):
    zgrupowane = []
    for warunki, klasa, sup in reguly:
        znalezione = False
        for z in zgrupowane:
            if set(z['warunki']) == set(warunki):
                z['klasy'].add(klasa)
                z['support'] += sup
                znalezione = True
                break
        if not znalezione:
            zgrupowane.append({'warunki': warunki, 'klasy': {klasa}, 'support': sup})
    return zgrupowane

# Funkcja wypisująca reguły w czytelnej formie
def wypisz(reguly):
    for i, regula in enumerate(reguly, 1):
        cz1 = " ∧ ".join(f"({x} = {y})" for x, y in regula['warunki'])
        cz2 = " | ".join(f"(d = {k})" for k in sorted(regula['klasy']))
        cz3 = f"[{regula['support']}]" if regula['support'] > 1 else ""
        print(f"rule {i}: {cz1} => {cz2}{cz3}")

# Wywołanie algorytmu na danych z pliku
df = wczytaj_dane("C:/Users/Wiktoria/Desktop/dane11.txt")
reguly = lem2_algorytm(df)
scalone = scal_reguly(reguly)
wypisz(scalone)
