#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import ddlib
import divlaw
import handle_string
from datetime import datetime

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
		check_symbol = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+',title,re.U|re.I)
		if check_symbol is not None:
			yield [
				doc_id,
				check_symbol.group(),
				None
			]
		else :
			get_content = re.finditer(re.escape(title)+r'\ssố\s',header_text,re.U|re.I)
			if divlaw.lenIterator(get_content) >0 :
				get_content = re.finditer(re.escape(title)+r'\ssố\s',header_text,re.U|re.I)
				for i in get_content:
					break
				get_id = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+',header_text[i.end():],re.U|re.I)
				if(get_id is not None):
					yield [
						doc_id,
						get_id.group(),
						None
					]
			else :
				getTitleModified = re.finditer(r'của\s',title,re.U|re.I)
				if divlaw.lenIterator(getTitleModified) >0 :
					getTitleModified = re.finditer(r'của\s',title,re.U|re.I)
					for i in getTitleModified:
						break
					temp = title[i.end():]
				get_content = re.finditer(re.escape(title)+r'(.(?!thông\squa\s))+',header_text,re.U|re.I)
				if divlaw.lenIterator(get_content) >0 :
					get_content = re.finditer(re.escape(title)+r'(.(?!thông\squa\s))+',header_text,re.U|re.I)
					for i in get_content:
						break
					get_date = re.finditer(r'ngày\s\d{1,2}\stháng\s\d{1,2}\snăm\s\d{4}',header_text[i.end():],re.U|re.I)
					if divlaw.lenIterator(get_date) > 0:
						get_date = re.finditer(r'ngày\s\d{1,2}\stháng\s\d{1,2}\snăm\s\d{4}',header_text[i.end():],re.U|re.I)
						for j in get_date:
							break
						date = header_text[i.end()+j.start():i.end()+j.end()]
						findNumber = re.finditer(r'\d+',date)
						tempDate = None
						for indx,n in enumerate(findNumber):
							if indx == 0 :
								temp1 = date[n.start():n.end()]
								tempDate = '0'+temp1 if len(temp1) < 2 else temp1
							if indx == 1:
								temp1 = date[n.start():n.end()]
								temp2 = '0'+temp1 if len(temp1) < 2 else temp1
								tempDate = temp2 +'-'+ tempDate
							if indx == 2:
								temp1 = date[n.start():n.end()]
								tempDate = temp1 +'-'+ tempDate
								break
						yield [
					 		doc_id,
					 		temp,
					 		tempDate
					 	]
