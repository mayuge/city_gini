import csv
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt



def main():
	filename = 'calSheetForCityGini.csv'
	#ファイルをリスト化
	array = readfile(filename)
	#処理の内容
	data = calGini(filename, array)
	result = countAcc(filename, data)
	#ファイルを書き込み
	writefile(filename, result)

def countAcc(filename, array):
	for i in range(1,len(array)):
		if array[i][59] == array[i-1][59]:
			array[i][72] = array[i-1][72]
			continue

		count = 0
		for j in range(1,len(array)):
			if(array[i][59] == array[j][59] and array[i][59] !='' and array[j][59] !=''):
				count += int(array[j][71])
		array[i][72] = count

		#10000件に一度保存
		if(i % 1000 == 0):
			writefile(filename, array)
		
		#パーセント、入力、市町村名を表示
		print(round(i/len(array)*100,1),array[i][72],array[i][64])	
	return array
	


def plotScat(array):
	for i in range(1,len(array)):
		if int(array[i][71]) > 5:
			y = int(array[i][71])
			x = float(array[i][8])
			plt.scatter(x, y, c='blue',s=5)
			print(round(i/len(array)*100),array[i][64],array[i][71])
	plt.show()

def calGini(filename, array):

	for i in range(1,len(array)):
		JCODE = array[i][59]
		TOTPOP = 9
		gini_num = 8

		if JCODE == array[i-1][59]:
			array[i][gini_num] = array[i-1][gini_num]
			continue

		
		popList = []

		for j in range(1,len(array)):
			if array[j][59] == JCODE and array[j][TOTPOP]!= 0 and array[j][TOTPOP] !='':
				popList.append(int(array[j][TOTPOP]))
		
		popList.sort()
		popPile = []

		for pop in range(0,len(popList)):
			tmp = 0
			for k in range(pop,0,-1):
				tmp += popList[k]
		
			popPile.append(tmp)

		grossPile = sum(popPile)
		#popPileの最後尾が人口

		#triangleのエラー対策
		try:
			triAngle = popPile[-1]*len(popPile)/2
		except:
			print('ERROR')
			array[i][gini_num] = 0
			continue

		#なぜかゼロで割られることがある
		if triAngle == 0:
			print('DIVIDE BY ZERO')
			array[i][gini_num] = 0
			continue

		gini = (triAngle-grossPile)/triAngle

		array[i][gini_num] = gini

		#1000件に一度保存
		if(i % 1000 == 0):
			writefile(filename, array)
		
		#パーセント、入力、市町村名を表示
		print(round(i/len(array)*100,1),array[i][8],array[i][64])	

	return array

def plotGini(array):
	JCODE = '15202'
	popList = []

	for j in range(1,len(array)):
		if array[j][59] == JCODE and array[j][9]!= 0 and array[j][9] !='':
			popList.append(int(array[j][9]))
			cityName = array[j][64]
	
	popList.sort()
	print(popList)
	popPile = []

	for pop in range(0,len(popList)):
		tmp = 0
		for k in range(pop,0,-1):
			tmp += popList[k]
	
		popPile.append(tmp)

	grossPile = sum(popPile)

	#popPileの最後尾が人口
	triAngle = popPile[-1]*len(popPile)/2

	gini = (triAngle-grossPile)/triAngle

	# プロット範囲のxを用意
	x = np.arange(0,len(popPile))
	
	# xに対応するyの値を用意
	y = popPile
	
	# pyplot.plot(x, y)でプロット作成
	plt.plot(x, y)

	plt.title(cityName+'のジニ係数　'+str((triAngle-grossPile)/triAngle), fontname="MS Gothic")
	
	# plt.show()で画面に表示（Jupyter Notebookの場合は不要）
	plt.show()

		










def plot(array):
	JCODE ='15202'
	triAngle = 0
	cityName = ''
	popList = []
	#抽出
	for i in range(1,len(array)):
		if array[i][16] == JCODE and array[i][8]!=0 and array[i][8]!='':
			popList.append(int(array[i][8]))
			triAngle = float(array[i][11])
			cityName = array[i][21]

	popList.sort()

	popPile = []
	#積み上げ
	for i in range(0,len(popList)):
		tmp = 0
		for j in range(i,0,-1):
			tmp += popList[j]

		popPile.append(tmp)

	grossPile = sum(popPile)

	# プロット範囲のxを用意
	x = np.arange(0,len(popPile))
	
	# xに対応するyの値を用意
	y = popPile
	
	# pyplot.plot(x, y)でプロット作成
	plt.plot(x, y)

	plt.title(cityName+'のジニ係数　'+str((triAngle-grossPile)/triAngle), fontname="MS Gothic")
	
	# plt.show()で画面に表示（Jupyter Notebookの場合は不要）
	plt.show()

def readfile(filename):    
	print('読込中')
	with open(filename, 'r', newline='', encoding='shift-jis') as csvfile:
		#CSVを読み込む
		csvreader = csv.reader(csvfile)
		#SBVをリスト化
		array = list(csvreader)
		
		print('読込完了')
		return array


def triangle(filename, array):
	for i in range(1,len(array)):
		
		#三角形の面積を求める
		array[i][14] = float(array[i][10]) * float(array[i][9]) / 2
		#dont devide by zero
		if int(array[i][14]) != 0:
			#ジニ係数
			array[i][15] = abs(float(array[i][14])-int(array[i][13]))/ int(array[i][14])

		#10000件に一度保存
		if(i % 10000 == 0):
			writefile(filename, array)

		#パーセント、入力、市町村名を表示
		print(round(i/len(array)*100,1),array[i][14],array[i][15],array[i][21])	

	return array


def writefile(filename, array):
    with open(filename, 'w', newline='', encoding='shift-jis') as csvfile:
        csvwriter = csv.writer(csvfile)
        try:
            print('書き込み中')
            csvwriter.writerows(array)
        finally:
            print('書き込み終了')
main()
print('終了')