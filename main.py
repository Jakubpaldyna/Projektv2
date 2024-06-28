import folium
import webbrowser
from geopy.geocoders import Nominatim

# Przykładowe dane
teatry = [
    {"nazwa": "Teatr Wielki", "adres": "plac Teatralny 1, Warszawa", "współrzędne": "52.24356, 21.00142"},
    {"nazwa": "Teatr Narodowy", "adres": "plac Teatralny 3, Warszawa", "współrzędne": "52.2446, 21.0035"}
]

klienci = {
    "Teatr Wielki": ["Jan Kowalski", "Anna Nowak"],
    "Teatr Narodowy": ["Piotr Wiśniewski"]
}

pracownicy = {
    "Teatr Wielki": ["Michał Lewandowski", "Zofia Kaczmarek"],
    "Teatr Narodowy": ["Katarzyna Zielińska"]
}

geolocator = Nominatim(user_agent="teatr_locator")

# Logowanie
def login():
    print("Witaj w systemie zarządzania teatrami.")
    nazwa_uzytkownika = input("Podaj nazwę użytkownika: ")
    haslo = input("Podaj hasło dostępu: ")
    print(f"Próba logowania jako: {nazwa_uzytkownika}, hasło: {haslo}")  # Dodatkowe informacje diagnostyczne
    if nazwa_uzytkownika == "admin" and haslo == "admin":
        print("Zalogowano pomyślnie.")
        return True
    else:
        print("Niepoprawna nazwa użytkownika lub hasło.")
        return False
# Funkcja read
def read_teatry():
    print("Lista teatrów:")
    for teatr in teatry:
        print(f"{teatr['nazwa']}, adres: {teatr['adres']}, współrzędne: {teatr.get('współrzędne', 'Brak')}")

def read_klienci(teatr):
    if teatr in klienci:
        print(f"Klienci {teatr}:")
        for klient in klienci[teatr]:
            print(f"- {klient}")
    else:
        print("Nie znaleziono teatru o podanej nazwie.")

def read_pracownicy(teatr):
    if teatr in pracownicy:
        print(f"Pracownicy {teatr}:")
        for pracownik in pracownicy[teatr]:
            print(f"- {pracownik}")
    else:
        print("Nie znaleziono teatru o podanej nazwie.")

def read_współrzędne():
    for teatr in teatry:
        print(f"Nazwa: {teatr['nazwa']}, Współrzędne: {teatr.get('współrzędne', 'Brak')}")

# Funkcja create
def create_teatry(nazwa, adres):
    location = geolocator.geocode(adres)
    if location:
        wspolrzedne = f"{location.latitude}, {location.longitude}"
        teatry.append({'nazwa': nazwa, 'adres': adres, 'współrzędne': wspolrzedne})
        print(f"Dodano teatr: {nazwa}, adres: {adres}, współrzędne: {wspolrzedne}")
    else:
        print(f"Nie udało się pobrać współrzędnych dla adresu: {adres}")

def create_klienci(teatr, klient):
    if teatr in klienci:
        klienci[teatr].append(klient)
    else:
        klienci[teatr] = [klient]
    print(f"Dodano klienta {klient} do teatru {teatr}")

def create_pracownicy(teatr, pracownik):
    if teatr in pracownicy:
        pracownicy[teatr].append(pracownik)
    else:
        pracownicy[teatr] = [pracownik]
    print(f"Dodano pracownika {pracownik} do teatru {teatr}")

# Funkcja update
def update_teatry(nazwa, nowy_adres):
    location = geolocator.geocode(nowy_adres)
    if location:
        nowe_wspolrzedne = f"{location.latitude}, {location.longitude}"
        for teatr in teatry:
            if teatr['nazwa'] == nazwa:
                teatr['adres'] = nowy_adres
                teatr['współrzędne'] = nowe_wspolrzedne
                print(f"Zaktualizowano adres i współrzędne teatru {nazwa} na {nowy_adres}, {nowe_wspolrzedne}")
                return
        print("Nie znaleziono teatru o podanej nazwie.")
    else:
        print(f"Nie udało się pobrać współrzędnych dla adresu: {nowy_adres}")

def update_klienci(teatr, stary_klient, nowy_klient):
    if teatr in klienci:
        if stary_klient in klienci[teatr]:
            klienci[teatr][klienci[teatr].index(stary_klient)] = nowy_klient
            print(f"Zaktualizowano klienta {stary_klient} na {nowy_klient} w teatrze {teatr}")
        else:
            print(f"Nie znaleziono klienta {stary_klient} w teatrze {teatr}")
    else:
        print(f"Nie znaleziono teatru {teatr}")

def update_pracownicy(teatr, stary_pracownik, nowy_pracownik):
    if teatr in pracownicy:
        if stary_pracownik in pracownicy[teatr]:
            pracownicy[teatr][pracownicy[teatr].index(stary_pracownik)] = nowy_pracownik
            print(f"Zaktualizowano pracownika {stary_pracownik} na {nowy_pracownik} w teatrze {teatr}")
        else:
            print(f"Nie znaleziono pracownika {stary_pracownik} w teatrze {teatr}")
    else:
        print(f"Nie znaleziono teatru {teatr}")

# Funkcja remove
def remove_teatry(nazwa):
    global teatry
    teatry = [teatr for teatr in teatry if teatr['nazwa'] != nazwa]
    print(f"Usunięto teatr {nazwa}")

def remove_klienci(teatr, klient):
    if teatr in klienci:
        if klient in klienci[teatr]:
            klienci[teatr].remove(klient)
            print(f"Usunięto klienta {klient} z teatru {teatr}")
        else:
            print(f"Nie znaleziono klienta {klient} w teatrze {teatr}")
    else:
        print(f"Nie znaleziono teatru {teatr}")

def remove_pracownicy(teatr, pracownik):
    if teatr in pracownicy:
        if pracownik in pracownicy[teatr]:
            pracownicy[teatr].remove(pracownik)
            print(f"Usunięto pracownika {pracownik} z teatru {teatr}")
        else:
            print(f"Nie znaleziono pracownika {pracownik} w teatrze {teatr}")
    else:
        print(f"Nie znaleziono teatru {teatr}")

# Funkcje do generowania map
def generuj_mape_teatrow(teatry):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    for teatr in teatry:
        nazwa = teatr['nazwa']
        adres = teatr['adres']
        wspolrzedne = teatr.get('współrzędne')
        pracownicy_teatr = pracownicy.get(nazwa, [])
        klienci_teatr = klienci.get(nazwa, [])
        pracownicy_label = "<br>".join(pracownicy_teatr)
        klienci_label = "<br>".join(klienci_teatr)

        if wspolrzedne:
            lat, lon = map(float, wspolrzedne.split(', '))
            folium.Marker(
                location=[lat, lon],
                popup=f"{nazwa}<br>{adres}<br><b>Pracownicy:</b><br>{pracownicy_label}<br><b>Klienci:</b><br>{klienci_label}",
                tooltip=nazwa
            ).add_to(m)
    nazwa_pliku = 'mapa_teatrow.html'
    m.save(nazwa_pliku)
    print(f"Mapa teatrów została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)


def generuj_mape_pracownikow(teatr):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    if teatr in pracownicy:
        pracownicy_teatr = pracownicy[teatr]
        teatr_info = next((t for t in teatry if t['nazwa'] == teatr), None)
        if teatr_info and teatr_info.get('współrzędne'):
            lat, lon = map(float, teatr_info['współrzędne'].split(', '))
            popup_content = "<br>".join(pracownicy_teatr)
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"Pracownicy teatru: {', '.join(pracownicy_teatr)}"
            ).add_to(m)
    nazwa_pliku = f'mapa_pracownikow_{teatr.replace(" ", "_")}.html'
    m.save(nazwa_pliku)
    print(f"Mapa pracowników teatru '{teatr}' została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)

def generuj_mape_klientow(teatr):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    if teatr in klienci:
        for klient in klienci[teatr]:
            teatr_info = next((t for t in teatry if t['nazwa'] == teatr), None)
            if teatr_info and teatr_info.get('współrzędne'):
                lat, lon = map(float, teatr_info['współrzędne'].split(', '))
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{klient}",
                    tooltip=klient
                ).add_to(m)
    nazwa_pliku = f'mapa_klientow_{teatr.replace(" ", "_")}.html'
    m.save(nazwa_pliku)
    print(f"Mapa klientów teatru '{teatr}' została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)


def generuj_mape_wszystkiego():
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)

    for teatr in teatry:
        nazwa = teatr['nazwa']
        adres = teatr['adres']
        wspolrzedne = teatr.get('współrzędne')
        pracownicy_teatr = pracownicy.get(nazwa, [])
        klienci_teatr = klienci.get(nazwa, [])
        pracownicy_label = "<br>".join(pracownicy_teatr)
        klienci_label = "<br>".join(klienci_teatr)

        if wspolrzedne:
            lat, lon = map(float, wspolrzedne.split(', '))
            folium.Marker(
                location=[lat, lon],
                popup=f"{nazwa}<br>{adres}<br><b>Pracownicy:</b><br>{pracownicy_label}<br><b>Klienci:</b><br>{klienci_label}",
                tooltip=nazwa
            ).add_to(m)

    nazwa_pliku = 'mapa_wszystkiego.html'
    m.save(nazwa_pliku)
    print(f"Mapa wszystkiego została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)
def main():
    if login():
        while True:
            print("\nWybierz opcję:")
            print("1. Wyświetl teatry")
            print("2. Dodaj teatr")
            print("3. Aktualizuj teatr")
            print("4. Usuń teatr")
            print("5. Wyświetl klientów teatru")
            print("6. Dodaj klienta do teatru")
            print("7. Aktualizuj klienta w teatrze")
            print("8. Usuń klienta z teatru")
            print("9. Wyświetl pracowników teatru")
            print("10. Dodaj pracownika do teatru")
            print("11. Aktualizuj pracownika w teatrze")
            print("12. Usuń pracownika z teatru")
            print("13. Generuj mapę teatrów")
            print("14. Generuj mapę pracowników dla teatru")
            print("15. Generuj mapę klientów dla teatru")
            print("16. Generuj mapę wszystkiego")
            print("17. Wyjdź z programu")

            opcja = input("Podaj numer opcji: ")

            if opcja == "1":
                for teatr in teatry:
                    print(f"{teatr['nazwa']}, adres: {teatr['adres']}, współrzędne: {teatr.get('współrzędne', 'Brak')}")
            elif opcja == "2":
                nazwa = input("Podaj nazwę teatru: ")
                adres = input("Podaj adres teatru: ")
                location = geolocator.geocode(adres)
                if location:
                    wspolrzedne = f"{location.latitude}, {location.longitude}"
                    teatry.append({'nazwa': nazwa, 'adres': adres, 'współrzędne': wspolrzedne})
                    print(f"Dodano teatr: {nazwa}, adres: {adres}, współrzędne: {wspolrzedne}")
                else:
                    print(f"Nie udało się pobrać współrzędnych dla adresu: {adres}")
            elif opcja == "3":
                nazwa = input("Podaj nazwę teatru do aktualizacji: ")
                nowy_adres = input("Podaj nowy adres teatru: ")
                teatr = next((t for t in teatry if t['nazwa'] == nazwa), None)
                if teatr:
                    teatr['adres'] = nowy_adres
                    location = geolocator.geocode(nowy_adres)
                    if location:
                        teatr['współrzędne'] = f"{location.latitude}, {location.longitude}"
                    else:
                        print(f"Nie udało się zaktualizować współrzędnych dla teatru: {nazwa}")
                    print(f"Aktualizacja teatru {nazwa} zakończona pomyślnie.")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa}")
            elif opcja == "4":
                nazwa = input("Podaj nazwę teatru do usunięcia: ")
                teatr = next((t for t in teatry if t['nazwa'] == nazwa), None)
                if teatr:
                    teatry.remove(teatr)
                    klienci.pop(nazwa, None)
                    pracownicy.pop(nazwa, None)
                    print(f"Teatr {nazwa} został pomyślnie usunięty.")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa}")
            elif opcja == "5":
                nazwa_teatru = input("Podaj nazwę teatru, dla którego chcesz wyświetlić klientów: ")
                read_klienci(nazwa_teatru)
            elif opcja == "6":
                nazwa_teatru = input("Podaj nazwę teatru, do którego chcesz dodać klienta: ")
                if nazwa_teatru in klienci:
                    nowy_klient = input("Podaj imię i nazwisko nowego klienta: ")
                    klienci[nazwa_teatru].append(nowy_klient)
                    print(f"Dodano klienta {nowy_klient} do teatru {nazwa_teatru}.")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "7":
                nazwa_teatru = input("Podaj nazwę teatru, w którym chcesz zaktualizować klienta: ")
                if nazwa_teatru in klienci:
                    stary_klient = input("Podaj imię i nazwisko aktualizowanego klienta: ")
                    if stary_klient in klienci[nazwa_teatru]:
                        nowy_klient = input("Podaj nowe imię i nazwisko klienta: ")
                        klienci[nazwa_teatru][klienci[nazwa_teatru].index(stary_klient)] = nowy_klient
                        print(f"Zaktualizowano klienta {stary_klient} na {nowy_klient} w teatrze {nazwa_teatru}.")
                    else:
                        print(f"Nie znaleziono klienta o nazwie: {stary_klient}")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "8":
                nazwa_teatru = input("Podaj nazwę teatru, z którego chcesz usunąć klienta: ")
                if nazwa_teatru in klienci:
                    klient_do_usuniecia = input("Podaj imię i nazwisko klienta do usunięcia: ")
                    if klient_do_usuniecia in klienci[nazwa_teatru]:
                        klienci[nazwa_teatru].remove(klient_do_usuniecia)
                        print(f"Usunięto klienta {klient_do_usuniecia} z teatru {nazwa_teatru}.")
                    else:
                        print(f"Nie znaleziono klienta o nazwie: {klient_do_usuniecia}")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "9":
                nazwa_teatru = input("Podaj nazwę teatru, dla którego chcesz wyświetlić pracowników: ")
                if nazwa_teatru in pracownicy:
                    print(f"Pracownicy teatru {nazwa_teatru}:")
                    for pracownik in pracownicy[nazwa_teatru]:
                        print(f"- {pracownik}")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "10":
                nazwa_teatru = input("Podaj nazwę teatru, do którego chcesz dodać pracownika: ")
                if nazwa_teatru in pracownicy:
                    nowy_pracownik = input("Podaj imię i nazwisko nowego pracownika: ")
                    pracownicy[nazwa_teatru].append(nowy_pracownik)
                    print(f"Dodano pracownika {nowy_pracownik} do teatru {nazwa_teatru}.")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "11":
                nazwa_teatru = input("Podaj nazwę teatru, w którym chcesz zaktualizować pracownika: ")
                if nazwa_teatru in pracownicy:
                    stary_pracownik = input("Podaj imię i nazwisko aktualizowanego pracownika: ")
                    if stary_pracownik in pracownicy[nazwa_teatru]:
                        nowy_pracownik = input("Podaj nowe imię i nazwisko pracownika: ")
                        pracownicy[nazwa_teatru][pracownicy[nazwa_teatru].index(stary_pracownik)] = nowy_pracownik
                        print(f"Zaktualizowano pracownika {stary_pracownik} na {nowy_pracownik} w teatrze {nazwa_teatru}.")
                    else:
                        print(f"Nie znaleziono pracownika o nazwie: {stary_pracownik}")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "12":
                nazwa_teatru = input("Podaj nazwę teatru, z którego chcesz usunąć pracownika: ")
                if nazwa_teatru in pracownicy:
                    pracownik_do_usuniecia = input("Podaj imię i nazwisko pracownika do usunięcia: ")
                    if pracownik_do_usuniecia in pracownicy[nazwa_teatru]:
                        pracownicy[nazwa_teatru].remove(pracownik_do_usuniecia)
                        print(f"Usunięto pracownika {pracownik_do_usuniecia} z teatru {nazwa_teatru}.")
                    else:
                        print(f"Nie znaleziono pracownika o nazwie: {pracownik_do_usuniecia}")
                else:
                    print(f"Nie znaleziono teatru o nazwie: {nazwa_teatru}")
            elif opcja == "13":
                generuj_mape_teatrow(teatry)
            elif opcja == "14":
                nazwa_teatru = input("Podaj nazwę teatru, dla którego chcesz wygenerować mapę pracowników: ")
                generuj_mape_pracownikow(nazwa_teatru)
            elif opcja == "15":
                nazwa_teatru = input("Podaj nazwę teatru, dla którego chcesz wygenerować mapę klientów: ")
                generuj_mape_klientow(nazwa_teatru)
            elif opcja == "16":
                generuj_mape_wszystkiego()
            elif opcja == "17":
                print("Wylogowano.")
                break
            else:
                print("Niepoprawny numer opcji. Spróbuj ponownie.")

if __name__ == "__main__":
    main()