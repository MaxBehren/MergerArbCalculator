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
		#db = MySQLdb.connect("localhost","root","","mergerarb" )
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


	# target = raw_input("Enter the target ticker: ")
	# acquirer = raw_input("Enter the acquirer ticker: ")
	# tshare = Share(target)
	# ashare = Share(acquirer)
	# print tshare.get_name() + " last trade: " + tshare.get_price()
	# print ashare.get_name() + " last trade: " + ashare.get_price()

def intro():
	print "\nWelcome to MergerAarb Calculator written by Max Behren\n"

def outro():
	print "Thank you for running MergerArb Calculator\n"

def deal_info(deal):
	print "DISPLAY DEAL INFO FOR: " + deal[0]


	#FIXME: implement


if __name__ == '__main__':
	main()