#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
        doc_id      = "text",
        header_text   = "text"
    :[])
def extract(
        doc_id         = "text",
        content = "text" 
    ):
    
    a = divlaw.getHeader(content)
    yield [
        doc_id,
        content[0:a],
    ]

