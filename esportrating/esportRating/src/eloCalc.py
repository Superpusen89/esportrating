# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import esportrating.py

try:
    conn = MySQLdb.connect(host="localhost", user="root", passwd="HenrietteIda", db="esportrating")
    cursor = conn.cursor()
    
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

listen = true
number_of_matches = cursor.execute("SELECT COUNT(*) FROM PY_trigger")
while listen:
    number_of_matches_2 = cursor.execute("SELECT COUNT(*) FROM PY_trigger")
    if(number_of_matches!=number_of_matches_2):
        print number_of_matches
        print number_of_matches_2
        number_of_matches = number_of_matches_2