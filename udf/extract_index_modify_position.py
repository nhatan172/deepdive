#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
    law_id ="text",
    position ="text",
    modified_law_id ="text",
    part_modify_index ="int",
    chap_modify_index ="int",
    sec_modify_index ="int",
    law_modify_index ="int",
    item_modify_index ="int",
    point_modify_index ="int",
    correct ="boolean" 
    :[])
def extract(
    law_id ="text",
    position ="text",
    modified_law_id ="text",
    part_modify_name ="text",
    chap_modify_name ="text",
    sec_modify_name ="text",
    law_modify_name ="text",
    item_modify_name ="text",
    point_modify_name ="text",
    part_name_sources ="text[]",
    part_index_sources ="int[]",
    chap_name_sources ="text[]",
    chap_index_sources ="int[]",
    sec_name_sources ="text[]",
    sec_index_sources ="int[]",
    law_name_sources ="text[]",
    law_index_sources ="int[]",
    item_name_sources ="text[]",
    item_index_sources ="int[]",
    point_name_sources ="text[]",
    point_index_sources ="int[]",
    ):

    part_modify_index = None
    chap_modify_index = None
    sec_modify_index = None
    law_modify_index = None
    item_modify_index = None
    point_modify_index = None
    length = len(chap_name_sources)
    correct = True

    if part_modify_name is not None:
        temp = handle_string.standardString(part_modify_name)
        for i in range(0, length) :
            if temp == handle_string.standardString(part_name_sources[i]) :
                part_modify_index = part_index_sources[i]
                break
    if chap_modify_name is not None:
        temp = handle_string.standardString(chap_modify_name)
        for i in range(0, length) :
            if temp == handle_string.standardString(chap_name_sources[i]) :
                chap_modify_index = chap_index_sources[i]
                part_modify_index = part_index_sources[i]
                break
    if sec_modify_name is not None:
        temp = handle_string.standardString(sec_modify_name)
        for i in range(0, length) :
            if temp == handle_string.standardString(sec_name_sources[i]) :
                chap_modify_index = chap_index_sources[i]
                part_modify_index = part_index_sources[i]
                sec_modify_index = sec_index_sources[i]
                break
    if law_modify_name is not None:
        find_out = False
        temp = handle_string.standardString(law_modify_name)
        for i in range(0, length) :
            if temp == handle_string.standardString(law_name_sources[i]) :
                chap_modify_index = chap_index_sources[i]
                part_modify_index = part_index_sources[i]
                sec_modify_index = sec_index_sources[i]
                law_modify_index = law_index_sources[i]
                find_out = True
                break
        if not find_out :
            correct = False
    if (item_modify_name is not None) and (law_modify_name is not None) and (point_modify_name is None):
        find_out = False
        tempLaw = handle_string.standardString(law_modify_name)
        for i in range(0, length) :
            if tempLaw == handle_string.standardString(law_name_sources[i]) :
                if item_modify_name == handle_string.standardString(item_name_sources[i]) :
                    chap_modify_index = chap_index_sources[i]
                    part_modify_index = part_index_sources[i]
                    sec_modify_index = sec_index_sources[i]
                    law_modify_index = law_index_sources[i]
                    item_modify_index = item_index_sources[i]
                    find_out = True
                    break
        if not find_out :
            correct = False
    if (item_modify_name is not None) and (law_modify_name is not None) and (point_modify_name is not None):
        find_out = False
        tempLaw = handle_string.standardString(law_modify_name)
        tempPoint = handle_string.standardString(law_modify_name)
        for i in range(0, length) :
            if tempLaw == handle_string.standardString(law_name_sources[i]) :
                if item_modify_name == handle_string.standardString(item_name_sources[i]) :
                    if point_modify_name == handle_string.standardString(point_name_sources[i]):
                        chap_modify_index = chap_index_sources[i]
                        part_modify_index = part_index_sources[i]
                        sec_modify_index = sec_index_sources[i]
                        law_modify_index = law_index_sources[i]
                        item_modify_index = item_index_sources[i]
                        point_modify_index = point_index_sources[i]
                        find_out = True
                        break
        if not find_out :
            correct = False
    if (part_modify_index is None) or (sec_modify_index is None) or (chap_modify_index is None) or (law_modify_index is None):
        correct = False
    if correct:
        yield [
            law_id ,
            position ,
            modified_law_id ,
            part_modify_index ,
            chap_modify_index ,
            sec_modify_index ,
            law_modify_index ,
            item_modify_index,
            point_modify_index ,
            correct
        ]