#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw

@tsv_extractor
@returns(lambda
    law_id         ="text",
    part_index      ="int",
    totalChap       ="int",
    chap_index      ="int",
    chap_start      ="int",
    chap_end        ="int",
    chap_name		="text"
    :[])
def extract(
    id 			="text",
    content 	="text",
    part_index 	="int",
    part_start 	="int",
    part_end 	="int"
    ):

	rs = divlaw.divPart(content)
	part = divlaw.getPart(rs,part_index)
	totalChap = part['totalChap']

	if totalChap > 0:
		for i in range(0,totalChap):
			yield [
				id,
				part_index,
				totalChap,
				i,
				part['chaps'][i]['start'],
				part['chaps'][i]['end'],
				part['chaps'][i]['name']
			]
	else :
		yield [
			id,
			part_index,
			0,
			0,
			part_start,
			part_end,
			None
		]