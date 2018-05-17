#!/usr/bin/env python
# coding=utf-8
from deepdive import *
import sys, re


def extract_mn_phrase(begin_index, pos_tags, tokens, max_distance):
    num_tokens = len(pos_tags)
    # find end of the M phrase
    end_index = begin_index + 1
    while end_index < num_tokens and pos_tags[end_index] == "M":
        end_index += 1
    end_index -= 1
    # find end of the M N(Nu) phrase
    end_index += 1
    if not (end_index < num_tokens and (pos_tags[end_index] == "N" or pos_tags[end_index] == "Nu")):
        end_index = -1
    # Check whether have M N(Nu) - M N(Nu) or not
    if end_index >= 0:
        for distance in range(1, max_distance + 1):
            if (end_index + distance + 1) < num_tokens and pos_tags[end_index + distance + 1] == "M":
                temp = extract_mn_phrase(end_index + distance + 1, pos_tags, tokens, max_distance)
                if temp >= 0:
                    end_index = temp
    return end_index


@tsv_extractor
@returns(lambda
                 mention_id="text",
                 mention_text="text",
                 mention_type="text",
                 law_id="text",
                 position ="text",
                 sentence_index =  "int",
                 begin_index="int",
                 end_index="int",
         : [])
def extract(
        doc_id="text",
        position="text",
        sentence_index = "int",
        sentence_text = "text",
        tokens="text[]",
        pos_tags="text[]",
):
    """
    Finds phrases that are continuous words tagged with PERSON.
    """
    # # Convert all to unicode
    # doc_id = doc_id.decode('utf8')
    # tokens = map(lambda token: token.decode('utf8'), tokens)
    # pos_tags = map(lambda tag: tag.decode('utf8'), pos_tags)

    # regexs
    # (example: 100.000 đồng)
    REGEX_MONEY = ur'^(?:\d+(?:[\.\s]\d{3})*|(?:[^\W\d]|\s)+)(?:\s+(?:triệu|tỷ))?((\s+đồng)|\s+đ)$'
    # (example: 100.000 đồng đến 200.000 đồng)
    REGEX_MONEY_RANGE = ur'^(?:\d+(?:[\.\s]\d{3})+|(?:[^\W\d]|\s)+)(?:\s+triệu)?((\s+đồng)|\s+đ)(?:[^\W\d]|\s)+(?:\d+(?:[\.\s]\d{3})+|(?:[^\W\d]|\s)+)(?:\s+triệu)?((\s+đồng)|\s+đ)$'
    # (example: 1 năm, 01 năm, 20 năm, hai mươi năm)
    REGEX_DATE = ur'^(?:\d{1,2}|(?:[^\W\d]|\s)+)\s+(?:năm|tháng)$'
    # (example: 01 năm đến 02 năm, một năm đến hai năm)
    REGEX_DATE_RANGE = ur'^(?:\d{1,2}|(?:[^\W\d]|\s)+)\s+(?:năm|tháng)(?:[^\W\d]|\s)+(?:\d{1,2}|(?:[^\W\d]|\s)+)\s+(?:năm|tháng)$'
    regex_money = re.compile(REGEX_MONEY, re.UNICODE)
    regex_money_range = re.compile(REGEX_MONEY_RANGE, re.UNICODE)
    regex_date = re.compile(REGEX_DATE, re.UNICODE)
    regex_date_range = re.compile(REGEX_DATE_RANGE, re.UNICODE)

    num_tokens = len(pos_tags)
    max_distance = 4
    i = 0
    while i < num_tokens:
        begin_index = None
        end_index = None
        mention_type = None
        if tokens[i] == 'tù_chung_thân' and (i + 1) < num_tokens:
            begin_index = i
            end_index = i
            mention_type = 'LIFE_IMPRISONMENT'
        elif tokens[i] == 'tử_hình' or tokens[i] == 'án_tử_hình' or tokens[i] == 'thi_hành_án_tử_hình' or tokens[i] == 'tử_hình':
            begin_index = i
            end_index = i
            mention_type = 'CAPITAL_PUNISHMENT'
        elif pos_tags[i] == "M":
            begin_index = i
            # find M N(Nu) (or M N(Nu) - M N(Nu))phrase
            end_index = extract_mn_phrase(begin_index, pos_tags, tokens, max_distance)
            if end_index >= 0:
                # Get candidate mention type
                phrase = " ".join(word for word in tokens[begin_index: end_index + 1])
                phrase = phrase.decode('utf8')
                if regex_money_range.search(phrase):
                    mention_type = 'MONEY_RANGE'
                elif regex_money.search(phrase):
                    mention_type = 'MONEY'
                elif regex_date_range.search(phrase):
                    mention_type = 'DATE_RANGE'
                elif regex_date.search(phrase):
                    mention_type = 'DATE'

        if begin_index and end_index and mention_type:
            i = end_index
            # generate a mention identifier
            mention_id = "{}_{}_{}_{}".format(doc_id, position, begin_index, end_index)
            mention_text = " ".join(map(lambda k: tokens[k].replace('\\', '\\\\'), range(begin_index, end_index + 1)))
            # Output a tuple for each founded phrase
            yield [
                mention_id,
                mention_text,
                mention_type,
                doc_id,
                position,
                sentence_index,
                begin_index,
                end_index,
            ]
        # Increase index
        i += 1
