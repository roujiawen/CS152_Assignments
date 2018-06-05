# The code here will ask the user for input based on the askables
# It will check if the answer is known first


from pyswip.prolog import Prolog
from pyswip.easy import *
import sys
import os.path

prolog = Prolog() # Global handle to interpreter

retractall = Functor("retractall")
known = Functor("known",3)



#Reference: https://stackoverflow.com/questions/38951047/anyone-successfully-bundled-data-files-into-a-single-file-with-pyinstaller
if hasattr(sys, "_MEIPASS"):
    datadir = os.path.join(sys._MEIPASS, "KB.pl")
else:
    datadir = "KB.pl"

prolog.consult(datadir) # open the KB


def search(query):
    call(retractall(known))

    prolog.asserta("known(yes, take_out, " + query["take_out"][0] + ")")
    prolog.asserta("known(yes, open_late, " + query["open_late"][0] + ")")
    prolog.asserta("known(yes, english, " + query["english"][0] + ")")
    prolog.asserta("known(yes, distance, " + str(query["distance"]) + ")")
    for price in query["price"]:
        prolog.asserta("known(yes, price, \"" + price + "\")")
    for diet in query["diet"]:
        prolog.asserta("known(yes, diet, \"" + diet.lower() + "\")")
    for ftype in query["food_type"]:
        prolog.asserta("known(yes, type, \"" + ftype.lower() + "\")")

    return set([soln['X'] for soln in prolog.query("suggestion(X).", maxresult=100)])

#print(search({'take_out': ['no'], 'distance': 5.5, 'open_late': ['yes'], 'price': ['_1', '_2'], 'diet': ['vegan'], 'english': ['no'], 'food_type': ['korean','italian','chinese','southeast asian']}))
