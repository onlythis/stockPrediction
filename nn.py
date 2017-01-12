import csv
from stock import sql
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

higharray=[]
lowarray=[]

class Input:
	def __init__(self,column,value):
		self.column=column
		self.value=value

def ConvertValue(column,value):
	col=26
	for x in range(2,25,1):
		if(column==COLUMNS[x]):
			col=x
	if(col==3):
		print(value)
		if(value[0]=='+'):
			value=value[1:len(value)]
			value=float(value)
		else:
			value=float(value)
	if(col==8 or col==10):
		for y in range(len(value)):
			if(value[y]=='B'):
				value=value[0:y]
				value=float(value)*1000000000
			elif(value[y]=='M'):
				value=value[0:y]
				value=float(value)*1000000
	if(value=="None"):
		return 0
	value=float(value)
	return value

def zeroToOne(inputs):
	ret=[]
	high=-100
	low=999999999999
	for y in range(len(inputs)):
		if(inputs[y]>high):
			high=inputs[y]
		if(inputs[y]<low):
			low=inputs[y]
	for y in range(len(inputs)):
		if(high-low==0):
			ret.append(0)
		else:
			ret.append((inputs[y]-low)/(high-low))
	saveHighLow(high,low)
	return ret

def saveHighLow(high,low):
	higharray.append(high)
	lowarray.append(low)

def symvalInputs(symvalslayer):
	layer =[]
	ret =[]
	for x in range(len(symvalslayer)):
		for n in range(23):
			layer.append(ConvertValue(COLUMNS[n+2],symvalslayer[x][n+2]))
		ret.append(layer)
		layer=[]
	return ret

def symTargets(layer):
	ret=[]
	for x in range(1,len(layer)):
		ret.append(layer[x][1])
	return ret

def ClassifyTargets(targs):
	targets=[]
	for x in range(len(targs)):
		if(targs[x][0]>2):
			targets.append(5)
		elif(targs[x][0]>1.5):
			targets.append(4)
		elif(targs[x][0]>1):
			targets.append(3)
		elif(targs[x][0]>.5):
			targets.append(2)
		elif(targs[x][0]>0):
			targets.append(1)
		elif(targs[x][0]<-2):
			targets.append(-5)
		elif(targs[x][0]<-1.5):
			targets.append(-4)
		elif(targs[x][0]<-1):
			targets.append(-3)
		elif(targs[x][0]<-.5):
			targets.append(-2)
		elif(targs[x][0]<0):
			targets.append(-1)
		else:
			targets.append(0)
	return targets

class NeuralNetwork:
	def __init__(self):
		self.symInputs=[]
		for x in range(len(symvals)):
			self.symInputs.append(symvalInputs(symvals[x]))
		self.symColumns=[]
		symcolumn=[]
		for x in range(23):
			for y in range(len(symvals)):#504
				for z in range(len(self.symInputs[1])):#number o days
					symcolumn.append(self.symInputs[y][z][x])
			self.symColumns.append(symcolumn)
			symcolumn=[]
		self.symValues=[]
		for x in range(23):
			self.symValues.append(zeroToOne(self.symColumns[x]))
		self.symTargets=[]
		for x in range(len(symvals)):
			self.symTargets.append(symTargets(self.symInputs[x]))
		self.symLayers=[]
		symlayer=[]
		symlayerday=[]
		for x in range(len(symvals)):#504
			for y in range(len(self.symInputs[1])):#number o days minus last day
				for z in range(23):
					symlayerday.append(self.symValues[z][y+(x*len(self.symInputs[1]))])#-1?
				symlayer.append(symlayerday)
				symlayerday=[]
			self.symLayers.append(symlayer)
			symlayer=[]
		self.inputs=[]
		self.lastday=[]
		for x in range(504):
			for y in range(len(self.symLayers[1])):
				if(y==len(self.symLayers[1])-1):
					self.lastday.append(self.symLayers[x][y])
				else:
					self.inputs.append(self.symLayers[x][y])
		print("Number of Inputs: " + str(len(self.inputs)))
		self.targets=[]
		for x in range(504):
			for y in range(len(self.symTargets[1])):
				self.targets.append([self.symTargets[x][y]])

	def NN(self):
		symlen=int(len(self.inputs)/504)
		print("training")
		out=[]
		error=[]
		for x in range(25):
			start=x*symlen
			sym=self.inputs[start:start+symlen]
			targets=self.targets[start:start+symlen]
			net = nl.net.newff([[0, 1]]*23, [22, 22, 1])
			net.trainf = nl.train.train_rprop #gd, gdm, gda, gdx, rprop
			e = net.train(sym, targets, show=100, epochs=100,goal=0.0001)
			out.append(net.sim([sym[symlen-1]]))
			error.append(e[len(e)-1])
		for x in range(25):
			print(symvals[x][symlen][1])
			print("actual: " + symvals[x][symlen][3])
			print("error: " + str(error[x]))
			print("predicted: " + str(out[x]))

	def NB(self):
		print("Naive Bayes")
		symlen=int(len(self.inputs)/504)
		targets=[]
		for x in range(len(self.targets)):
			if(self.targets[x][0]>0):
				targets.append(1)
			else:
				targets.append(0)
		total=0
		for x in range(504):
			gnb = GaussianNB()
			start=x*symlen
			inputs=numpy.array(self.inputs[start:start+symlen])
			targ=numpy.array(targets[start:start+symlen])
			pred=gnb.fit(inputs,targ).predict(inputs)
			total+=(targ==pred).sum()
		print("Correctly predicted: " + str(total))

	def SVM(self):
		print("svm")
		clf = svm.SVC()
		inputs = numpy.array(self.inputs)
		targets=ClassifyTargets(self.targets)
		pred=clf.fit(inputs,targets).predict(inputs)
		predtargets=[]
		for x in range(len(targets)):
			if(targets[x]>0):
				predtargets.append(1)
			else:
				predtargets.append(0)
		for x in range(len(pred)):
			if(pred[x]>0):
				pred[x]=1
			else:
				pred[x]=0
		print((predtargets==pred).sum())

	def NearCen(self):
		print("nearcen")
		inputs = numpy.array(self.inputs)
		targets=ClassifyTargets(self.targets)
		clf = NearestCentroid()
		pred = clf.fit(inputs,targets).predict(inputs)
		predtargets=[]
		for x in range(len(targets)):
			if(targets[x]>0):
				predtargets.append(1)
			else:
				predtargets.append(0)
		for x in range(len(pred)):
			if(pred[x]>0):
				pred[x]=1
			else:
				pred[x]=0
		print((predtargets==pred).sum())


	def SVR(self):
		print("svr")
		inputs = numpy.array(self.inputs)
		targets=ClassifyTargets(self.targets)
		clf = SVR(C=1.0, epsilon=.0)
		pred = clf.fit(inputs,targets).predict(inputs)
		predtargets=[]
		for x in range(len(targets)):
			if(targets[x]>0):
				predtargets.append(1)
			else:
				predtargets.append(0)
		for x in range(len(pred)):
			if(pred[x]>0):
				pred[x]=1
			else:
				pred[x]=0
		print((predtargets==pred).sum())

def run():
	test=NeuralNetwork()
	test.NB()
	#test.NearCen()
	#test.SVR()
	#test.SVM()
	test.NN()

if __name__ == "__main__":
	run()
