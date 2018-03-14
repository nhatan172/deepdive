#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string
import divlaw
def lenIterator(list):
    sum = 0
    for i in list :
        sum += 1
    return sum
def get_numerical_symbol(title):
    get_title1 = re.search(r'(của\s.*)\s(đã được|được)',title)
    get_title  = re.search(r'([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*))',title,re.M|re.I)
    # get_id = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)+',get_content.group())
    # get_title1 = re.search(r'([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)\s(đã được))|([0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)\s(được))',title)
    if(get_title1 is not None):
        number = re.search(r'[0-9]+(/[0-9]+)*((/|-)[A-ZĐ]+[0-9]*)',get_title1.group())
        if(number is not None):
            return number.group()
    elif ((get_title is not None) and (get_title1 is None)):
        return get_title.group()
    else :
        return None
@tsv_extractor
@returns(lambda
    law_id ="text",
    part_index ="int",
    chap_index ="int",
    sec_index ="int",
    law_index ="int",
    item_index ="int",
    point_index ="int",
    numerical_sybol  ="text",
    title   = "text",
    content = "text",
    location_content = "int",
    count = "int"
    :[])
def extract(
    law_id = "text",
    totalLaw = "int",
    law_content = "text",
    totalItem = "int",
    item_content =  "text",
    totalpoint = "int",
    point_content = "text",
    part_index ="int",
    chap_index ="int",
    sec_index ="int",
    law_index ="int",
    item_index ="int",
    point_index ="int"
    ):
    # get_type = re.search(r'[s|S]ửa đổi[\s|\,]*(bổ sung)*',name_title)
    # if(get_type is not None):
    # text = 'như sau: “1. _Hoạt động giao thông đường thủy nội địa_ gồm hoạt động của người, phương tiện tham gia giao thông vận tải trên đường thủy nội địa'
    p =re.compile(r'\:(\s|\\n|\*|\_|\#)*(\“|\")')
    numerical_sybol = None
    done = 0
    end = 0
    if(totalpoint > 0 ):
        temp = p.finditer(point_content,re.DOTALL)
        if(lenIterator(temp) > 0 ):
            for get_content in p.finditer(point_content):
                start_point = get_content.start()
                leng = len(point_content)
                title_point = point_content[0:start_point]
                numerical_sybol_point = get_numerical_symbol(title_point)
                if(numerical_sybol_point is None):
                    done = 2
                    start = start_point
                    title = title_point
                    content = point_content
                elif(numerical_sybol is not None):
                    done = 3
                    match = re.finditer(r"(\\n(\s|\_|\.|\*|\#)*\“(.(?!\“|\”))+.{2})|(\\n(\s|\_|\.|\*|\#)*\"(.(?!\"))+.{2})", point_content,re.DOTALL)
                    count = divlaw.lenIterator(match)
                    yield[
                        law_id,
                        part_index ,
                        chap_index ,
                        sec_index ,
                        law_index ,
                        item_index ,
                        point_index,
                        numerical_sybol_point,
                        title_point,
                        point_content,
                        start_point,
                        count
                    ]
                break
        else :
            end = 1        
    if(((totalItem > 0 and done == 0 ) or ( totalItem > 0 and done ==2 )) and end != 1):
        temp = p.finditer(item_content,re.DOTALL)
        if(lenIterator(temp) > 0 ):
            for get_content in p.finditer(item_content):
                if(done == 0 ):
                    start_item = get_content.start()
                    leng = len(item_content)
                    title_item = item_content[0:start_item]
                    numerical_sybol_item = get_numerical_symbol(title_item)
                    if(numerical_sybol_item is None):
                        done = 4
                        start = start_item
                        title = title_item
                        content = item_content
                    if(numerical_sybol_item is not None):
                        done = 5
                        match = re.finditer(r"(\\n(\s|\_|\.|\*|\#)*\“(.(?!\“|\”))+.{2})|(\\n(\s|\_|\.|\*|\#)*\"(.(?!\"))+.{2})", item_content,re.DOTALL)
                        count = divlaw.lenIterator(match)
                        yield[
                            law_id,
                            part_index ,
                            chap_index ,
                            sec_index ,
                            law_index ,
                            item_index ,
                            point_index,
                            numerical_sybol_item,
                            title_item,
                            item_content,
                            start_item,
                            count
                        ]
                if(done == 2 ):
                    start_item = get_content.start()
                    leng = len(item_content)
                    title_item = item_content[0:start_item]
                    content = item_content
                    numerical_sybol_item = get_numerical_symbol(title_item)
                    if(numerical_sybol_item is not None):
                        numerical_sybol = numerical_sybol_item
                        done = 6
                break
        else:
            end = 1
    if(((totalLaw > 0  and done == 0) or (totalLaw > 0 and done == 4) or(totalLaw > 0 and done == 2)) and end != 1):
        temp = p.finditer(law_content,re.DOTALL)
        if(lenIterator(temp)>0):
            for get_content in p.finditer(law_content):
                if(done == 0):
                    start_law = get_content.start()
                    leng = len(law_content)
                    title_law = law_content[0:start_law]
                    numerical_sybol = get_numerical_symbol(title_law)
                    match = re.finditer(r"(\\n(\s|\_|\.|\*|\#)*\“(.(?!\“|\”))+.{2})|(\\n(\s|\_|\.|\*|\#)*\"(.(?!\"))+.{2})", law_content,re.DOTALL)
                    count = divlaw.lenIterator(match)
                    yield[
                        law_id,
                        part_index ,
                        chap_index ,
                        sec_index ,
                        law_index ,
                        item_index ,
                        point_index,
                        numerical_sybol,
                        title_law,
                        law_content,
                        start_law,
                        count
                    ]
                if(done == 2 or done == 4):
                    start_law = get_content.start()
                    title_law = law_content[0:start_law]
                    numerical_sybol = get_numerical_symbol(title_law)
                    if(numerical_sybol is not None):
                        done = 7
                break
        else :
            end =1
    if(done == 2 or done == 4 or done ==6 or done == 7 ):
        match = re.finditer(r"(\\n(\s|\_|\.|\*|\#)*\“(.(?!\“|\”))+.{2})|(\\n(\s|\_|\.|\*|\#)*\"(.(?!\"))+.{2})", content,re.DOTALL)
        count = divlaw.lenIterator(match)
        yield[
            law_id,
            part_index ,
            chap_index ,
            sec_index ,
            law_index ,
            item_index ,
            point_index,
            numerical_sybol,
            title,
            content,
            start,
            count
        ]
    done = 0
    end =0
