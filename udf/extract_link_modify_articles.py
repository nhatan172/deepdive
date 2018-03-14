#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
    doc_id = "text",
    position = "text",
    modify_doc_id = "text"  
    :[])
def extract(
    doc_id =  "text",
    position = "text", 
    modify_title = "text",
    released_date = "text",
    doc_id_resources = "text[]",
    doc_title_resources = "text[]",
    doc_symbol_resources = "text[]",
    type_doc = "text[]",
    released_date_resources ="text[]" 
    ):
    
    pattern = re.compile(r"[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+")
    m = pattern.match(modify_title)
    if (m is not None):
        symbol = m.group(0)
        available = False
        for i in range(0,len(doc_symbol_resources)):
            if doc_symbol_resources[i] == symbol :
                available = True
                yield [
                    doc_id,
                    position,
                    doc_id_resources[i],
                ]
        if available == False :
            yield [
                doc_id,
                position,
                "NA",
            ]
    else :
        available = False
        tempReal = handle_string.to_unicode(modify_title)
        for i in range(0,len(doc_title_resources)):
            temp = type_doc[i] + " " + doc_title_resources[i]
            tempU = handle_string.to_unicode(temp)
            if tempU.strip == tempReal.strip :
                if released_date is not None :
                    if (released_date_resources[i] == released_date) :
                        available = True
                        yield [
                            doc_id,
                            position,
                            doc_id_resources[i],
                        ]
                        break
                else :
                    yield [
                            doc_id,
                            position,
                            doc_id_resources[i],
                        ]
                    break
        if available == False :
            yield [
                doc_id,
                position,
                "NA",
            ]


