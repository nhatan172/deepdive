#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw

@tsv_extractor
@returns(lambda
        law_id         ="text",
        part_index     ="int",
        chap_index     ="int",
        sec_index      ="int",
        law_index      ="int",
        totalItem      ="int",
        item_index     ="int",
        item_start     ="int",
        item_end       ="int",
        item_name      ="text",
        item_content   ="text",
        title_end       ="int",
    :[])
def extract(
        id          ="text",
        content     ="text",
        part_index  ="int",
        chap_index  ="int",
        sec_index   ="int",
        law_index   ="int",
        law_start   ="int",
        law_end     ="int",
    ):

    result = divlaw.newDivItem(content,law_start)
    totalItem = result[1]
    if totalItem > 0:
        for i in range(0, totalItem):
            start = result[0][i]['start']
            end = result[0][i]['end']
            title_end = end
            item_content = result[0][i]['content']
            list_point = divlaw.newDivPoint(item_content,start)
            if list_point[1]> 0:
                title_end = list_point[0][0]['start']
            yield [
                id,
                part_index,
                chap_index,
                sec_index,
                law_index,
                totalItem,
                i,
                start,
                end,
                result[0][i]['name'],
                item_content,
                title_end
            ]
    else :
        yield [
            id,
            part_index,
            chap_index,
            sec_index,
            law_index,
            0,
            0,
            law_start,
            law_end,
            None,
            None,
            law_end
        ]
