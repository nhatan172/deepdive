#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw
import handle_string
import numpy
def add_underline(string):
    return string.replace(" ","_")
def compare(a,b):
    if len(a) > len(b):
        return -1
    elif len(a) < len(b):
        return 1
    else :
        return 0
@tsv_extractor
@returns(lambda
    id ="text",
    cont = "text",
    :[])

def extract(
    doc_id ="text",
    content="text",
    phrases = "text[]",
    ):

    content = content.replace('*',' ')
    content = content.replace('_',' ')
    if phrases is None or len(phrases) == 0:  
        yield [
            doc_id,
            content
        ]
    else :
        a = sorted(phrases,cmp = compare)
        for i in a:
            content = content.replace(i,add_underline(i))  
        yield [
            doc_id,
            content
        ]