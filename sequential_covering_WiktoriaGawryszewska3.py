from itertools import combinations  # do tworzenia kombinacji atrybutów

# Wczytywanie danych z pliku
plik = open("C:/Users/Wiktoria/Desktop/dane.txt", "r")
linie = plik.readlines()
plik.close()

dane = []
for linia in linie:
    liczby = linia.strip().split()  # usuń znaki nowej linii i podziel po spacji
    dane.append([int(liczba) for liczba in liczby])  # zamień na liczby całkowite

# Funkcja do generowania reguł (algorytm sequential covering)
def sequential_covering(dane):
    liczba_atrybutow = len(dane[0]) - 1  # ostatnia kolumna to decyzja, więc odejmujemy 1
    do_pokrycia = set(range(len(dane)))  # indeksy obiektów, które jeszcze nie mają reguły
    reguly = []  # końcowa lista reguł
    rzad = 1  # zaczynamy od reguł jednoczynnikowych (1 cecha)

    # Dopóki są obiekty do pokrycia i nie przekroczono liczby atrybutów
    while len(do_pokrycia) > 0 and rzad <= liczba_atrybutow:
        nowe_reguly = []  # reguły znalezione w tym rzędzie

        # Przejdź po wszystkich niepokrytych obiektach
        for idx_obiektu in sorted(do_pokrycia):
            obiekt = dane[idx_obiektu]  # pobierz aktualny obiekt

            # Wygeneruj wszystkie kombinacje atrybutów o długości 'rzad'
            kombinacje = combinations(range(liczba_atrybutow), rzad)
            for kombinacja in kombinacje:
                # Pobierz wartości atrybutów z tej kombinacji dla danego obiektu
                wartosc_klucz = tuple(obiekt[i] for i in kombinacja)

                # Szukamy obiektów, które mają takie same wartości w tej kombinacji
                obiekty_o_tych_wartosciach = []
                for i, obj in enumerate(dane):
                    obj_wartosc = tuple(obj[j] for j in kombinacja)
                    if obj_wartosc == wartosc_klucz:
                        obiekty_o_tych_wartosciach.append((i, obj[-1]))  # (indeks, decyzja)

                # Sprawdź, czy wszystkie obiekty mają tę samą decyzję
                decyzje = [dec for (_, dec) in obiekty_o_tych_wartosciach]
                if len(set(decyzje)) == 1:  # jeśli decyzje są zgodne

                    # Zbuduj warunki do reguły w postaci tekstu
                    warunki = " ∧ ".join(
                        f"(a{i + 1} = {wartosc_klucz[pos]})"
                        for pos, i in enumerate(kombinacja)
                    )

                    # Zbierz pokryte obiekty spośród niepokrytych
                    pokryte_z_niepokrytych = [idx for (idx, _) in obiekty_o_tych_wartosciach if idx in do_pokrycia]

                    # Tylko jeśli reguła pokrywa coś nowego i nie jest sprzeczna
                    if len(set(decyzje)) == 1 and pokryte_z_niepokrytych:

                        support = len(obiekty_o_tych_wartosciach)  # wszystkie pasujące, nie tylko niepokryte
                        if support > 1:
                            tekst_reguly = f"{warunki} ⇒ (d = {decyzje[0]}) [{support}]"

                        else:
                            tekst_reguly = f"{warunki} ⇒ (d = {decyzje[0]})"

                        # Dodaj nową regułę do listy z tego rzędu
                        nowe_reguly.append(tekst_reguly)

                        # Usuń pokryte obiekty z listy do pokrycia
                        do_pokrycia -= set(pokryte_z_niepokrytych)

                        break  # przejdź do następnego obiektu

        # Jeśli w tym rzędzie udało się coś znaleźć, dodaj do końcowej listy
        if nowe_reguly:
            reguly.append((rzad, nowe_reguly))

        # Jeśli nic nie znaleziono, przejdź do wyższego rzędu
        if not nowe_reguly:
            rzad += 1
            continue


    rzad += 1

    return reguly  # zwróć wszystkie znalezione reguły

# Uruchomienie algorytmu i wypisanie wyniku
reguly = sequential_covering(dane)

# Wypisz każdą regułę, pogrupowaną według rzędu
for rzad, lista_regul in reguly:
    print(f"\nReguły {rzad} rzędu:")
    for r in lista_regul:
        print(r)
