#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw

@tsv_extractor
@returns(lambda
        law_id         ="text",
		totalPart      ="int",
    	part_index     ="int",
   		part_start     ="int",
    	part_end       ="int",
    	part_name	="text"
    :[])
def extract(
        id         = "text",
        content = "text"
    ):

	a = divlaw.divPart(content)
	totalPart = divlaw.getTotalPart(a)
	if totalPart > 0:
		for i in range(0,totalPart):
			yield [
				id,
				totalPart,
				i,
				divlaw.getPart(a,i)['start'],
				divlaw.getPart(a,i)['end'],
				divlaw.getPart(a,i)['name'],
			]
	else :
		yield [
			id,
			0,
			0,
			divlaw.getPart(a,0)['start'],
			divlaw.getPart(a,0)['end'],
			None,
		]