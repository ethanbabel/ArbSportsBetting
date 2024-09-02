import mysql.connector
import parse_odds
import datetime
from dotenv import load_dotenv
import os
import pandas as pd

def get_connection():
    load_dotenv()
    mydb = mysql.connector.connect(
        host = os.getenv('DATABASE_HOST'),
        user = os.getenv('DATABASE_USER'),
        passwd = os.getenv('DATABASE_PASSWORD'),
        database = "ArbSportsBetting"
    )
    return mydb



def clear_tables():
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            cursor.execute("SET foreign_key_checks = 0")
            tables = ['Events', 'team1odds', 'team2odds', 'Arbs']
            for table in tables:
                cursor.execute(f'DELETE FROM {table}')
            cursor.execute("SET foreign_key_checks = 1") 
            mydb.commit()

def check_exists(team1: bool, eventID: str, line: float) -> bool:
    with get_connection() as mydb:
        with mydb.cursor() as cursor: 
            if(team1):
                cursor.execute('SELECT * FROM team1odds WHERE eventID = %s AND spread = %s', (eventID, line))
                return len(cursor.fetchall())>0
            else:
                cursor.execute('SELECT * FROM team2odds WHERE eventID = %s AND spread = %s', (eventID, line))
                return len(cursor.fetchall())>0

def update_data():
    with get_connection() as mydb:
        with mydb.cursor() as cursor:  
            for sport in parse_odds.get_in_season_sports():
                for event in parse_odds.get_event_ids(sport):
                    id = event['id']
                    team1 = event['team1']
                    team2 = event['team2']
                    dt = event['dt']
                    cursor.execute("INSERT INTO Events(id, sport, team1, team2, dt) VALUES(%s, %s, %s, %s, %s)", (id, sport, team1, team2, dt))
                    for odd in parse_odds.get_event_odds(sport, id):
                        sportsbook = odd['bookmaker']
                        price = odd['price']
                        line = float(odd['line'])
                        if (odd['team']==team1):
                            if check_exists(True, id, line):
                                cursor.execute(f"SELECT odds, books FROM team1odds WHERE eventID = '{id}' AND spread = {line}")
                                sql_response = cursor.fetchone()
                                odds = sql_response[0] + f'{price} '
                                books = sql_response[1] + f'{sportsbook} '
                                cursor.execute(f"UPDATE team1odds SET odds = '{odds}', books = '{books}'  WHERE eventID = '{id}' AND spread = {line}")
                            else:
                                price = str(price) + " "
                                sportsbook = sportsbook + " "
                                cursor.execute("INSERT INTO team1odds (eventID, team, spread, odds, books) VALUES (%s, %s, %s, %s, %s)", (id, team1, line, price, sportsbook))
                        else:
                            if check_exists(False, id, line):
                                cursor.execute(f"SELECT odds, books FROM team2odds WHERE eventID = '{id}' AND spread = {line}")
                                sql_response = cursor.fetchone()
                                odds = sql_response[0] + f'{price} '
                                books = sql_response[1] + f'{sportsbook} '
                                cursor.execute(f"UPDATE team2odds SET odds = '{odds}', books = '{books}'  WHERE eventID = '{id}' AND spread = {line}")
                            else:
                                price = str(price) + " "
                                sportsbook = sportsbook + " "
                                cursor.execute("INSERT INTO team2odds (eventID, team, spread, odds, books) VALUES (%s, %s, %s, %s, %s)", (id, team2, line, price, sportsbook))
            mydb.commit()

def update_arbitrage():
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            cursor.execute("SELECT Events.id, Events.sport, team1odds.spread, team1odds.odds, team1odds.books, team2odds.odds, team2odds.books \
                FROM team1odds INNER JOIN team2odds ON team1odds.spread = - team2odds.spread AND team1odds.eventID = team2odds.eventID \
                INNER JOIN Events ON team1odds.eventID = Events.id")
            for entry in cursor.fetchall():
                id = entry[0]
                sport = entry[1]
                line = entry[2]
                favorite_odds = list(entry[3][:-1].split(" "))
                favorite_books = list(entry[4][:-1].split(" "))
                underdog_odds = list(entry[5][:-1].split(" "))
                underdog_books = list(entry[6][:-1].split(" "))
                for i in range(len(favorite_odds)):
                    for j in range(len(underdog_odds)):
                        profit_percentage = 1 - ((1.0/float(favorite_odds[i])) + (1.0/float(underdog_odds[j])))
                        if (profit_percentage > 0):
                            cursor.execute("INSERT INTO Arbs (sport, eventID, spread, oddFavorite, bookFavorite, oddUnderdog, bookUnderdog, profitPercentage) \
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (sport, id, line, favorite_odds[i], favorite_books[i], \
                                underdog_odds[j], underdog_books[j], profit_percentage))
            mydb.commit()

def save_historical_arbitrage(profit_percentage: float):
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            dt = datetime.datetime.now()
            cursor.execute("INSERT INTO Historical (profitPercentage, dt) VALUES (%s, %s)", (profit_percentage*100, dt))
            mydb.commit()

def get_arbitrage_string() -> str:
    arbs = ''
    max_profit_percentage = 0
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            cursor.execute("SELECT * FROM Arbs")
            for arb in cursor:
                max_profit_percentage = max(max_profit_percentage, arb[8])
                if arb[8] > 0.005:
                    arbs = arbs + str(arb) + '\n'
            if(max_profit_percentage >= 0.005):
                save_historical_arbitrage(max_profit_percentage)
    return arbs

def get_arbitrage_list() -> list:
    arbs = []
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            cursor.execute("SELECT * FROM Arbs")
            arbing_info = cursor.fetchall()
            for arb in arbing_info:
                if arb[8] > 0.005:
                    cursor.execute(f"SELECT team1, team2 FROM Events WHERE id = '{arb[2]}'")
                    teams = cursor.fetchall()
                    arb = list(arb)
                    arb.append(teams[0][0])
                    arb.append(teams[0][1])
                    arbs.append(arb)
    return arbs

def get_historical_average() -> float:
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            cursor.execute("SELECT AVG(profitPercentage) FROM Historical")
            avg = cursor.fetchall()[0][0]
    return float(avg)

def update_all():
    try:
        print("Clearing Tables... (0/3) ")
        clear_tables()
        print("Tables Cleared. (1/3)")
        print("Updating Event & Spread Data... (1/3) ")
        update_data()
        print("Event & Spread Data Updated. (2/3) ")
        print("Updating Arbitrage Data... (2/3) ")
        update_arbitrage()
        print("Arbitrage Data Updated. (3/3) ")
        return True
    except TypeError:
        print("API Limit reached. ")
        return False

def ping():
    with get_connection() as mydb:
        with mydb.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchall()

