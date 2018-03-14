#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string

@tsv_extractor
@returns(lambda
        organization_id       = "text",
        organization_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        begin_index      = "int",
        end_index        = "int",
    :[])
def extract(
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        begin_index      = "int",
        end_index        = "int", 
    ):

    num_tokens = len(tokens)
    first_indexes = (i for i in range(begin_index,end_index) if  handle_string.is_upper(tokens[i]))
    for i in first_indexes:
        last_index = i
        while last_index<= end_index and end_index<num_tokens:
            organization_id = "%s_%d_%d_%d" % (doc_id, sentence_index, i, last_index)
            if i == last_index :
                organization_text = handle_string.replace_underscore(tokens[i])
            else :
                organization_text = handle_string.replace_underscore(" ".join(map(lambda j: tokens[j], xrange(i, last_index+1))))
            yield  [
            organization_id,
            organization_text ,
            doc_id          ,
            sentence_index   ,
            i      ,
            last_index        ,
            ]
            last_index += 1
