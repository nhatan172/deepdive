#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import ddlib
import os,sys
from util.processer import  *

@tsv_extractor
@returns(lambda
        organization_id   = "text",
                feature = "text",
         :[])
def extract(
        organization_id          = "text",
        begin_index              = "int",
        end_index   = "int",
        doc_id         = "text",
        sentence_index     = "int",
        tokens         = "text[]",
        pos_tags       = "text[]",
        dep_types      = "text[]",
        dep_heads    = "int[]",
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
                dep_par=dep_heads[i] - 1,  # Note that as stored from CoreNLP 0 is ROOT, but for DDLIB -1 is ROOT
                dep_label=dep_types[i]))
        ####
        org_span = ddlib.Span(begin_word_id=begin_index, length=(end_index - begin_index +1))
        for feature in ddlib.get_generic_features_mention(sent, org_span):
                yield [organization_id, feature]
