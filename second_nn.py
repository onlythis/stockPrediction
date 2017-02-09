import csv
from stock import sql, select_col
from datetime import datetime, timedelta
from functools import reduce
import numpy
import neurolab as nl
import pylab
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.svm import SVR

COLUMNS = ["date", "symbol", "price", "change", "volume", "prev_close", "open", "avg_daily_volume", "market_cap","book_value", "ebitda", "dividend_share", "dividend_yield", "earnings_share", "days_high", "days_low", "year_high", "year_low", "fiftyday_moving_avg", "twohundredday_moving_avg", "price_earnings_ratio", "price_earnings_growth_ratio", "price_sales", "price_book", "short_ratio"]

symbols = sql('symbol','date',"'2016-12-21'")
VALUES = sql('*','symbol',"'__ebay__'")
symvals=[]

for each in range(len(symbols)):
	symbols[each]=str(symbols[each])
	symbols[each]=symbols[each][4:len(symbols[each])-5]

for each in range(len(symbols)):
	symvals.append(sql('*','symbol',"'__{}__'".format(symbols[each])))


class col_vals:
	def __init__(self):
		dates=select_col('date')
		str_dates = [str(s)[2:-3].split('-') for s in dates]
		#year, month, day passed to datetime
		days= [datetime(int(str_dates[x][0]),int(str_dates[x][1]),int(str_dates[x][2])) for x in range(len(str_dates))]
		#number of days after the first day, days are already in order
		self.days = [(days[x]-days[0]).days for x in range(len(days))]

		syms=select_col('symbol')
		self.syms = [str(s)[4:-5] for s in syms]
		print(len(self.syms))

		cols = [select_col(index) for index in COLUMNS]
		cols[0] = self.days
		cols[1] = self.syms
		#print average
		print(reduce(lambda x,y: x+y,cols[0]) / len(cols[0]))
		
		print(cols[1][1])
		print(len(cols[1]))
		#price to avg_daily_volume
		for x in range(2,8):
			cols[x] = [float(str(s)[1:-2]) if str(s)[1:-2]!="'None'" else 0 for s in cols[x]]
			print(COLUMNS[x])
			print(cols[x][1:5])
			print(reduce(lambda x,y: x+y,cols[x]) / len(cols[x]))

		print(COLUMNS[8])
		print(cols[1][23], cols[1][1033])
		print(cols[8][23], cols[8][1033])
		#some of the data is wrong(239735.72B)
		for x in range(len(cols[8])):
			mk=str(cols[8][x])
			if(mk[-4]=='B'):
				cols[8][x]=float(format(float(mk[2:-4])*10**3, '.0f'))
				if(cols[8][x]>10**6):
					cols[8][x]=cols[8][x]/(10**3)
			elif(mk[-4]=='M'):
				cols[8][x]=float(format(float(mk[2:-4]), '.2f'))
			else:
				cols[8][x]=0
		print("4")
		print(cols[8][23], cols[8][1033])
		print(cols[8][1:5])
		print(reduce(lambda x,y: float(x)+float(y),cols[8]) / len(cols[8]))
		print(max(cols[8]))

		cols[9] = [float(str(s)[1:-2]) if str(s)[1:-2]!="'None'" else 0 for s in cols[9]]

		print(COLUMNS[9])
		for x in range(len(cols[9])):
			if(cols[9][x]>250):
				cols[9][x]=0
		#1 symbol of false data
		[print(x) for x in cols[9] if x>250]		
		print(cols[9][1:5])
		print(reduce(lambda x,y: x+y,cols[9]) / len(cols[9]))
		print(max(cols[9]))

		print(COLUMNS[10])
		print(cols[1][23], cols[1][1033])
		print(cols[10][23], cols[10][1033])
		#some of the data is wrong(239735.72B)
		for x in range(len(cols[10])):
			mk=str(cols[10][x])
			if(mk[-4]=='B'):
				cols[10][x]=float(format(float(mk[2:-4])*10**3, '.0f'))
				if(cols[10][x]>10**6):
					cols[10][x]=cols[10][x]/(10**3)
			elif(mk[-4]=='M'):
				cols[10][x]=float(format(float(mk[2:-4]), '.2f'))
			else:
				cols[10][x]=0
		print("4")
		print(cols[10][23], cols[10][1033])
		print(cols[10][1:5])
		print(reduce(lambda x,y: float(x)+float(y),cols[10]) / len(cols[10]))
		print(max(cols[10]))
		
		print(cols[11][:20])
		for x in range(11,25):
			cols[x] = [float(str(s)[1:-2]) if str(s)[1:-2]!="'None'" else 0 for s in cols[x]]
			print(COLUMNS[x])
			print(cols[x][1:5])
			print(reduce(lambda x,y: x+y,cols[x]) / len(cols[x]))






























x=col_vals()
