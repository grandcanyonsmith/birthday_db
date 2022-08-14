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
    cursor.execute("SHOW TABLES FROM " + database)
    return cursor.fetchall()


tables = ([x[0] for x in get_tables('auroradevdb')])
table = tables[0]

# connect to the database and table and print all columns
def get_all_data(table):
    cursor.execute("SELECT * FROM " + table)
    return cursor.fetchall()


# query what birthdays are on a given day, returns a list of names
def get_birthdays_on_day(day, table):
    cursor.execute("SELECT name FROM " + table + " WHERE DATE_FORMAT(birthday, '%m-%d') = DATE_FORMAT(" + day + ", '%m-%d')")  # noqa
    return [x[0] for x in cursor.fetchall()]


# print the birthdays that are on a given day
def print_birthdays_on_day(day, table):
    for name in get_birthdays_on_day(day, table):
        print(name)


# create a function that allows me to enter any name and query the database for the birthday. Have it ask me for the name and then query the database for the birthday.
def get_birthday(name):
    cursor.execute("SELECT birthday FROM " + table + " WHERE name LIKE '%" + name + "%'")  # noqa
    birthday = cursor.fetchall()
    # convert the birthday to a string
    if birthday == []:
        return 'That name is not in the database'
    else:
        birthday = str(birthday[0][0])
        # split the string into a list
        birthday = birthday.split('-')
        # convert the list to a string
        birthday = '-'.join(birthday)
        # convert that string to a datetime object
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        formatted_day = birthday.strftime('%B %d')
        return formatted_day


# print the birthday of people that are my cousins using the 'relation' column
def get_birthdays_based_on_relationship(relationship):
    cursor.execute("SELECT name, birthday FROM " + table + " WHERE relation LIKE '%" + relationship + "%'")  # noqa
    birthdays = cursor.fetchall()
    for i, (name, birthday) in enumerate(birthdays):
        birthday = str(birthday)
        birthday = birthday.split('-')
        birthday = '-'.join(birthday)
        if birthday != 'None' and birthday != '':
            birthday = datetime.strptime(birthday, '%Y-%m-%d')
            formatted_day = birthday.strftime('%B %d')
            birthdays[i] = (name, formatted_day)
    return [x for x in birthdays if x[1] not in ['None', '']]
# print the birthdays of people that are my cousins using the 'relation' column

def print_birthdays_based_on_relationship(relationship):

    for name, birthday in get_birthdays_based_on_relationship(relationship):

        print(name + ' ' + str(birthday))

def get_anniversary_dates_based_on_relationship(relationship):
    cursor.execute("SELECT name, anniversary FROM " + table + " WHERE relation LIKE '%" + relationship + "%'")  # noqa
    anniversary_dates = cursor.fetchall()
    for i, (name, anniversary_date) in enumerate(anniversary_dates):
        anniversary_date = str(anniversary_date)
        anniversary_date = anniversary_date.split('-')
        anniversary_date = '-'.join(anniversary_date)
        if anniversary_date != 'None' and anniversary_date != '':
            anniversary_date = datetime.strptime(anniversary_date, '%Y-%m-%d')
            formatted_day = anniversary_date.strftime('%B %d')
            anniversary_dates[i] = (name, formatted_day)
    return [x for x in anniversary_dates if x[1] not in ['None', '']]


def print_all_data(table):
    headers = ['Name', 'Birthday', 'Anniversary', 'Relationship']
    data = get_all_data(table)
    for i, (name, birthday, anniversary, relationship) in enumerate(data):
        # convert the birthday to a string
        if birthday is None or birthday == '':
            birthday = 'None'
        else:
            # split the string into a list
            birthday = str(birthday)
            birthday = birthday.split('-')
            # convert the list to a string
            birthday = '-'.join(birthday)
            # convert that string to a datetime object
            birthday = datetime.strptime(birthday, '%Y-%m-%d')
            formatted_day = birthday.strftime('%B %d')
            # data[i] = (name, formatted_day, anniversary, relationship)
        data[i] = (name, str(formatted_day), str(anniversary), relationship)
    table = AsciiTable(data, headers)
    return table.table


def format_date(date):
    date = str(date)
    date = date.split('-')
    date = '-'.join(date)
    date = datetime.strptime(date, '%Y-%m-%d')
    formatted_date = date.strftime('%B %d')

    return formatted_date


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

if __name__ == '__main__':
    print(print_all_data_colorful(table))
    print(get_anniversary_dates_based_on_relationship('uncle'))
    print(get_birthday('Doug'))
    print(get_birthdays_based_on_relationship('brother'))
    print(get_birthdays_based_on_relationship('sister'))

