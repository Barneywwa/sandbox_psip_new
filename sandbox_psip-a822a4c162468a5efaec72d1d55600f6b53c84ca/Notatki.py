import psycopg2 as ps
from dane import users_list

db_params = ps.connect(
    database='postgres',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432
)

cursor=db_params.cursor()

# engine=sqlalchemy.create_engine(db_params)
# connection=engine.connect()

def dodaj_uzytkownika(user:str):
    for nick in users_list:
        if user == nick['nick']:
            sql_query_1 = f"INSERT INTO public.laboratoria(nick, name, city, posts) VALUES('{nick['nick']}','{nick['name']}','{nick['city']}','{nick['posts']}');"
            cursor.execute(sql_query_1)
            db_params.commit()

dodaj_uzytkownika(input('dodaj uzytkownikow'))

#def usun_uzytkownika(user:str):
#    sql_query_1 = sqlalchemy.text(f"delete from public.my_table where name='{user}';")
#    cursor.execute(sql_query_1)
#    cursor.commit
#
#def aktualizuj_uzytkownika(user_1:str,user_2:str):
#    sql_query_1 = sqlalchemy.text(f"update public.my_table set name='{user_1}'where name='{user_2}';")
#    connection.execute(sql_query_1)
#    connection.commit()
#aktualizuj_uzytkownika(
#    user_1=input('na kogo zamienic'),
#    user_2=input('kogo zamienic')
#)