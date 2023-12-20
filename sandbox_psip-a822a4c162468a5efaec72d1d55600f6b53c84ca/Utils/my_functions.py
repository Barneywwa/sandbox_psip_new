import requests
from bs4 import BeautifulSoup
import folium
import psycopg2 as ps

db_params = ps.connect(
    database='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432
)

cursor = db_params.cursor()


def add_user_to() -> None:
    nick = input('Podaj nick:')
    name = input('Podaj imie:')
    city = input('Podaj miasto:')
    posts = int(input('Podaj liczbę postów:'))
    sql_query_1 = f"INSERT INTO public.laboratoria(nick, name, city, posts) VALUES('{name}', '{nick}', '{city}', '{posts}');"
    cursor.execute(sql_query_1)
    db_params.commit()


def remove_user_from() -> None:
    name = input('Podaj użytkownika do usunięcia: ')
    sql_query_1 = f"SELECT * FROM public.laboratoria WHERE name='{name}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    print(f'znaleziono uzytkownikow: ')
    print('0: usun wszystkich odnelazionych uzytkownikow')
    for numerek, user_to_be_removed in enumerate(query_result):
        print(f'{numerek + 1}: {user_to_be_removed}')
    numer = int(input(f'Wybierz numer użytkownika do usunięcia: '))
    if numer == 0:
        sql_query_2 = f"DELETE * FROM public.laboratoria;"
        cursor.execute(sql_query_2)
        db_params.commit()
    else:
        sql_query_2 = f"DELETE FROM public.laboratoria WHERE id='{query_result[numer - 1][0]}';"
        cursor.execute(sql_query_2)
        db_params.commit()


def show_users() -> None:
    sql_query_1 = f"SELECT * FROM public.laboratoria"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for row in query_result:
        print(f'Twój znajomy {row[2]} dodał {row[4]} postów!!!')


def update_user() -> None:
    nick_of_user = input('podaj nick użytkownika do modyfikacji')
    sql_query_1 = f"SELECT * FROM public.laboratoria WHERE nick='{nick_of_user}';"
    cursor.execute(sql_query_1)
    print('Znaleziono!!!')
    name = input('podaj nowe imie uzytkownika: ')
    nick = input('podaj nową ksywę uzytkownika: ')
    city = input('podaj nowe miasto uzytkownika: ')
    posts = int(input('podaj nową liczbę postów uzytkownika: '))
    sql_query_2 = f"UPDATE public.laboratoria SET name='{name}', nick='{nick}', city='{city}', posts='{posts}';"
    cursor.execute(sql_query_2)
    db_params.commit()


########################### MAPA ###########################

def get_coordinates_of(city: str) -> list[float, float]:
    adres_URL = f'https://pl.wikipedia.org/wiki/{city}'

    response = requests.get(url=adres_URL)
    response_html = BeautifulSoup(response.text, 'html.parser')

    # POBRANIE WSPÓŁRZĘDNYCH Z TREŚCI STRONY INTERNETOWEJ

    res_html_latitude = response_html.select('.latitude')[1].text

    # ŁOPATOLOGICZNIE MOŻNA ZROBIĆ TAK: print(res_html_latitude[23:-7])

    res_html_latitude = float(res_html_latitude.replace(',', '.'))

    # DRUGA WSPÓŁRZĘDNA

    res_html_longitude = response_html.select('.longitude')[1].text
    res_html_longitude = float(res_html_longitude.replace(',', '.'))

    return [res_html_latitude, res_html_longitude]

# for item in nazwy_miejscowosci:
# print(get_coordinates_of(aa))


# Zwrócić mapę z pinezką odnoszącą się do wskazanego użytkownika podanego z klawiatury
def get_map_of_user() -> None:
    city = input('Podaj nazwe miasta uzytkownika: ')
    sql_query_1 = f"SELECT * FROM public.laboratoria WHERE city ='{city}';"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    city = get_coordinates_of(city)
    map = folium.Map(location=city,
                     tiles='OpenStreetMap',
                     zoom_start=14
                     )
    for user in query_result:
        folium.Marker(location=city,
                      popup=f'Tu rządzi {user[2]} z GEOINFORMATYKI 2023\n OU YEEEEAAAAHHHH🚀'
                      ).add_to(map)
        map.save(f'mapka_{user[1]}.html')


# Zwrócić mapę z wszystkimi użytkownikami z danej listy (znajomymi)

###RYSOWANIE MAPY
def get_map_of() -> None:
    map = folium.Map(location=[52.3, 21.0],
                     tiles="OpenStreetMap",
                     zoom_start=7
                     )
    sql_query_1 = f"SELECT * FROM public.laboratoria;"
    cursor.execute(sql_query_1)
    query_result = cursor.fetchall()
    for user in query_result:
        folium.Marker(location=get_coordinates_of(city=user[3]),
                      popup=f'Użytkownik {user[2]} \n'
                            f'liczba postów {user[4]}'
                      ).add_to(map)
    map.save('mapka.html')


############################## END OF MAP ELEMENT ##############################

def gui() -> None:
    while True:
        print(f'MENU: \n'
              f'0: Zakończ program \n'
              f'1: Wyświetl użytkowników  \n'
              f'2: Dodaj użytkownika \n'
              f'3: Usuń użytkownika \n'
              f'4: Modyfikuj użytkownika \n'
              f'5: Wygeneruj mapę z użytkownikiem \n'
              f'6: Wygeneruj mapę ze wszystkimi użytkownikami \n'
              )

        menu_option = input('Podaj funkcję do wywołania')
        print(f'Wybrano funkcję {menu_option}')

        match menu_option:
            case '0':
                print('Kończę pracę')
                break
            case '1':
                print('Lista Użytkowników: ')
                show_users()
            case '2':
                print('Dodaj użytkownika: ')
                add_user_to()
            case '3':
                print('Usuń użytkownika: ')
                remove_user_from()
            case '4':
                print('Modyfikuję użytkownika')
                update_user()
            case '5':
                print('Rysuję mapę z użytkownikiem')
                get_map_of_user()
            case '6':
                print('Rysuję mapę ze wszystkimi użytkownikami')
                get_map_of()


def pogoda_z(miasto:str):
    URL = f'https://danepubliczne.ingw.pl/api/data/synop/station/{miasto}'
    return requests.get(URL).json()

class User:
    def __init__(self, name , nick, city, posts):
        self.name = name
        self.nick = nick
        self.city = city
        self.posts = posts
    def pogoda_z(self, miasto:str):
        URL = f'https://danepubliczne.ingw.pl/api/data/synop/station/{miasto}'
        return requests.get(URL).json()

npc_1 = User(name = 'Bartosz', nick = 'Baran', city = 'opoczno', posts = '997')
npc_2 = User(name = 'Mateusz', nick = 'Swietlik', city = 'lublin', posts = '112')

print(npc_1.city)
print(npc_2.city)

print(npc_1.pogoda_z(npc_1.city))
print(npc_2.pogoda_z(npc_1.city))
