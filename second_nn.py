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

		cols = [select_col(index) for index in COLUMNS]
		cols[0] = self.days
		cols[1] = self.syms

		#price to avg_daily_volume
		for x in range(2,8):
			cols[x] = [float(str(s)[1:-2]) if str(s)[1:-2]!="'None'" else 0.0 for s in cols[x]]

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
				cols[8][x]=0.0


		cols[9] = [float(str(s)[1:-2]) if str(s)[1:-2]!="'None'" else 0.0 for s in cols[9]]

		for x in range(len(cols[9])):
			if(cols[9][x]>250):
				cols[9][x]=0.0
		#1 symbol of false data

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
				cols[10][x]=0.0
		for x in range(len(cols[10])):
			if(cols[10][x]<0):
				cols[10][x]=0.0
		for x in range(11,25):
			cols[x] = [float(str(s)[1:-2]) if str(s)[1:-2]!="'None'" else 0.0 for s in cols[x]]

		self.cols=cols
		#for x in range(2,25):
			#print(reduce(lambda x,y: x+y,cols[x]) / len(cols[x]))
			#print(reduce(lambda x,y: x+y,self.cols[x]) / len(self.cols[x]))

		for x in range(2,25):
			print(COLUMNS[x])
			print(max(self.cols[x]))
			print(min(self.cols[x]))
			print(reduce(lambda x,y: x+y,self.cols[x]) / len(self.cols[x]))
			#print(*(x for x in self.cols[x] if x <0))
		self.scaled_cols=cols
		for x in range(2,25):
			mini=min(cols[x])
			maxi=max(cols[x])
			try:
				line=(map(lambda x: (x-mini)/(maxi-mini),cols[x]))
				form=[float(format(y,'.8f')) for y in line]
				self.scaled_cols[x]=form
				print(reduce(lambda x,y: x+y,self.scaled_cols[x]) / len(self.scaled_cols[x]))
				#print(*(format(map(lambda x: (x-mini)/(maxi-mini),cols[x]),'.4f')))
			except TypeError as e:
				print(e)























x=col_vals()
