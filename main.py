from geopy.geocoders import Nominatim
import folium
import webbrowser

# Przykładowe dane
teatry = [
    {"nazwa": "Teatr Wielki", "adres": "plac Teatralny 1, Warszawa", "współrzędne": "52.243, 21.001"},
    {"nazwa": "Teatr Narodowy", "adres": "plac Teatralny 3, Warszawa", "współrzędne": "52.243, 21.002"}
]

klienci = {
    "Teatr Wielki": ["Jan Kowalski", "Anna Nowak"],
    "Teatr Narodowy": ["Piotr Wiśniewski"]
}

pracownicy = {
    "Teatr Wielki": ["Michał Lewandowski", "Zofia Kaczmarek"],
    "Teatr Narodowy": ["Katarzyna Zielińska"]
}

# funkcja read
def read_teatry():
    print("Lista teatrów:")
    for teatr in teatry:
        print(f"{teatr['nazwa']}, adres: {teatr['adres']}, współrzędne: {teatr['współrzędne']}")

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
        print(f"Nazwa: {teatr['nazwa']}, Współrzędne: {teatr['współrzędne']}")

# Funkcja create
def create_teatry(nazwa, adres):
    geolocator = Nominatim(user_agent="teatr_locator")
    location = geolocator.geocode(adres)
    if location:
        wspolrzedne = f"{location.latitude}, {location.longitude}"
        teatry.append({'nazwa': nazwa, 'adres': adres, 'współrzędne': wspolrzedne})
        print(f"Dodano teatr: {nazwa}, adres: {adres}, współrzędne: {wspolrzedne}")
    else:
        print(f"Nie udało się pobrać współrzędnych dla adresu: {adres}")

def create_klienci(teatr, klient, spektakle):
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
    geolocator = Nominatim(user_agent="teatr_locator")
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

def update_klienci(teatr, klient, nowe_spektakle):
    if teatr in klienci and klient in klienci[teatr]:
        klienci[teatr][klient] = nowe_spektakle
        print(f"Zaktualizowano spektakle klienta {klient} w teatrze {teatr}")
    else:
        print("Nie znaleziono klienta lub teatru o podanej nazwie.")

def update_pracownicy(teatr, stary_pracownik, nowy_pracownik):
    if teatr in pracownicy and stary_pracownik in pracownicy[teatr]:
        pracownicy[teatr] = [nowy_pracownik if p == stary_pracownik else p for p in pracownicy[teatr]]
        print(f"Zaktualizowano pracownika {stary_pracownik} na {nowy_pracownik} w teatrze {teatr}")
    else:
        print("Nie znaleziono pracownika lub teatru o podanej nazwie.")

# Funkcja remove
def remove_teatry(nazwa):
    global teatry
    for teatr in teatry:
        if teatr['nazwa'] == nazwa:
            teatry.remove(teatr)
            print(f"Usunięto teatr {nazwa}")
            return
    print(f"Nie znaleziono teatru o nazwie {nazwa}")

def remove_klienci(teatr, klient):
    if teatr in klienci and klient in klienci[teatr]:
        klienci[teatr].remove(klient)
        print(f"Usunięto klienta {klient} z teatru {teatr}")
    else:
        print(f"Nie znaleziono klienta {klient} lub teatru {teatr} o podanej nazwie.")

def remove_pracownicy(teatr, pracownik):
    if teatr in pracownicy and pracownik in pracownicy[teatr]:
        pracownicy[teatr].remove(pracownik)
        print(f"Usunięto pracownika {pracownik} z teatru {teatr}")
    else:
        if teatr not in pracownicy:
            print(f"Nie znaleziono teatru o nazwie {teatr}.")
        else:
            print(f"Nie znaleziono pracownika {pracownik} w teatrze {teatr}.")

def remove_współrzędne(nazwa):
    global teatry
    teatry = [teatr for teatr in teatry if teatr['nazwa'] != nazwa]
    print(f"Usunięto współrzędne teatru {nazwa}")

# Funkcje do generowania map
def generuj_mape_teatrow(teatry):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    for teatr in teatry:
        nazwa = teatr['nazwa']
        adres = teatr['adres']
        wspolrzedne = teatr['współrzędne']
        lat, lon = map(float, wspolrzedne.split(', '))
        folium.Marker(
            location=[lat, lon],
            popup=f"{nazwa}<br>{adres}",
            tooltip=nazwa
        ).add_to(m)
    nazwa_pliku = 'mapa_teatrow.html'
    m.save(nazwa_pliku)
    print(f"Mapa została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)

def generuj_mape_pracownikow(pracownicy):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    for teatr, pracownicy_list in pracownicy.items():
        for pracownik in pracownicy_list:
            teatr_info = next((t for t in teatry if t['nazwa'] == teatr), None)
            if teatr_info:
                lat, lon = map(float, teatr_info['współrzędne'].split(', '))
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{pracownik} ({teatr})",
                    tooltip=pracownik
                ).add_to(m)
    nazwa_pliku = 'mapa_pracownikow.html'
    m.save(nazwa_pliku)
    print(f"Mapa pracowników została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)

def generuj_mape_klientow(klienci):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    for teatr, klienci_list in klienci.items():
        for klient in klienci_list:
            teatr_info = next((t for t in teatry if t['nazwa'] == teatr), None)
            if teatr_info:
                lat, lon = map(float, teatr_info['współrzędne'].split(', '))
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{klient} ({teatr})",
                    tooltip=klient
                ).add_to(m)
    nazwa_pliku = 'mapa_klientow.html'
    m.save(nazwa_pliku)
    print(f"Mapa klientów została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)

def generuj_mape_wszystkie(teatry, pracownicy, klienci):
    m = folium.Map(location=[52.235, 21.015], zoom_start=13)
    for teatr in teatry:
        nazwa = teatr['nazwa']
        adres = teatr['adres']
        wspolrzedne = teatr['współrzędne']
        lat, lon = map(float, wspolrzedne.split(', '))
        folium.Marker(
            location=[lat, lon],
            popup=f"{nazwa}<br>{adres}",
            tooltip=nazwa
        ).add_to(m)
    for teatr, pracownicy_list in pracownicy.items():
        for pracownik in pracownicy_list:
            teatr_info = next((t for t in teatry if t['nazwa'] == teatr), None)
            if teatr_info:
                lat, lon = map(float, teatr_info['współrzędne'].split(', '))
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{pracownik} ({teatr})",
                    tooltip=pracownik
                ).add_to(m)
    for teatr, klienci_list in klienci.items():
        for klient in klienci_list:
            teatr_info = next((t for t in teatry if t['nazwa'] == teatr), None)
            if teatr_info:
                lat, lon = map(float, teatr_info['współrzędne'].split(', '))
                folium.Marker(
                    location=[lat, lon],
                    popup=f"{klient} ({teatr})",
                    tooltip=klient
                ).add_to(m)
    nazwa_pliku = 'mapa_wszystkie.html'
    m.save(nazwa_pliku)
    print(f"Mapa dla wszystkich została wygenerowana i zapisana jako '{nazwa_pliku}'.")
    webbrowser.open(nazwa_pliku)

# Wywołanie funkcji generujących mapy dla sprawdzenia
generuj_mape_teatrow(teatry)
generuj_mape_pracownikow(pracownicy)
generuj_mape_klientow(klienci)
generuj_mape_wszystkie(teatry, pracownicy, klienci)