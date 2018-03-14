#!/usr/bin/env python
from deepdive import *
import random
from collections import namedtuple
import handle_string

ORGLabel = namedtuple('OrganizationLabel', 'organization_id,label, type')

@tsv_extractor
@returns(lambda
        organization_id   = "text",
        label   = "int",
        rule_id = "text",
    :[])
# heuristic rules for finding positive/negative examples of spouse relationship mentions
def supervise(
    organization_id ="text",
    begin_index     ="int",
    end_index       ="int",
    doc_id          ="text",
    sentence_index  ="int",
    tokens          ="text[]", 
    pos_tags    ="text[]", 
    ner_tags        ="text[]",
    ):
    
    
    org = ORGLabel(organization_id=organization_id, label=None, type=None)

    if (handle_string.len_token(tokens[begin_index]) == 1) and (begin_index == end_index):
        yield org._replace(label=-1, type='tokens:to_short')

    for i in range(begin_index,end_index+1):
        if pos_tags[i]=="A" :
            if pos_tags[i+1] == "V":
                yield org._replace(label=-1, type='pos_tag_seq:a_v')
                break

    for i in range(begin_index,end_index+1):
        if ner_tags[i] == "POS" :
            yield org._replace(label=-1, type='ner_tag:pos')
            break