#!/usr/bin/env python
# coding=utf-8
import codecs
import re

def get_left_window(start_idx, tokens, WINDOW_SIZE):
    return tokens[max(0, start_idx - WINDOW_SIZE):start_idx]

def get_right_window(end_idx, tokens, WINDOW_SIZE):
    return tokens[end_idx + 1: min(end_idx + WINDOW_SIZE + 1, len(tokens))]

# Return the start and end indexes of all subsets of words in the sentence
# sent, with size at most max_phrase_length
def get_all_phrases_in_sentence(tokens, max_phrase_length):
    for start in range(len(tokens)):
        for end in reversed(range(start, min(
                len(tokens), start + max_phrase_length))):
            yield " ".join(word for word in tokens[start:end + 1])

def get_list_phrase_contains_mention(m_begin_index, m_end_index, tokens):
    num_tokens = len(tokens)
    phrase_begin_index = m_begin_index
    phrase_end_index = m_end_index
    regex = re.compile(ur'\w', re.UNICODE)
    while phrase_begin_index > 0:
        if phrase_begin_index >= 2 and tokens[phrase_begin_index -1 ] == ")" and regex.search(tokens[phrase_begin_index - 2]):
            break
        phrase_begin_index -= 1
    while phrase_end_index < num_tokens:
        if phrase_end_index + 1 < num_tokens and (tokens[phrase_end_index + 1] == ";" or tokens[phrase_end_index + 1] == "."):
            break
        phrase_end_index += 1
    return (phrase_begin_index, phrase_end_index)



# tokens = ['a' ,')' ,'Phạt' ,'cảnh_cáo', ';','đ', ')', 'Phạt', 'tiền', 'đến', '10.000.000', 'đồng', ';']
# tokens1 = ['Phạt' ,'cảnh_cáo', 'Phạt', 'tiền', 'đến', '10.000.000', 'đồng', 'hay']
#
# print get_list_phrase_contains_mention(5, 6, tokens1)