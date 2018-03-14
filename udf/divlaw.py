# -*- coding:utf8 -*-

import re


#chia doan van thanh list cac text dua tren cac chi so bat dau cua cac doan trong array
def split(string,array):
	result = []
	for i in range(0,len(array)) :
		if(i != (len(array)-1)) :
			result.append(string[array[i]:array[i+1]])
		else:
			result.append(string[array[i]:(len(string)-1)])
	return result	
#sua lai gia tri bat dau cho cac index trong array
def check(string,array):
	for i in range(0,len(array)) :
		if(string[(array[i]-2):array[i]] == "**"):
			array[i] = array[i]-2
	return array
#check xem trong dong chua tu do co in dam hay ko (**xxx**)
def reFind(string,array):
	for i in range(0,len(array)):
		count = 0;
		tempInt = array[i] - 2
		tempC = string[tempInt]
		while tempC != '\n':
			if (tempC == '*'):
				count += 1
			tempInt += 1
			tempC = string[tempInt]
		if count < 2 :
			del array[i]
	return array
#do dai cua list
def lenIterator(list):
	sum = 0
	if list != None :
		for i in list :
			sum += 1
	return sum
def itemInQuote(string, index) :
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	for i in quotes :
		if index >= i.span()[0] and index < i.span()[1] :
			return True
	return False
#Chia theo phan
def divPart(string):
	limitText = len(string)
	partIndex = []
	it = re.finditer(r"\\n(\*|\s|\#|\_|\.)*(Phần(\*|\s|\#|\_)+thứ|PHẦN(\*|\s|\#|\_)+THỨ)(\*|\s|\#|\_)+", string)
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	if lenIterator(it) > 0 :
		it = re.finditer(r"\\n(\*|\s|\#|\_|\.)*(Phần(\*|\s|\#|\_)+thứ|PHẦN(\*|\s|\#|\_)+THỨ)(\*|\s|\#|\_)+", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					partIndex.append(match.span()[0]+2)
			else :
				partIndex.append(match.span()[0]+2)
		sum = len(partIndex)
	if sum > 0 :
		result = {
			"totalPart": len(partIndex),
			"parts" : ""
		}
		listParts = []
		for i in range(0,len(partIndex)):
			if i!=(len(partIndex)-1):
				part = {
					"start":partIndex[i],
					"end": (partIndex[i+1]),
					"totalChap": "",
					"chaps": "",
					"name" : ""
				}
				res = divChapter(string[partIndex[i]:partIndex[i+1]],partIndex[i])
				part['chaps'] = res[0]
				part['totalChap'] = res[1]
				findName = re.finditer(r"(Phần(\*|\s|\#|\_)+thứ|PHẦN(\*|\s|\#|\_)+THỨ)(\*|\s|\#|\_)+([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Phần(\*|\s|\#|\_)+thứ|PHẦN(\*|\s|\#|\_)+THỨ)(\*|\s|\#|\_)+([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
					for fN in findName:
						part['name'] = string[partIndex[i]+fN.span()[0]:partIndex[i]+fN.span()[1]]
						part['name'] = re.sub(r"(\*|\#|\_)",'',part['name'])
						break
				listParts.append(part)
			else :
				part = {
					"start":partIndex[i],
					"end": limitText,
					"totalChap": "",
					"chaps": "",
					"name" : ""
				}
				res = divChapter(string[partIndex[i]:limitText],partIndex[i])
				part['chaps'] = res[0]
				part['totalChap'] = res[1]
				findName = re.finditer(r"(Phần(\*|\s|\#|\_)+thứ|PHẦN(\*|\s|\#|\_)+THỨ)(\*|\s|\#|\_)+([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Phần(\*|\s|\#|\_)+thứ|PHẦN(\*|\s|\#|\_)+THỨ)(\*|\s|\#|\_)+([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
					for fN in findName:
						part['name'] = string[partIndex[i]+fN.span()[0]:partIndex[i]+fN.span()[1]]
						part['name'] = re.sub(r"(\*|\#|\_)",'',part['name'])
						break
				listParts.append(part)
		result['[parts'] = listParts
	else :
		result = {
			"totalPart": 0,
			"parts" : ""
		}
		listParts = []
		part = {
					"start": 0,
					"end": len(string),
					"totalChap": "",
					"chaps": "",
					"name": ""
				}
		res = divChapter(string,0)
		part['chaps'] = res[0]
		part['totalChap'] = res[1]
		listParts.append(part)
	result['parts'] = listParts
	return result
#(\\n(\*|\s|\#|\_|\“|\")*(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+)
#Chia theo chuong
def divChapter(string, startIndex) :
	it = re.finditer(r"\\n(\*|\s|\#|\_)*(Chương|CHƯƠNG)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])", string)
	chapterIndex = [] #chuoi cac index bat dau cua cac chapter
	listChaps = []
	sum =  0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)
	if  a >0:
		it = re.finditer(r"\\n(\*|\s|\#|\_)*(Chương|CHƯƠNG)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					chapterIndex.append(match.span()[0])
			else :
				chapterIndex.append(match.span()[0])
		sum = len(chapterIndex)
	if sum > 0 :
		for j in range(0,len(chapterIndex)):
			if j != (len(chapterIndex)-1):
				chap = {
					"start":(chapterIndex[j]+startIndex),
					"end": (chapterIndex[j+1]+startIndex),
					"totalSec": "",
					"secs": "",
					"name": ""
				}
				res = divSection(string[chapterIndex[j]:chapterIndex[j+1]],chapterIndex[j]+startIndex)
				chap['secs'] = res[0]
				chap['totalSec'] = res[1]
				findName = re.finditer(r"(Chương|CHƯƠNG)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Chương|CHƯƠNG)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
					for fN in findName:
						chap['name'] = string[chapterIndex[j]+fN.span()[0]:chapterIndex[j]+fN.span()[1]]
						chap['name'] = re.sub(r"(\*|\#|\_)",'',chap['name'])
						break
				listChaps.append(chap)
			else :
				chap = {
					"start":chapterIndex[j]+startIndex,
					"end": len(string)+startIndex,
					"totalSec": "",
					"secs": "",
					"name": ""
				}
				res = divSection(string[chapterIndex[j]:len(string)],chapterIndex[j]+startIndex)
				chap['secs'] = res[0]
				chap['totalSec'] = res[1]
				findName = re.finditer(r"(Chương|CHƯƠNG)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Chương|CHƯƠNG)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
					for fN in findName:
						chap['name'] = string[chapterIndex[j]+fN.span()[0]:chapterIndex[j]+fN.span()[1]]
						chap['name'] = re.sub(r"(\*|\#|\_)",'',chap['name'])
						break
				listChaps.append(chap)
	else :
		chap = {
					"start": startIndex ,
					"end": startIndex+len(string),
					"totalSec": "",
					"secs": "",
					"name": ""
				}
		res = divSection(string,startIndex)
		chap['secs'] = res[0]
		chap['totalSec'] = res[1]
		listChaps.append(chap)
	resultlist = []
	resultlist.append(listChaps)
	resultlist.append(sum)
	return resultlist	

#Chia theo muc
def divSection(string, startIndex):
	it = re.finditer(r"(\\n(\*|\s|\#|\_|\.)*(Mục|MỤC)(\*|\s|\#|\_)+(\w|[0-9])+(\_|\.|\s)*)", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	a = lenIterator(it)
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	if a>0:
		it = re.finditer(r"(\\n(\*|\s|\#|\_|\.)*(Mục|MỤC)(\*|\s|\#|\_)+(\w|[0-9])+(\_|\.|\s)*)", string)
		for match in it:
			if sumQoutes > 0:
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else:
				sectionIndex.append(match.span()[0])
		sum = lenIterator(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex),
					"end": (sectionIndex[j+1]+startIndex),
					"totalLaw": "",
					"laws": "",
					"name": ""
				}
				res = divLaw(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['laws'] = res[0]
				sec['totalLaw'] = res[1]
				findName = re.finditer(r"(Mục|MỤC)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Mục|MỤC)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						sec['name'] = re.sub(r"(\*|\#|\_)",'',sec['name'])
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex,
					"end": len(string) +startIndex,
					"totalLaw": "",
					"laws": "",
					"name":""
				}
				res = divLaw(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['laws'] = res[0]
				sec['totalLaw'] = res[1]
				findName = re.finditer(r"(Mục|MỤC)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Mục|MỤC)(\*|\s|\#|\_)+([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						sec['name'] = re.sub(r"(\*|\#|\_)",'',sec['name'])
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"totalLaw": "",
					"laws": "",
					"name":""
				}
		res = divLaw(string,startIndex)
		sec['laws'] = res[0]
		sec['totalLaw'] = res[1]
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist

#chia theo dieu
#dont need change name variable
def divLaw(string,startIndex):
	it = re.finditer(r"\\n(\*|\s|\#|\_)*(Điều|ĐIỀU|Điều)(\*|\s|\#|\_)+[0-9]+(\w|Đ|đ)*", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	a = lenIterator(it)
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	if a>0:
		it = re.finditer(r"\\n(\*|\s|\#|\_)*(Điều|ĐIỀU|Điều)(\*|\s|\#|\_)+[0-9]+(\w|Đ|đ)*", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0]+2)
			else :
				sectionIndex.append(match.span()[0]+2)
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex),
					"end": (sectionIndex[j+1]+startIndex),
					"totalItem": "",
					"items":"",
					"name": ""
				}
				findName = re.finditer(r"(Điều|ĐIỀU|Điều)(\*|\s|\#|\_)+[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Điều|ĐIỀU|Điều)(\*|\s|\#|\_)+[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						sec['name'] = re.sub(r"(\*|\#|\_)",'',sec['name'])
						break
				# res = divItem(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				# sec['items'] = res[0]
				# sec['totalItem'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex,
					"end": len(string) +startIndex,
					"totalItem": "",
					"items":"",
					"name":""
				}
				findName = re.finditer(r"(Điều|ĐIỀU|Điều)(\*|\s|\#|\_)+[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Điều|ĐIỀU|Điều)(\*|\s|\#|\_)+[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						sec['name'] = re.sub(r"(\*|\#|\_)",'',sec['name'])
						break
				# res = divItem(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				# sec['items'] = res[0]
				# sec['totalItem'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"totalItem": "",
					"items":"",
					"name": ""
				}
		# res = divItem(string,startIndex)
		# sec['items'] = res[0]
		# sec['totalItem'] = res[1]
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist

def divItem(string,startIndex) :
	it = re.finditer(r"\\n(\*|\s|\#|\_)*[0-9]+(\w|Đ|đ)*", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)
	
	if a>0:
		it = re.finditer(r"\\n(\*|\s|\#|\_)*[0-9]+(\w|Đ|đ)*", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else :
				sectionIndex.append(match.span()[0])
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex)+2,
					"end": (sectionIndex[j+1]+startIndex)+2,
					"name": "",
					"totalPoint": "",
					"points": ""
				}
				findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divPoint(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['points'] = res[0]
				sec['totalPoint'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) + startIndex,
					"name": "",
					"totalPoint": "",
					"points": ""
				}
				findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divPoint(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['points'] = res[0]
				sec['totalPoint'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": "",
					"totalPoint": "0",
					"points": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist
def divPoint(string,startIndex) :
	it = re.finditer(r"\\n(\s|\*|\_|\#)*(\w|đ)+(\s|\*|\_)*\)", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)

	if a>0:
		it = re.finditer(r"\\n(\s|\*|\_|\#)*([a-z]|đ)+(\s|\*|\_)*\)", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else :
				sectionIndex.append(match.span()[0])
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex)+2,
					"end": (sectionIndex[j+1]+startIndex),
					"name": ""
				}
				findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]+2:sectionIndex[j] + 2 +fN.span()[1]]
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) +startIndex,
					"name":""
				}
				findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]+2:sectionIndex[j]+ 2 +fN.span()[1]]
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist
def newDivItem(string,startIndex):
	it = re.finditer(r"\\n(\*|\s|\#|\_)*[0-9]+(\w|Đ|đ)*", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string,re.DOTALL)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)

	if a>0:
		it = re.finditer(r"\\n(\*|\s|\#|\_)*[0-9]+(\w|Đ|đ)*", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else :
				sectionIndex.append(match.span()[0])
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex + 2),
					"end": (sectionIndex[j+1]+startIndex + 2),
					"name": "",
					"content": string[sectionIndex[j]+2:sectionIndex[j+1]+2]
				}
				findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) + startIndex,
					"name": "",
					"content": string[sectionIndex[j]+2:]
				}
				findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist
def newDivPoint(string,startIndex):
	it = re.finditer(r"\\n(\s|\*|\_|\#)*(\w|đ)+(\s|\*|\_)*\)", string)
	sectionIndex = []
	listSecs = []
	sum = 0
	quotes = re.finditer(r"(\“(.(?!\“|\”))+.{2})|(\"(.(?!\"))+.{2})", string)
	sumQoutes = lenIterator(quotes)
	a = lenIterator(it)

	if a>0:
		it = re.finditer(r"\\n(\s|\*|\_|\#)*([a-z]|đ)+(\s|\*|\_)*\)", string)
		for match in it:
			if sumQoutes > 0 :
				if itemInQuote(string, match.span()[0]) == False :
					sectionIndex.append(match.span()[0])
			else :
				sectionIndex.append(match.span()[0])
		sum = len(sectionIndex)
	if sum > 0 :
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex + 2),
					"end": (sectionIndex[j+1] + startIndex + 2),
					"name": "",
					"content": string[sectionIndex[j]+2:sectionIndex[j+1]+2]
				}
				findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]+2:sectionIndex[j] + 2 +fN.span()[1]]
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) +startIndex,
					"name":"",
					"content": string[sectionIndex[j]+2:len(string)]
				}
				findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"([a-z]|đ)+",string[sectionIndex[j]+2:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]+2:sectionIndex[j]+ 2 +fN.span()[1]]
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(sum)
	return resultlist
def getHeader(content) :
	result = divPart(content)
	id_firstPart = result['parts'][0]['start']
	id_firstChapter = result['parts'][0]['chaps'][0]['start']
	id_firstSec = result['parts'][0]['chaps'][0]['secs'][0]['start']
	id_firstLaw = result['parts'][0]['chaps'][0]['secs'][0]['laws'][0]['start']
	alist = []
	if id_firstPart > 0 :
		alist.append(id_firstPart)
	if id_firstChapter > 0 :
		alist.append(id_firstChapter)
	if id_firstSec > 0	:
		alist.append(id_firstSec)
	if id_firstLaw > 0 :
		alist.append(id_firstLaw)
	if not alist:
		return len(content)
	return min(alist)

def getTotalPart(result) :
	return result['totalPart']

def getTotalChapter(result, indexPart) :
	return result['parts'][indexPart]['totalChap']

def getTotalSection(result, indexPart, indexChapter) :
	return result['parts'][indexPart]['chaps'][indexChapter]['totalSec']

def getTotalLaw(result,indexPart,indexChapter,indexSec) :
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['totalLaw']

def getTotalItem(result,indexPart,indexChapter,indexSec,indexLaw) :
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][indexLaw]['totalItem']
def getTotalPoint(result,indexPart,indexChapter,indexSec,indexLaw,indexItem):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][indexLaw]['items'][indexItem]['totalPoint']

def getPart(result,index):
	return result['parts'][index]

def getChapter(result,indexPart,index):
	return result['parts'][indexPart]['chaps'][index]

def getSection(result, indexPart, indexChapter, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][index]

def getLaw(result, indexPart, indexChapter, indexSec, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][index]

def getItem(result, indexPart, indexChapter, indexSec, indexLaw, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][indexLaw]['items'][index]

def getPoint(result, indexPart, indexChapter, indexSec, indexLaw, indexItem, index):
	return result['parts'][indexPart]['chaps'][indexChapter]['secs'][indexSec]['laws'][indexLaw]['items'][indexItem]['points'][index]

#problem with iterator -> generator
#################################
def divPartModifyLaw(string):
	limitText = len(string)
	partIndex = []
	it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\")*(Phần thứ|PHẦN THỨ)\s", string)
	if lenIterator(it) > 0 :
		it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\")*(Phần thứ|PHẦN THỨ)\s", string)
		for match in it:
			partIndex.append(match.span()[0]+2)
		result = {
			"totalPart": len(partIndex),
			"parts" : ""
		}
		listParts = []
		for i in range(0,len(partIndex)):
			if i!=(len(partIndex)-1):
				part = {
					"start":partIndex[i],
					"end": (partIndex[i+1]),
					"totalChap": "",
					"chaps": "",
					"name": "",
				}
				res = divChapterModifyLaw(string[partIndex[i]:partIndex[i+1]],partIndex[i])
				part['chaps'] = res[0]
				part['totalChap'] = res[1]
				findName = re.finditer(r"(Phần thứ|PHẦN THỨ)\s([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Phần thứ|PHẦN THỨ)\s([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
					for fN in findName:
						part['name'] = string[partIndex[i]+fN.span()[0]:partIndex[i]+fN.span()[1]]
						break
				listParts.append(part)
			else :
				part = {
					"start":partIndex[i],
					"end": limitText,
					"totalChap": "",
					"chaps": "",
					"name": ""
				}
				res = divChapterModifyLaw(string[partIndex[i]:limitText],partIndex[i])
				part['chaps'] = res[0]
				part['totalChap'] = res[1]
				listParts.append(part)
				findName = re.finditer(r"(Phần thứ|PHẦN THỨ)\s([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Phần thứ|PHẦN THỨ)\s([A-Z]|[a-z]|À|Á|Â|Ã|È|É|Ê|Ì|Í|Ò|Ó|Ô|Õ|Ù|Ú|Ă|Đ|Ĩ|Ũ|Ơ|à|á|â|ã|è|é|ê|ì|í|ò|ó|ô|õ|ù|ú|ă|đ|ĩ|ũ|ơ|Ư|Ă|Ạ|Ả|Ấ|Ầ|Ẩ|Ẫ|Ậ|Ắ|Ằ|Ẳ|Ẵ|Ặ|Ẹ|Ẻ|Ẽ|Ề|Ề|Ể|ư|ă|ạ|ả|ấ|ầ|ẩ|ẫ|ậ|ắ|ằ|ẳ|ẵ|ặ|ẹ|ẻ|ẽ|ề|ế|ể|Ễ|Ệ|Ỉ|Ị|Ọ|Ỏ|Ố|Ồ|Ổ|Ỗ|Ộ|Ớ|Ờ|Ở|Ỡ|Ợ|Ụ|Ủ|Ứ|Ừ|ễ|ệ|ỉ|ị|ọ|ỏ|ố|ồ|ổ|ỗ|ộ|ớ|ờ|ở|ỡ|ợ|ụ|ủ|ứ|ừ|Ử|Ữ|Ự|Ỳ|Ỵ|Ý|Ỷ|Ỹ|ử|ữ|ự|ỳ|ỵ|ỷ|ỹ)+",string[partIndex[i]:len(string)])
					for fN in findName:
						part['name'] = string[partIndex[i]+fN.span()[0]:partIndex[i]+fN.span()[1]]
						break
		result['[parts'] = listParts
	else :
		result = {
			"totalPart": 0,
			"parts" : "",
		}
		listParts = []
		part = {
					"start": 0,
					"end": len(string),
					"totalChap": "",
					"chaps": "",
					"name": ""
				}
		res = divChapterModifyLaw(string,0)
		part['chaps'] = res[0]
		part['totalChap'] = res[1]
		listParts.append(part)
	result['parts'] = listParts
	return result

#Chia theo chuong
def divChapterModifyLaw(string, startIndex) :
	it = re.finditer(r"(\\n(\*|\s|\#|\_|\“|\")*(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+)", string)
	chapterIndex = [] #chuoi cac index bat dau cua cac chapter
	listChaps = []
	a = lenIterator(it)
	if  a >0:
		it = re.finditer(r"(\\n(\*|\s|\#|\_|\“|\")*(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+)", string)
		for match in it:
			chapterIndex.append(match.span()[0])
		for j in range(0,len(chapterIndex)):
			if j!=(len(chapterIndex)-1):
				chap = {
					"start":(chapterIndex[j]+startIndex),
					"end": (chapterIndex[j+1]+startIndex),
					"totalSec": "",
					"secs": "",
					"name": ""
				}
				res = divSectionModifyLaw(string[chapterIndex[j]:chapterIndex[j+1]],chapterIndex[j]+startIndex)
				chap['secs'] = res[0]
				chap['totalSec'] = res[1]
				findName = re.finditer(r"(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
					for fN in findName:
						chap['name'] = string[chapterIndex[j]+fN.span()[0]:chapterIndex[j]+fN.span()[1]]
						break
				listChaps.append(chap)
			else :
				chap = {
					"start":chapterIndex[j]+startIndex,
					"end": len(string)+startIndex,
					"totalSec": "",
					"secs": "",
					"name": ""
				}
				res = divSectionModifyLaw(string[chapterIndex[j]:len(string)],chapterIndex[j]+startIndex)
				chap['secs'] = res[0]
				chap['totalSec'] = res[1]
				findName = re.finditer(r"(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Chương|CHƯƠNG)\s([A-Z]|[a-z]|[0-9])+",string[chapterIndex[j]:len(string)])
					for fN in findName:
						chap['name'] = string[chapterIndex[j]+fN.span()[0]:chapterIndex[j]+fN.span()[1]]
						break
				listChaps.append(chap)
	else :
		chap = {
					"start": startIndex ,
					"end": startIndex+len(string),
					"totalSec": "",
					"secs": "",
					"name": ""
				}
		res = divSectionModifyLaw(string,startIndex)
		chap['secs'] = res[0]
		chap['totalSec'] = res[1]
		listChaps.append(chap)
	resultlist = []
	resultlist.append(listChaps)
	resultlist.append(a)
	return resultlist	

#Chia theo muc
def divSectionModifyLaw(string, startIndex):
	it = re.finditer(r"(\\n(\*|\s|\#|\_|\“|\"|\.)*(Mục|MỤC)\s([A-Z]|[a-z]|[0-9])+)", string)
	sectionIndex = []
	listSecs = []
	a = lenIterator(it)
	if a>0:
		it = re.finditer(r"(\\n(\*|\s|\#|\_|\“|\"|\.)*(Mục|MỤC)\s([A-Z]|[a-z]|[0-9])+)", string)
		for match in it:
			sectionIndex.append(match.span()[0])
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex),
					"end": (sectionIndex[j+1]+startIndex),
					"totalLaw": "",
					"laws": "",
					"name": ""
				}
				res = divLawModifyLaw(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['laws'] = res[0]
				sec['totalLaw'] = res[1]
				findName = re.finditer(r"(Mục|MỤC)\s([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Mục|MỤC)\s([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex,
					"end": len(string) +startIndex,
					"totalLaw": "",
					"laws": "",
					"name": ""
				}
				res = divLawModifyLaw(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['laws'] = res[0]
				sec['totalLaw'] = res[1]
				findName = re.finditer(r"(Mục|MỤC)\s([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(Mục|MỤC)\s([A-Z]|[a-z]|[0-9])+",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"totalLaw": "",
					"laws": "",
					"name": ""
				}
		res = divLawModifyLaw(string,startIndex)
		sec['laws'] = res[0]
		sec['totalLaw'] = res[1]
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(a)
	return resultlist

#chia theo dieu
#dont need change name variable
def divLawModifyLaw(string,startIndex):
	it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\"|\.)*Điều [0-9]+(\w|Đ|đ)*", string)
	sectionIndex = []
	listSecs = []
	a = lenIterator(it)
	if a>0:
		it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\"|\.)*Điều [0-9]+(\w|Đ|đ)*", string)
		for match in it:
			sectionIndex.append(match.span()[0]+2)
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex),
					"end": (sectionIndex[j+1]+startIndex),
					"totalItem": "",
					"items":"",
					"name": ""
				}
				findName = re.finditer(r"Điều [0-9]+(\w|Đ|đ)+",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"Điều [0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divItemModifyLaw(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['items'] = res[0]
				sec['totalItem'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex,
					"end": len(string) +startIndex,
					"totalItem": "",
					"items":"",
					"name":""
				}
				findName = re.finditer(r"Điều [0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"Điều [0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divItemModifyLaw(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['items'] = res[0]
				sec['totalItem'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"totalItem": "",
					"items":"",
					"name": ""
				}
		res = divItemModifyLaw(string,startIndex)
		sec['items'] = res[0]
		sec['totalItem'] = res[1]
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(a)
	return resultlist

def divItemModifyLaw(string,startIndex) :
	it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\"|\.)*[0-9]+(\w|Đ|đ)*", string)
	sectionIndex = []
	listSecs = []
	a = lenIterator(it)
	if a>0:
		it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\"|\.)*[0-9]+(\w|Đ|đ)*", string)
		for match in it:
			sectionIndex.append(match.span()[0])
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex)+2,
					"end": (sectionIndex[j+1]+startIndex)+2,
					"name": "",
					"totalPoint": "",
					"points": ""
				}
				findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+(\w|Đ|đ)*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divPointModifyLaw(string[sectionIndex[j]:sectionIndex[j+1]],sectionIndex[j]+startIndex)
				sec['points'] = res[0]
				sec['totalPoint'] = res[1]
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) + startIndex,
					"name": "",
					"totalPoint": "",
					"points": ""
				}
				findName = re.finditer(r"[0-9]+\w*",string[sectionIndex[j]:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"[0-9]+\w*",string[sectionIndex[j]:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+fN.span()[0]:sectionIndex[j]+fN.span()[1]]
						break
				res = divPointModifyLaw(string[sectionIndex[j]:len(string)],sectionIndex[j]+startIndex)
				sec['points'] = res[0]
				sec['totalPoint'] = res[1]
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": "",
					"totalPoint": "",
					"points": ""
				}
		listSecs.append(sec)
		res = divPointModifyLaw(string,startIndex)
		sec['points'] = res[0]
		sec['totalPoint'] = res[1]
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(a)
	return resultlist
def divPointModifyLaw(string,startIndex) :
	it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\"|\.)*(\w|đ)+(\*|\s|\#|\_|\“|\"|\.)*\)", string)
	sectionIndex = []
	listSecs = []
	a = lenIterator(it)
	if a>0:
		it = re.finditer(r"\\n(\*|\s|\#|\_|\“|\"|\.)*(\w|đ)+(\*|\s|\#|\_|\“|\"|\.)*\)", string)
		for match in it:
			sectionIndex.append(match.span()[0])
		for j in range(0,len(sectionIndex)):
			if j!=(len(sectionIndex)-1):
				sec = {
					"start":(sectionIndex[j]+startIndex)+2,
					"end": (sectionIndex[j+1]+startIndex),
					"name": ""
				}
				findName = re.finditer(r"(\w|đ)+",string[sectionIndex[j]+2:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(\w|đ)+",string[sectionIndex[j]+2:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+2+fN.span()[0]:sectionIndex[j]+2+fN.span()[1]]
						break
				listSecs.append(sec)
			else :
				sec = {
					"start":sectionIndex[j]+startIndex+2,
					"end": len(string) +startIndex,
					"name":""
				}
				findName = re.finditer(r"(\w|đ)+",string[sectionIndex[j]+2:len(string)])
				if lenIterator(findName)>0 :
					findName = re.finditer(r"(\w|đ)+",string[sectionIndex[j]+2:len(string)])
					for fN in findName:
						sec['name'] = string[sectionIndex[j]+2+fN.span()[0]:sectionIndex[j]+2+fN.span()[1]]
						break
				listSecs.append(sec)
	else :
		sec = {
					"start": startIndex,
					"end": startIndex+len(string),
					"name": ""
				}
		listSecs.append(sec)
	resultlist = []
	resultlist.append(listSecs)
	resultlist.append(a)
	return resultlist
	## sua lai get name
def getCover(law):
	result = []
	if (law['totalPart']>0):
		result.append(1)
		result.append(law['totalPart']['parts'][0]['name'])
		return result
	elif getTotalChapter(law,0) > 0:
		chapter = getChapter(law,0,0)
		result.append(2)
		result.append(chapter['name'])
		return result
	elif getTotalSection(law,0,0) > 0:
		section = getSection(law,0,0,0)
		result.append(3)
		result.append(section['name'])
		return result
	elif getTotalLaw(law,0,0,0):
		law = getLaw(law,0,0,0,0)
		result.append(4)
		result.append(law['name'])
		return result
	elif getTotalItem(law,0,0,0,0):
		item = getItem(law,0,0,0,0,0)
		result.append(5)
		result.append(item[name])
		return result
	elif getTotalPoint(law,0,0,0,0,0):
		point = getPoint(law,0,0,0,0,0,0)
		result.append(6)
		result.append(point['name'])
		return result
	return None


