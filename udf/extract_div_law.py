#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw

@tsv_extractor
@returns(lambda
        doc_id      = "text",
        content       ="text"
    :[])
def extract(
        doc_id         = "text",
        law_structor = "text[]"
    ):
    
    a = divlaw.divPart(content)
    yield[
    doc_id,
    a,
    ]