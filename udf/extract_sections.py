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
    totalSec       ="int",
    sec_index      ="int",
    sec_start      ="int",
    sec_end        ="int",
    sec_name		="text"
    :[])
def extract(
    id 			="text",
    content 	="text",
    part_index  ="int",
    chap_index 	="int",
    chap_start 	="int",
    chap_end 	="int"

    ):
	rs = divlaw.divPart(content)
	chap = divlaw.getChapter(rs,part_index,chap_index)
	totalSec = chap['totalSec']
	if totalSec > 0:
		for i in range(0,totalSec):
			yield [
				id,
				part_index,
				chap_index,
				totalSec,
				i,
				chap['secs'][i]['start'],
				chap['secs'][i]['end'],
				chap['secs'][i]['name']
			]
	else :
		yield [
			id,
			part_index,
			chap_index,
			0,
			0,
			chap_start,
			chap_end,
			None
		]