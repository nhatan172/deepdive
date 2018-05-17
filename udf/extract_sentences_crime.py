#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import divlaw
from pyvi.pyvi import ViPosTagger, ViTokenizer
import handle_string

@tsv_extractor
@returns(lambda
    law_id         ="text",
    position = "text",
    sentence_index = "int",
    sentence_text = "text",
    tokens = "text[]",
    pos_tags = "text[]",
    parent_post = "text"
    :[])

def extract(
    id 			="text",
    content 	="text",
    part_index  ="int",
    chap_index 	="int",
    sec_index 	="int",
    law_index 	="int",
    item_index = 'int',
    point_index = 'int',
    start_index ="int",
    end_index   ="int",
    ):
    sent_index = 0
    parent_index = 0
    for s in content[start_index:end_index].split("\\n"):
        if s != "":
            it = re.finditer(r"(.(?!(\.\s)))+.{2}",s,re.I)
            lent = divlaw.lenIterator(it)
            it = re.finditer(r"(.(?!(\.\s)))+.{2}",s,re.I)
            listIndex = []
            position = 0
            if item_index is None :
                position = "{}_{}_{}_{}_0_0".format(part_index+1,chap_index+1,sec_index+1,law_index+1)
                parent_index = None
            elif point_index is None :
                position = "{}_{}_{}_{}_{}_0".format(part_index+1,chap_index+1,sec_index+1,law_index+1,item_index +1)
                parent_index = "{}_{}_{}_{}_{}_0".format(part_index+1,chap_index+1,sec_index+1,law_index+1,0)
            else :
                position = "{}_{}_{}_{}_{}_{}".format(part_index+1,chap_index+1,sec_index+1,law_index+1, item_index + 1, point_index + 1)
                parent_index = "{}_{}_{}_{}_{}_{}".format(part_index+1,chap_index+1,sec_index+1,law_index+1, item_index + 1, 0)
            if lent > 0:
                for i in it :
                    listIndex.append(i.start())
                if (len(s) - i.end()) > 5 :
                    listIndex.append(i.end())
                    lent += 1
            else :
                listIndex.append(0)
            for j in range(0,lent) :
                if (j != (lent - 1)) :
                    string = handle_string.to_unicode(s[listIndex[j]:listIndex[j+1]])
                    string = string.replace("\\",'')
                    tokenize = ViPosTagger.postagging(ViTokenizer.tokenize(string))[0] 
                    pos_tag = ViPosTagger.postagging(ViTokenizer.tokenize(string))[1]
                    tk = []
                    for token in tokenize :
                        token = token.encode('utf-8')
                        tk.append(token)
                    yield [
                        id,
                        position,
                        sent_index,
                        " ".join(tk),
                        tk,
                        pos_tag,
                        parent_index
                    ]
                    sent_index += 1
                else :
                    string = handle_string.to_unicode(s[listIndex[j]:])
                    string = string.replace("\\",'')
                    tokenize =  ViPosTagger.postagging(ViTokenizer.tokenize(string))[0]
                    pos_tag = ViPosTagger.postagging(ViTokenizer.tokenize(string))[1]
                    tk = []
                    for token in tokenize :
                        token = token.encode('utf-8')
                        tk.append(token)
                    yield [
                        id,
                        position,
                        sent_index,
                        " ".join(tk),
                        tk,
                        pos_tag,
                        parent_index
                    ]
                    sent_index+=1