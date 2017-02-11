import xlwt, xlrd
import urllib
import csv
import sqlite3
from yahoo_finance import Share
from datetime import datetime

def run():
	stocksCSV = r'/home/dan/Documents/stocksyms.csv'
	with open(stocksCSV, newline='') as csvfile:
		reader = csv.reader(csvfile, skipinitialspace=True)
		four500 = list(reader)
	
	now=datetime.now()
	database = sqlite3.connect(r'/home/dan/Documents/database.db')
	data=database.cursor()
	for stock in four500:

		s=Share(stock)
		print("\n" + str(stock) + "\n")
		print("price: "+s.get_price())
		print("change: "+str(s.get_change()))
		print("volume: "+s.get_volume())
		print("prev close: "+str(s.get_prev_close()))
		print("open: "+str(s.get_open()))
		print("avg daily volume: "+str(s.get_avg_daily_volume()))
		print("market cap: "+str(s.get_market_cap()))
		print("book value: "+str(s.get_book_value()))
		print("ebitda: "+str(s.get_ebitda()))
		print("dividend share: "+str(s.get_dividend_share()))
		print("dividend yield: "+str(s.get_dividend_yield()))
		print("earnings share: "+str(s.get_earnings_share()))
		print("days high: "+str(s.get_days_high()))
		print("days low: "+str(s.get_days_low()))
		print("year high: "+str(s.get_year_high()))
		print("year low: "+str(s.get_year_low()))
		print("50day moving avg: "+str(s.get_50day_moving_avg()))
		print("200day moving avg: "+str(s.get_200day_moving_avg()))
		print("price earnings ratio: "+str(s.get_price_earnings_ratio()))
		print("price earnings growth ratio: "+str(s.get_price_earnings_growth_ratio()))
		print("price sales: "+str(s.get_price_sales()))
		print("price book: "+str(s.get_price_book()))
		print("short ratio: "+str(s.get_short_ratio()))

		data.execute("INSERT INTO stocks VALUES(?, ?, ?, ?, ?,   ?, ?, ?, ?, ?,   ?, ?, ?, ?, ?,   ?, ?, ?, ?, ?,   ?, ?, ?, ?, ?)", (str(now), str(stock), s.get_price(), str(s.get_change()), s.get_volume(), s.get_prev_close(), str(s.get_open()), str(s.get_avg_daily_volume()), str(s.get_market_cap()), str(s.get_book_value()), str(s.get_ebitda()), str(s.get_dividend_share()), str(s.get_dividend_yield()), str(s.get_earnings_share()), str(s.get_days_high()), str(s.get_days_low()), str(s.get_year_high()), str(s.get_year_low()), str(s.get_50day_moving_avg()), str(s.get_200day_moving_avg()), str(s.get_price_earnings_ratio()), str(s.get_price_earnings_growth_ratio()), str(s.get_price_sales()), str(s.get_price_book()), str(s.get_short_ratio())))

	database.commit()
	data.close()
	print("success")

def sql(select,where,like):
	database = sqlite3.connect(r'/home/dan/Documents/database.db')
	data=database.cursor()
	ret=data.execute('select {} from stocks where {} like {} '.format(select,where,like))
	ret2=[]
	app=ret2.append
	for each in ret:
		app(each)
	data.close()
	return ret2

def select_col(col):
	database = sqlite3.connect(r'/home/dan/Documents/database.db')
	data=database.cursor()
	ret=data.execute('select {} from stocks'.format(col))
	ret2=[]
	app=ret2.append
	for each in ret:
		app(each)
	data.close()
	return ret2

def neural():
	dates=sql('date','symbol',"'__mmm__'")
	print(dates)

def writetoCSV():
	database = sqlite3.connect(r'/home/dan/Documents/database.db')
	data=database.cursor()
	rows=[]
	for row in data.execute('select * from stocks where date like "__________"'):
		rows.append(row)
	with open('all10.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(rows)
	data.close()

def update():
	database = sqlite3.connect(r'/home/dan/Documents/database.db')
	data=database.cursor()
	data.execute('update stocks set date="2016-12-27" where date="2016-12-23 23:07:04.350565"')
	database.commit()
	data.close()

if __name__ == "__main__":
	method=input("Enter method to run: ")
	if(method=="run"):
		run()
	if(method=="sql"):
		select=input("select: ")
		where=input("where: ")
		like=input("like: ")
		ret=sql(select,where,like)
		print(ret)
	if(method=="neural"):
		neural()
	if(method=="write"):
		writetoCSV()
	if(method=="update"):
		update()
