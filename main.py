import mysql.connector
from mysql.connector import Error
from datetime import datetime
from terminaltables import AsciiTable
from colorama import init, Fore, Back, Style
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def connect():
    try:
        conn = mysql.connector.connect(host=os.getenv('HOST'),
                                       database=os.getenv('DATABASE'),
                                       user='admin',
                                       password=os.getenv('PASSWORD'))
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)

        return None
connect()
conn = connect()
cursor = conn.cursor()


def get_tables(database):
    cursor.execute(f"SHOW TABLES FROM {database}")
    return cursor.fetchall()


tables = ([x[0] for x in get_tables('auroradevdb')])
table = tables[0]

# connect to the database and table and print all columns
def get_all_data(table):
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()

def format_date(date):
    date = str(date)
    date = date.split('-')
    date = '-'.join(date)
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%B %d')


# query what birthdays are on a given day, returns a list of names
def get_birthdays_on_day(day, table):
    cursor.execute(
        f"SELECT name FROM {table}"
        + " WHERE DATE_FORMAT(birthday, '%m-%d') = DATE_FORMAT("
        + day
        + ", '%m-%d')"
    )

    return [x[0] for x in cursor.fetchall()]


# print the birthdays that are on a given day
def print_birthdays_on_day(day, table):
    for name in get_birthdays_on_day(day, table):
        print(name)


# create a function that allows me to enter any name and query the database for the birthday. Have it ask me for the name and then query the database for the birthday.
def get_birthday(name):
    cursor.execute(
        f"SELECT birthday FROM {table}" + " WHERE name LIKE '%" + name + "%'"
    )

    birthday = cursor.fetchall()
    if birthday == []:
        return 'That name is not in the database'
    birthday = str(birthday[0][0])
    return format_date(birthday)


# print the birthday of people that are my cousins using the 'relation' column
def get_birthdays_based_on_relationship(relationship):
    cursor.execute(
        f"SELECT name, birthday FROM {table}"
        + " WHERE relation LIKE '%"
        + relationship
        + "%'"
    )

    birthdays = cursor.fetchall()
    for i, (name, birthday) in enumerate(birthdays):
        birthday = str(birthday)
        birthday = birthday.split('-')
        birthday = '-'.join(birthday)
        if birthday not in ['None', '']:
            formatted_day = format_date(birthday)
            birthdays[i] = (name, formatted_day)
    return [x for x in birthdays if x[1] not in ['None', '']]


def get_anniversary_dates_based_on_relationship(relationship):
    cursor.execute(
        f"SELECT name, anniversary FROM {table}"
        + " WHERE relation LIKE '%"
        + relationship
        + "%'"
    )

    anniversary_dates = cursor.fetchall()
    for i, (name, anniversary_date) in enumerate(anniversary_dates):
        anniversary_date = str(anniversary_date)
        anniversary_date = anniversary_date.split('-')
        anniversary_date = '-'.join(anniversary_date)
        if anniversary_date not in ['None', '']:
            anniversary_date = format_date(anniversary_date)
            anniversary_dates[i] = (name, anniversary_date)
    return [x for x in anniversary_dates if x[1] not in ['None', '']]

def print_all_data_colorful(table):
    headers = ['Name', 'Birthday', 'Anniversary', 'Relationship']
    data = get_all_data(table)

    for i, (name, birthday, anniversary, relationship) in enumerate(data):
        # use the format_birthday function to convert the birthday to a string
        if birthday is None or birthday == '':
            birthday = 'None'
        else:
            birthday = format_date(birthday)

        if anniversary is None or anniversary == '':
            anniversary = 'None'
        else:
            anniversary = format_date(anniversary) 

        data[i] = (Fore.RED + name + Style.RESET_ALL, Fore.GREEN + str(birthday) + Style.RESET_ALL, Fore.BLUE + str(anniversary) + Style.RESET_ALL, Fore.YELLOW + relationship + Style.RESET_ALL)
    table = AsciiTable(data, headers)
    return table.table

def check_birthdays_today():
    cursor.execute(
        f"SELECT name, birthday FROM {table}"
        + " WHERE DATE_FORMAT(birthday, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d')"
    )

    birthdays = cursor.fetchall()
    for i, (name, birthday) in enumerate(birthdays):
        birthday = str(birthday)
        birthday = birthday.split('-')
        birthday = '-'.join(birthday)
        if birthday not in ['None', '']:
            formatted_day = format_date(birthday)
            birthdays[i] = (name, formatted_day)
    return [x for x in birthdays if x[1] not in ['None', '']]

def check_birthdays_this_week():
    cursor.execute(
        f"SELECT name, birthday FROM {table}"
        + " WHERE DATE_FORMAT(birthday, '%m-%d') BETWEEN DATE_FORMAT(CURDATE(), '%m-%d') AND DATE_FORMAT(CURDATE() + INTERVAL 7 DAY, '%m-%d')"
    )

    birthdays = cursor.fetchall()
    for i, (name, birthday) in enumerate(birthdays):
        birthday = str(birthday)
        birthday = birthday.split('-')
        birthday = '-'.join(birthday)
        if birthday not in ['None', '']:
            formatted_day = format_date(birthday)
            birthdays[i] = (name, formatted_day)
    return [x for x in birthdays if x[1] not in ['None', '']]

def check_birthdays_this_month():
    cursor.execute(
        f"SELECT name, birthday FROM {table}"
        + " WHERE DATE_FORMAT(birthday, '%m-%d') BETWEEN DATE_FORMAT(CURDATE(), '%m-%d') AND DATE_FORMAT(CURDATE() + INTERVAL 30 DAY, '%m-%d')"
    )

    birthdays = cursor.fetchall()
    for i, (name, birthday) in enumerate(birthdays):
        birthday = str(birthday)
        birthday = birthday.split('-')
        birthday = '-'.join(birthday)
        if birthday not in ['None', '']:
            formatted_day = format_date(birthday)
            birthdays[i] = (name, formatted_day)
    return [x for x in birthdays if x[1] not in ['None', '']]


def check_anniversaries_today():
    cursor.execute(
        f"SELECT name, anniversary FROM {table}"
        + " WHERE DATE_FORMAT(anniversary, '%m-%d') = DATE_FORMAT(CURDATE(), '%m-%d')"
    )

    anniversaries = cursor.fetchall()
    for i, (name, anniversary) in enumerate(anniversaries):
        anniversary = str(anniversary)
        anniversary = anniversary.split('-')
        anniversary = '-'.join(anniversary)
        if anniversary not in ['None', '']:
            formatted_day = format_date(anniversary)
            anniversaries[i] = (name, formatted_day)
    return [x for x in anniversaries if x[1] not in ['None', '']]

def check_anniversaries_this_week():
    cursor.execute(
        f"SELECT name, anniversary FROM {table}"
        + " WHERE DATE_FORMAT(anniversary, '%m-%d') BETWEEN DATE_FORMAT(CURDATE(), '%m-%d') AND DATE_FORMAT(CURDATE() + INTERVAL 7 DAY, '%m-%d')"
    )

    anniversaries = cursor.fetchall()
    for i, (name, anniversary) in enumerate(anniversaries):
        anniversary = str(anniversary)
        anniversary = anniversary.split('-')
        anniversary = '-'.join(anniversary)
        if anniversary not in ['None', '']:
            formatted_day = format_date(anniversary)
            anniversaries[i] = (name, formatted_day)
    return [x for x in anniversaries if x[1] not in ['None', '']]

def check_anniversaries_this_month():
    # check for anniversaries in the next 30 days
    cursor.execute(
        f"SELECT name, anniversary FROM {table}"
        + " WHERE DATE_FORMAT(anniversary, '%m-%d') BETWEEN DATE_FORMAT(CURDATE(), '%m-%d') AND DATE_FORMAT(CURDATE() + INTERVAL 30 DAY, '%m-%d')"
    )

    anniversaries = cursor.fetchall()
    for i, (name, anniversary) in enumerate(anniversaries):
        anniversary = str(anniversary)
        anniversary = anniversary.split('-')
        anniversary = '-'.join(anniversary)
        if anniversary not in ['None', '']:
            formatted_day = format_date(anniversary)
            anniversaries[i] = (name, formatted_day)
    return [x for x in anniversaries if x[1] not in ['None', '']]

if __name__ == '__main__':
    print(print_all_data_colorful(table))
    print(get_anniversary_dates_based_on_relationship('cousin'))
    print(get_birthday('Doug'))
    print(list(get_birthdays_based_on_relationship('brother')))
    print(list(get_birthdays_based_on_relationship('sister')))
    print("\n+Birthdays today: " + str(check_birthdays_today()))
    print("\n+Birthdays this week:", check_birthdays_this_week())
    print("\n+Birthdays this month:", check_birthdays_this_month())

    # print(check_anniversaries_today())
    print("\n+Anniversaries today:", check_anniversaries_today())
    print("\n+Anniversaries this week:", check_anniversaries_this_week())
    print("\n+Anniversaries this month:", check_anniversaries_this_month())

# TODO:
# - sort birthdays by soonest to latest
# - convert the table printer into a function that can be called from the main function for whatever table you want to print