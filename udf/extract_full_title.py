#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
    law_id ="text",
    full_text_title  ="text" 
    :[])
def extract(
    doc_id = "text",
    type_doc = "text",
    title = "text"
    ):
    
    temp = type_doc + " " + title
    temp = handle_string.to_unicode(temp)
    temp = temp.lower()
    temp = temp.encode('utf-8')
    yield [
        doc_id,
        temp,
    ]

    