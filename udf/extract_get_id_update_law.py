#!/usr/bin/env python
# -*- coding:utf8 -*-
from deepdive import *
import re
import ddlib

@tsv_extractor
@returns(lambda
    doc_id	= "text",
    :[])
def extract(
    doc_id = "text",
    doc_content = "text",
    name_title = "text",
    numerical_symbol = "text",
    ):
	if(numerical_symbol == doc_content):
		yield[
			doc_id,
		]
	elif(doc_content == name_title):
		yield[
			doc_id,
		]