import datetime
import queries
import math
import probeMethods
import MySQLdb
from decimal import Decimal


try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating", use_unicode=True, charset='utf8', )
    conn.autocommit(True)
    cursor = conn.cursor()

except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)


class Month(object):
    prevMonth = 0

def updateBaseRating():
    cursor.execute(queries.q23)
    conn.commit()
    print "updateBaseRating"


def getMonth():
    month = datetime.datetime.now().month
    cursor.execute(queries.q24)
    prevMonth = cursor.fetchone()[0]
    if month != prevMonth:
        cursor.execute(queries.q26 % [month])
        conn.commit()
        updateBaseRating()
    return 0
    
    
def check(match_id):
    cursor.execute("SELECT COUNT(points) FROM Player_match WHERE match_id = (SELECT id FROM Matches WHERE match_id = %s", [match_id])
    count = cursor.fetchone()[0]
    if(count != 0):
        resetDisplayRating(match_id)

def resetDisplayRating(match_id):
    cursor.execute("SELECT points, player_id FROM Player_match WHERE match_id=(SELECT id FROM Matches WHERE match_id = %s", [match_id]) #MATCH_ID
    pointsExist = cursor.fetchall()
    for row in pointsExist:
        player_id = Decimal(row[1])
        points = Decimal(row[0])
        if(points != null):
            cursor.execute("SELECT display_rating FROM Player WHERE id = %s", [player_id])
            display_rating = Decimal(cursor.fetchone()[0])
            newDisplay_rating = display_rating - points
            print Display_rating
            cursor.execute("UPDATE Player SET display_rating = %s WHERE id = %s", [newDisplay_rating, player_id])
            conn.commit()
        
def setDisplayRating(match_id):
    cursor.execute("SELECT pm.points, p.id FROM Player_match pm, Player p WHERE match_id=(SELECT id FROM Matches WHERE match_id = %s) AND pm.player_id=p.id", [match_id])
    data = cursor.fetchall()
    for row in data:
        points = float(row[0])
        player_id = float(row[1])
        cursor.execute("SELECT display_rating FROM Player WHERE id = %s", [player_id])
        display_rating = float(cursor.fetchone()[0])
        newDisplay_rating = display_rating + points
        cursor.execute("UPDATE Player SET display_rating = %s WHERE id = %s", [newDisplay_rating, player_id])
        conn.commit()
        
def calculate(match_id):
    getMonth()
    print "match_id i kalkis: ", match_id
    cursor.execute(queries.findAVG3, [match_id, match_id]) #finds losing team's average score
    B = float(cursor.fetchone()[0])
    cursor.execute(queries.findAVG4, [match_id, match_id]) #finds winning team's average score
    A = float(cursor.fetchone()[0])
    #Elo-rating formula
    Es = 1.0 / (1.0 + math.pow(10.0, ((B-A) / 400.0)))
    print "Es: ", Es 
    R = round(Decimal(15 * (1-Es)), 2) #winning team points
    print "R: ", R
    cursor.execute(queries.findID1, [match_id, match_id]) #finds every participating player on winning team
    ID = cursor.fetchall()
    for row in ID: #for each player -> update points
        id = row[0]
        print "for each player -> update points", id
        cursor.execute(queries.updatePoints, [R, match_id, id])
        conn.commit()
    R = -R #losing team points
    cursor.execute(queries.findID2, [match_id, match_id]) #finds every participating player on winning team
    ID = cursor.fetchall()
    for row in ID: #for each player -> update points
        id = row[0]
        print "for each player -> update points", id
        cursor.execute(queries.updatePoints, [R, match_id, id])
        conn.commit()
    setDisplayRating(match_id) #run this method