#	Main.py
#	Author:	Max Behren

import sys
import db_editing
import mysql_info
from yahoo_finance import Share
import MySQLdb
import MySQLdb.cursors

def main():
	intro()

	quit = False
	while not quit:
		print "Below are the active deals:\n"
		print "Target\tAcquirer"

		returnall = "select * from universe ORDER BY target;"
		db = MySQLdb.connect(mysql_info.login["host"],mysql_info.login["user"],mysql_info.login["password"],mysql_info.login["db"])
		cur = db.cursor()
		rows = cur.execute(returnall)
		universe = cur.fetchall()
		if rows == 0:
			print ("No deals in universe")
		else:
			for row in universe:
				print row[0] + "\t" + row[1]

		input = (raw_input ("\nEnter the ticker symbol of a target for more info on that deal, "
			"enter \"Edit\" to edit the database, or enter \"Quit\" to stop the program:\n")).lower()

		if input == "quit":
			quit = True
		elif input == "edit":
			edit_in = False
			while not edit_in:
				edit_input = (raw_input("EDIT: Enter \"Add\" to add a deal, \"Delete\" to delete a deal, "
					"or \"Back\" to go back:\n")).lower()
				if edit_input == "back":
					edit_in = True
				elif edit_input == "add":
					db_editing.add_deal()
					edit_in = True
				elif edit_input == "delete":
					db_editing.delete_deal()
					edit_in = True
				else:
					print "Please enter a valid input."

		else:
			search = "Select * from universe where target = \"" + input + "\";"
			intable = cur.execute(search)
			if intable > 0:
				tgt = cur.fetchone()
				deal_info(tgt)
			else:
				print "Please enter a valid input.\n"

	outro()


def intro():
	print "\nWelcome to MergerArb Calculator written by Max Behren."
	print "This program was created using python and SQL. It allows the user to view and modify a database of " +\
		"M&A transactions and monitor live deal spreads.\n"

def outro():
	print "Thank you for running MergerArb Calculator.\n"

def deal_info(deal):
	print "DISPLAY DEAL INFO FOR: " + deal[0]

	consid = 0
	if deal[3] == '1':
		consid = deal[4]
		print deal[0] + " is being acquired by " + deal[1] + " for $" + str(consid) + " per share."
	else:
		ashare = Share(deal[1])
		acprice = float(ashare.get_price())
		stocknum = float(deal[5])
		stockval = acprice * stocknum
		acprice = "{:.2f}".format(float(acprice))
		if deal[3] == '2':
			consid = "{:.2f}".format(float(stockval))
			print deal[0] + " is being acquired by " + deal[1] + " for $" + str(consid) + " per share (" + \
				str(stocknum) + " shares of " + deal[1] + ", currently trading at $" + str(acprice) + ")."
		elif deal[3] == '3':
			cash = float(deal[4])
			consid = cash + stockval
			cash = "{:.2f}".format(float(cash))
			consid = "{:.2f}".format(float(consid))
			print deal[0] + " is being acquired by " + deal[1] + " for a consideration of $" + str(consid) + " per share ($" + \
				cash + " plus " + str(stocknum) + " shares of " + deal[1] + ", trading at $" + str(acprice) + ")."
		else:
			print "ERROR!"

	tshare = Share(deal[0])
	tprice = float(tshare.get_price())
	spread = float(consid) - tprice
	spreadpercent = "{:.2f}".format(float(spread / tprice)*100)
	spread = "{:.2f}".format(spread)
	print deal[0] + " last traded at $" + str(tprice) + ", a spread of $" + str(spread) + " to the deal consideration (" + spreadpercent + "%).\n"


if __name__ == '__main__':
	main()
