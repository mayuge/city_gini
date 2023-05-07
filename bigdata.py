import csv
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt


def main():
	filename = 'コピーメッシュ_to_市町村_加工用データ_計算変更.csv'
	#ファイルをリスト化
	array = readfile(filename)
	#処理の内容
	#result = triangle(filename, array)
	plot(array)
	#ファイルを書き込み
	#writefile(filename, result)

def plot(array):
	JCODE ='22211'
	triAngle = 0
	cityName = ''
	pops = []
	for i in range(1,len(array)):
		if array[i][16] == JCODE and array[i][8]!=0 and array[i][8]!='':
			pops.append(int(array[i][8]))
			triAngle = float(array[i][11])
			cityName = array[i][21]

	pops.sort()
	popPile = []
	
	for i in range(0,len(pops)):
		tmp = 0
		for j in range(i,0,-1):
			tmp += pops[j]

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



def gini(filename, array):
	for i in range(1,len(array)):
		tmplist = []
		for j in range(1,len(array)):
			if array[i][16] == array[j][16]:
				if array[j][8] =='':
					array[j][8] = 0
				tmplist.append(int(array[j][8]))

		array[i][15] = gini2(tmplist)

	print(round(i/len(array)*100,1),array[i][15],array[i][21])	
	return array


def gini2(array):
    
    n = len(y)
    nume = 0
    for i in range(n):
        nume = nume + (i+1)*y[i]
        
    deno = n*sum(y)
    return ((2*nume)/deno - (n+1)/(n))*(n/(n-1))


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

#13がgrosspile
def grosspile(filename, array):
	for i in range(1,len(array)):
		popPile = 0
		for j in range(1,len(array)):
			#16はJCODE
			if array[i][16] == array[j][16]:
				#階段状に総計したpoppileを合計する
				popPile += int(array[j][12])
		
		#grosspile into list
		array[i][13] = popPile

		#10000件に一度保存
		if(i % 10000 == 0):
			writefile(filename, array)
		
		#パーセント、入力、市町村名を表示
		print(round(i/len(array)*100,1),array[i][13],array[i][21])	

	print('処理終了')		
	return array

#12がpoppile		
def poppile(filename, array):
	#max 387246 len(array)
	for i in range(1,len(array)):
			#array[i][16]はJCODE, array[i][8]はpopulation, array[9]は市町村メッシュ数 array[21]はcity-name
			#popGross は条件に当てはまる人口の累計
			popGross = 0
			for j in range(1,i+1):
				if array[i][16] == array[j][16] and array[j][8] !='':
					#連続したデータでないならば、同一JCODEのpopを階段状に総計する
					popGross += int(array[j][8])
				
			#popGross into list 
			array[i][12] = popGross
			
			#10000件に一度保存
			if(i % 10000 == 0):
				writefile(filename, array)

			#パーセント、入力、市町村名を表示
			print(round(i/len(array)*100,1),array[i][12],array[i][21])
	print('処理終了')		
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