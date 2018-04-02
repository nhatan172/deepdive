#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import re
from collections import namedtuple
from util.processer import *
import os, sys
import divlaw
import handle_string

CrimeLabel = namedtuple('CrimeLabel', 'p_id, label, type')


@tsv_extractor
@returns(lambda
				 mention_id="text",
				 label="int",
				 rule_id="text",
		 : [])
# heuristic rules for finding positive/negative examples of spouse relationship mentions
def supervise(
		mention_id="text",
		mention_begin_index="int", 
		mention_end_index="int",
		doc_id="text", 
		position = "text",
		sentence_index="int", 
		sentence_text="text",
		tokens="text[]", 
		pos_tags="text[]",
		label = "int"
):
	# # Read keywords from file
	# APP_HOME = os.environ['APP_HOME']
	# kw_non_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_non_crime.txt", 'r').readlines())
	# kw_legal_penalty = map(lambda word: word.strip(), open(APP_HOME + "/udf/dicts/kw_crime.txt", 'r').readlines())

	# Non penalty signals on the left of candidate mention
	# NON_PENAL_SIGNALS_LEFT = frozenset(kw_non_legal_penalty)
	# Penalty signals on the left of candidate mention
	# PENAL_SIGNALS_LEFT = frozenset(kw_legal_penalty)

	crime = CrimeLabel(mention_id=mention_id, label=None, type=None)

	# Negative rules
	if label < 0:
		yield crime._replace(label=1, type="neg:legal_penalty_false")



	# Positive rules
	# Ruile 1:
	if label > 0:
		yield crime._replace(label=1, type="pos:legal_penalty_true")