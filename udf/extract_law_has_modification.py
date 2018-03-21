#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import ddlib
import divlaw
import handle_string
from datetime import datetime

def findDate(string):
	date_checker = re.search(r'(.(?!\n))+ngày \d{1,2} tháng \d{1,2} năm \d{2,4}',string,re.U|re.I|re.DOTALL)
	if date_checker is not None:
		if date_checker.start() <= 1:
			return extractDate(date_checker.group(0))
	date_checker = re.search(r'(.(?!\n))+\d{1,2}\/\d{1,2}\/\d{2,4}',string,re.U|re.I|re.DOTALL)
	if date_checker is not None:
		if date_checker.start() <= 1:
			return extractDate(date_checker.group(0))
	date_checker = re.search(r'(.(?!\n))+\d{1,2}-\d{1,2}-\d{2,4}',string,re.U|re.I|re.DOTALL)
	if date_checker is not None:
		if date_checker.start() <= 1:
			return extractDate(date_checker.group(0))
	return None

def extractDate(string):
	date = None
	end_last = 0;
	dd = re.search(r'\d{1,2}',string,re.U|re.M)
	if dd is not None:
		end_last += dd.end(0)
		date = dd.group(0)
	else :
		return None
	dd = re.search(r'\d{1,2}',string[end_last:],re.U|re.M)
	if dd is not None:
		end_last += dd.end(0)
		date = dd.group(0) + '-' + date 
	else :
		return None
	dd = re.search(r'\d{2,4}',string[end_last:],re.U|re.M)
	if dd is not None:
		if len(dd.group(0)) == 2:
			date = '19' +dd.group(0) + '-' + date 
		elif len(dd.group(0)) != 3:
			date = dd.group(0) + '-' + date
		else :
			return None
	else :
		return None
	return date

@tsv_extractor
@returns(lambda
    doc_id	= "text",
    doc_content = "text",
    modyfied_doc_released_date = "text"
    :[])
def extract(
    doc_id	= "text",
    header_text	= "text",
    title = "text"
    ):
	temp = ""
	if title.startswith('Sửa đổi') or title.startswith('Bổ sung'):
		check_symbol = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+[^A-Za-z]',title,re.U|re.I)
		if check_symbol is not None:
			yield [
				doc_id,
				(re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+',check_symbol.group(),re.U|re.I)).group(),
				findDate(title[check_symbol.end(0):])
			]
		else :
			get_content = re.finditer(re.escape(handle_string.toUpperCase(title.strip()))+
				r'\s(SỐ\s)*[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+[^A-Za-z]',handle_string.toUpperCase(header_text),re.U|re.I)
			if divlaw.lenIterator(get_content) >0 :
				get_content = re.finditer(re.escape(handle_string.toUpperCase(title.strip()))+
					r'\s(SỐ\s)*[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+[^A-Za-z]',handle_string.toUpperCase(header_text),re.U|re.I)
				for i in get_content:
					break
				yield [
						doc_id,
						(re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐƯ]+[0-9]*)+',i.group(0),re.U|re.I)).group(0),
						findDate(title[i.end():])
				]
			else :
				getTitleModified = re.finditer(r'của\s',title,re.U|re.I)
				if divlaw.lenIterator(getTitleModified) >0 :
					getTitleModified = re.finditer(r'của\s',title,re.U|re.I)
					for i in getTitleModified:
						break
					temp = title[i.end():]
					get_content = re.finditer(re.escape(handle_string.toUpperCase(title)),handle_string.toUpperCase(header_text),re.U|re.I)
					if divlaw.lenIterator(get_content) >0 :
						get_content = re.finditer(re.escape(handle_string.toUpperCase(title)),handle_string.toUpperCase(header_text),re.U|re.I)
						for i in get_content:
							pass
						yield [
					 		doc_id,
					 		temp,
					 		findDate(header_text[i.end():])
					 	]
					else :
						yield [
					 		doc_id,
					 		temp,
					 		None
					 	]