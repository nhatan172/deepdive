#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw

@tsv_extractor
@returns(lambda
    law_id         ="text",
    part_index      ="int",
    chap_index     ="int",
    sec_index		="int",
    totalLaw       ="int",
    law_index      ="int",
    law_start      ="int",
    law_end        ="int",
    law_name		="text",
    law_content			="text",
    title_end		="int"
    :[])
def extract(
    id 			="text",
    content 	="text",
    part_index  ="int",
    chap_index 	="int",
    sec_index 	="int",
    sec_start 	="int",
    sec_end 	="int"

    ):

	rs = divlaw.divPart(content)
	sec = divlaw.getSection(rs,part_index, chap_index, sec_index)
	totalLaw = sec['totalLaw']
	if totalLaw > 0:
		for i in range(0,totalLaw):
			start = sec['laws'][i]['start']
			end = sec['laws'][i]['end']
			title_end = end
			list_items = divlaw.newDivItem(content[start:end],start)
			if list_items[1] > 0:
				title_end = list_items[0][0]['start']
			yield [
				id,
				part_index,
				chap_index,
				sec_index,
				totalLaw,
				i,
				start,
				end,
				sec['laws'][i]['name'],
				content[start:end],
				title_end
			]
	else :
		yield [
			id,
			part_index,
			chap_index,
			sec_index,
			0,
			0,
			sec_start,
			sec_end,
			"",
			"",
			sec_end
		]