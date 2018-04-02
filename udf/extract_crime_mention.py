#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import sys, re


def extract_phrase_list(tokens, begin_list):
    num_tokens = len(tokens)
    i = begin_list
    while i < num_tokens:
        if i + 3 < num_tokens: begin_phrase = i + 2
        else: break
        j = begin_phrase + 1
        while j < num_tokens:
            if (tokens[j] == ";" and (j + 2) < num_tokens and re.search("\w", tokens[j + 1]) and tokens[j + 2] == ")") or j == num_tokens - 1:
                end_phrase = j - 1
                i = end_phrase + 2
                yield (begin_phrase, end_phrase)
                break
            else: j += 1

def is_phrase_list_block(tokens):
    num_tokens = len(tokens)
    i = 0
    while i < num_tokens:
        if (i + 2) < num_tokens and tokens[i] == ":" and re.search("\w", tokens[i + 1]) and tokens[i + 2] == ")":
            return True
        else: i += 1
    return False
## lấy string nếu ngay đằng trước nó là mức phạt
# get_string(tokens, penalty_end_index, 1) in KW1:
def get_string(tokens, start, length):
    if (start + length) < len(tokens):
        return " ".join(word for word in tokens[start + 1: start + length + 1])
#lấy string trong trường hợp luật hình sự#
## lấy string nếu hành vi năm ở giưa câu
def get_crime_string(tokens, key, length):
    num_tokens = len(tokens)
    start = 0
    temp = 0
    for temp in range(0,num_tokens):
        if( (start + length) < num_tokens and tokens[start:start+length-1] in key):
            return " ".join(word for word in tokens[start +1: start + length +1])
        else:
            start = start + 1
    return None

def find_character(tokens, start, character):
    i = start + 1
    num_tokens = len(tokens)
    while i < num_tokens:
        if tokens[i] == character: return i
        else: i += 1

# def return_result(begin_phrase, law_id, position, num_tokens, penalty_id):
#     if begin_phrase:
#         if is_phrase_list_block(tokens): end_phrase = find_character(tokens, begin_phrase, ";") - 1
#         else:
#             if tokens[num_tokens - 1] == ".": end_phrase = num_tokens - 2
#             else: end_phrase = num_tokens -1

#     if begin_phrase and end_phrase:
#         begin_index = begin_phrase
#         end_index = end_phrase
#         # generate a mention identifier
#         mention_id = "{}_{}_{}_{}".format(law_id, position, begin_index, end_index)
#         mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
#         mention_type = "IN_ONE_SENTENCE"
#         associated_penalty_id = penalty_id
#         # print >> sys.stderr, "MENTION TYPE: {} AND MENTION ID: {}".format(mention_type, mention_id)
#         # Output a tuple for each founded phrase
#         yield [
#             mention_id,
#             mention_text,
#             mention_type,
#             law_id,
#             position,
#             begin_index,
#             end_index,
#             associated_penalty_id
#         ]
@tsv_extractor
@returns(lambda
            mention_id = "text",
            mention_text = "text",
            mention_type = "text",
            law_id = "text",
            position = "text",
            sentence_index = "int",
            begin_index = "int",
            end_index = "int",
            associated_penalty_id = "text"
         : [])
def extract(
        law_id = "text",
        position = "text",
        sentence_index = "int",
        tokens = "text[]",
        pos_tags = "text[]",
        penalty_id = "text",
        penalty_begin_index = "int",
        penalty_end_index = "int"
):
    num_tokens = len(tokens)
    is_passed = True
    check = 0

    # [PENALTY] ... : a ) ...
    i = penalty_end_index + 1
    phrase_list = None
    if is_phrase_list_block(tokens):
        phrase_list = extract_phrase_list(tokens, i + 1)
        is_passed = False

    if phrase_list:
        for begin, end in phrase_list:
            begin_index = begin
            end_index = end
            # generate a mention identifier
            mention_id = "{}_{}_{}_{}".format(law_id, position, begin_index, end_index)
            mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
            mention_type = "PHRASE_LIST"
            associated_penalty_id = penalty_id
            # print >> sys.stderr, "MENTION TYPE: {} AND MENTION ID: {} AND MENTION_TEXT: {}".format(mention_type, mention_id, mention_text)
            # Output a tuple for each founded phrase
            yield [
                mention_id,
                mention_text,
                mention_type,
                law_id,
                position,
                sentence_index,
                begin_index,
                end_index,
                associated_penalty_id
            ]

    # [PENALTY] ... (nếu | đối_với_hành_vi| đối_với trường_hợp | đối_với | trong trường_hợp | đối_với_hành_vi_vi_phạm)
    KW1 = ["đối_với_hành_vi","nếu", "đối_với","đối_với_hành_vi_vi_phạm", "đối_với_hành_vi điều_khiển", "đối_với_hành_vi_vi_phạm"]
    KW2 = ["đối_với trường_hợp", "trong trường_hợp"]
    KW3 = ["bị_phạt"]
    KW4 = ["sau đây"]
    if is_passed:
        begin_phrase = None
        end_phrase = None
        if get_string(tokens, penalty_end_index, 2) in KW2:
            begin_phrase = penalty_end_index + 3
            # return_result(begin_phrase,law_id,position, num_tokens, penalty_id)
        elif get_string(tokens, penalty_end_index, 1) in KW1:
            begin_phrase = penalty_end_index + 2
            # return_result(begin_phrase,law_id,position, num_tokens, penalty_id)
        elif get_crime_string(tokens, KW2, 2) in KW2:
            begin_phrase = get_crime_string(tokens, 2)
            # return_result(begin_phrase,law_id,position, num_tokens, penalty_id)
        elif get_crime_string(tokens, KW1, 1) in KW1:
            begin_phrase = get_crime_string(tokens, 1)
            # return_result(begin_phrase,law_id,position, num_tokens, penalty_id)
        elif (KW3[0] in tokens[0:penalty_begin_index-1]) and (penalty_end_index+1 < num_tokens):
            # kiểm tra xem có phải là list các hành vi hay không ?
            if "sau_đây" in tokens[0:num_tokens]:
                begin_phrase = penalty_end_index + 3
                end_phrase = len(tokens) - 1 
            else:
                begin_phrase = 0
                end_phrase = penalty_begin_index - 1
            check = 1
            # begin_index = begin_phrase
            # end_index = end_phrase
            # # generate a mention identifier
            # mention_id = "{}_{}_{}_{}".format(law_id, position, begin_index, end_index)
            # mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(0, penalty_end_index + 1)))
            # mention_type = "IN_ONE_SENTENCE"
            # associated_penalty_id = penalty_id
            # # print >> sys.stderr, "MENTION TYPE: {} AND MENTION ID: {}".format(mention_type, mention_id)
            # # Output a tuple for each founded phrase
            # # yield [
            # #     mention_id,
            # #     mention_text,
            # #     mention_type,
            # #     law_id,
            # #     position,
            # #     begin_index,
            # #     end_index,
            # #     associated_penalty_id
            # # ]
            # yield[
            #     None,
            #     None,
            #     None,
            #     None,
            #     mention_text,
            #     begin_phrase,
            #     end_phrase,
            #     None
            # ]

        if begin_phrase and check == 0 :
            if is_phrase_list_block(tokens): end_phrase = find_character(tokens, begin_phrase, ";") - 1
            else:
                if tokens[num_tokens - 1] == ".": end_phrase = num_tokens - 2
                else: end_phrase = num_tokens -1

        if begin_phrase and end_phrase:
            begin_index = begin_phrase
            end_index = end_phrase
            # generate a mention identifier
            mention_id = "{}_{}_{}_{}".format(law_id, position, begin_index, end_index)
            mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
            mention_type = "IN_ONE_SENTENCE"
            associated_penalty_id = penalty_id
            # print >> sys.stderr, "MENTION TYPE: {} AND MENTION ID: {}".format(mention_type, mention_id)
            # Output a tuple for each founded phrase
            yield [
                mention_id,
                mention_text,
                mention_type,
                law_id,
                position,
                sentence_index,
                begin_index,
                end_index,
                associated_penalty_id
            ]
