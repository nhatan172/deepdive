#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw
import handle_string
import ddlib
import os,sys
from util.processer import  *


@tsv_extractor
@returns(lambda
    id = "text",
    feature ="text",
    :[])
def extract(
		mention_id  ="text",
        begin_exp ="int",
        end_exp   ="int",
        begin_explain ="int",
        end_explain  ="int",
        tokens       ="text[]",
        pos_tags      ="text[]"
    ):
	
    sent = []
    for i,t in enumerate(tokens):
        sent.append(ddlib.Word(
            begin_char_offset=None,
            end_char_offset=None,
            word=t,
            lemma=tokens[i],
            pos=pos_tags[i],
            ner=None,
            dep_par=-1,  # Note that as stored from CoreNLP 0 is ROOT, but for DDLIB -1 is ROOT
            dep_label=None))

    # Create DDLIB Spans for the two person mentions
    p1_span = ddlib.Span(begin_word_id=begin_exp, length=(end_exp - begin_exp +1))
    p2_span = ddlib.Span(begin_word_id=begin_explain, length=(end_explain - begin_explain + 1))

    # Generate the generic features using DDLIB
    for feature in ddlib.get_seq_definition_features(sent, p1_span, p2_span):
        yield [mention_id, feature]
