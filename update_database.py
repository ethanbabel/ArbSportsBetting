import mysql.connector
import parse_odds
import datetime

mydb = mysql.connector.connect(
    host="arbsportsbettingdatabase.czcyyswyshyy.us-west-1.rds.amazonaws.com",
    user="admin",
    passwd="ArbSportsBettingsasha4",
    database="ArbSportsBetting"
)

cursor = mydb.cursor()

def clear_tables():
    tables = ['Events', 'OverDog', 'UnderDog']
    for table in tables:
        cursor.execute(f'DELETE FROM {table}')

def check_exists(positive: bool, eventID: str, line: float) -> bool:
    if(positive):
        cursor.execute('SELECT * FROM OverDog WHERE eventID = %s AND spread = %s', (eventID, line))
        return len(cursor.fetchall())>0
    else:
        cursor.execute('SELECT * FROM UnderDog WHERE eventID = %s AND spread = %s', (eventID, line))
        return len(cursor.fetchall())>0

def update():
    clear_tables()

    for sport in parse_odds.get_in_season_sports():
        for event in parse_odds.get_event_ids(sport):
            id = event['id']
            team1 = event['team1']
            team2 = event['team2']
            dt = event['dt']
            if id==None or team1==None or team2==None or dt==None or sport==None:
                print()
                print(f'ID; {id}, sport: {sport}, team1: {team1}, team2: {team2}, dt: {dt}')
                print()
            cursor.execute('INSERT INTO Events(id, sport, team1, team2, dt) VALUES(%s, %s, %s, %s, %s)', (id, sport, team1, team2, dt))
            for odd in parse_odds.get_event_odds(sport, id):
                sportsbook = odd['bookmaker']
                price = float(odd['price'])
                line = float(odd['line'])
                if (line>=0):
                    if check_exists(True, id, line):
                        cursor.execute(f"UPDATE OverDog SET {sportsbook} = {price} WHERE eventID = '{id}' AND spread = {line}")
                    else:
                        cursor.execute(f"INSERT INTO OverDog (eventID, spread, {sportsbook}) VALUES ('{id}', {line}, {price})")
                else:
                    if check_exists(True, id, line):
                        cursor.execute(f"UPDATE Underdog SET {sportsbook} = {price} WHERE eventID = '{id}' AND spread = {line}")
                    else:
                        cursor.execute(f"INSERT INTO UnderDog (eventID, spread, {sportsbook}) Values ('{id}', {line}, {price})")
    mydb.commit()

if __name__ == '__main__':
    # update()
    # cursor.execute("SELECT * FROM Events LIMIT 100")
    # print(cursor.fetchall())
    # print("\n \n")
    # cursor.execute("SELECT * FROM OverDog LIMIT 100")
    # print(cursor.fetchall())
    # print("\n \n")
    # cursor.execute("SELECT * FROM UnderDog LIMIT 100")
    # print(cursor.fetchall())
    pass
