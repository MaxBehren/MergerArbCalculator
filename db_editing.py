#	db_editing.py
#	Author: Max Behren


from yahoo_finance import Share
import mysql_info
import MySQLdb
import MySQLdb.cursors

def add_deal():
	print "ADDING DEAL"
	tar_in = False
	while not tar_in:
		target = raw_input("Enter the target ticker: ")
		if not target.isalpha():
			print "Please enter only letters"
		else:
			tshare = Share(target)
			if tshare.get_price():
				tar_in = True
				target = target.upper()
			else:
				print "Please enter a valid ticker symbol"


	pub_in = False

	while not pub_in:
		pubres = str(raw_input("Is the acquirer public (Y/N): ")).lower()
		if pubres == 'y':
			pub = 1
			pub_in = True
		elif pubres == 'n':
			pub = 0
			pub_in = True
		else:
			print "Please answer with 'Y' or 'N'"

	ac_in = False
	while not ac_in:
		if pub:
			acquirer = raw_input("Enter the acquirer ticker: ")
			if not acquirer.isalpha():
				print "Please enter only letters"
			else:
				ashare = Share(acquirer)
				if ashare.get_price():
					ac_in = True
					acquirer = acquirer.upper()
				else:
					print "Please enter a valid ticker symbol"
		else:
			acquirer = raw_input("Enter the acquirer name: ")
			if acquirer:
				ac_in = True

	consid = 1 #1 cash, 2 stock, 3 cash and stock
	if pub:
		valconsid = False
		while not valconsid:
			consid_in = raw_input("Is the consideration cash(1), stock(2) or cash and stock(3)? (Enter 1, 2, or 3): ")
			try:
				consid_in = int(consid_in)
				if consid_in == 1:
					consid = 1
					valconsid = True
				elif consid_in == 2:
					consid = 2
					valconsid = True
				elif consid_in == 3:
					consid = 3
					valconsid = True
				else:
					print "Please enter 1, 2, or 3"
			except ValueError:
				print "Please enter 1, 2, or 3"
	cash = 0
	if consid == 1 or consid == 3:
		cash_in = False
		while not cash_in:
			cash = raw_input ("Please enter the cash consideration: $")
			try:
				cash = "{:.2f}".format(float(cash))
				print "Cash is: $" + cash
				cash_in = True
			except ValueError:
				print "Please enter a valid dollar amount"
	stock = 0
	if consid == 2 or consid == 3:
		stock_in = False
		while  not stock_in:
			stock = raw_input ("Please enter the stock consideration (up to 4 decimals): ")
			try:
				stock = "{:.4f}".format(float(stock))
				print "Stock is: " + stock
				stock_in = True
			except ValueError:
				print "Please enter a valid stock amount"

	# print "Target:\t" + target
	# print "Acquirer:\t" + acquirer
	# print "pub:\t" + str(pub)
	# print "type:\t" + str(consid)
	# print "cash:\t" + str(cash)
	# print "stock:\t" + str(stock)

	query = "INSERT INTO universe (Target, Acquirer, Acq_public, Type, Cash, Stock) VALUES (\"" + target + "\",\"" + acquirer + "\"," + \
		str(pub) + "," + str(consid) + "," + str(cash) + "," + str(stock) +");"
	# print(query)

	db = MySQLdb.connect(mysql_info.login["host"],mysql_info.login["user"],mysql_info.login["password"],mysql_info.login["db"])
	cur = db.cursor()
	cur.execute(query)
	db.commit()
	print target.upper() + " deal entered\n"


def delete_deal():
	remain = True
	while remain:
		input = (raw_input ("DELETE: Enter the ticker symbol of the target of the deal you would like to delete, "
			"or enter \"Back\" to go back:\n")).lower()
		if input == "back":
			return
		else:
			query = "DELETE from universe where Target = \"" + input + "\";"
			db = MySQLdb.connect(mysql_info.login["host"],mysql_info.login["user"],mysql_info.login["password"],mysql_info.login["db"])
			cur = db.cursor()
			sucess = cur.execute(query)
			if sucess > 0:
				print input.upper() + " deal sucessfully deleted from universe.\n"
				db.commit()
				remain = False
			else:
				print "Please enter a valid input."








