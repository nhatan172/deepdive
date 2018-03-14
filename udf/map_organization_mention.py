#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string

@tsv_extractor
@returns(lambda
        mention_id       = "text",
        mention_text     = "text",
        doc_id           = "text",
        sentence_index   = "int",
        begin_index      = "int",
        end_index        = "int",
    :[])
def extract(
        doc_id         = "text",
        sentence_index = "int",
        tokens         = "text[]",
        pos_tags       = "text[]",
        ner_tags       = "text[]",
    ):
    
    num_tokens = len(ner_tags)
    # find all first indexes of series of tokens tagged as PERSON
    first_indexes = (i for i in xrange(num_tokens) if (pos_tags[i] == "N" or pos_tags[i] == "Np") and handle_string.is_upper(tokens[i]))
    last_end = -1
    for begin_index in first_indexes:
        if begin_index <= last_end :
            continue
        if(pos_tags[begin_index]=="Np"):
            end_index = begin_index + 1
            while end_index < num_tokens :
                if(pos_tags[end_index] == "N" or pos_tags[end_index] == "Np"):
                    end_index+=1
                elif(pos_tags[end_index] == "CC" and tokens[end_index] == "và"):
                    a = handle_string.find_tag_in(pos_tags,end_index,num_tokens-1,"N")
                    b = handle_string.find_tag_in(pos_tags,end_index,num_tokens-1,"Np")
                    if a != b and (a == -1 or b == -1):
                        end_index = max(a,b)
                    elif a ==b and  a == -1:
                        end_index -=1
                        break
                    else :
                        end_index = min(a,b)
                else :
                    break
            end_index = handle_string.re_index(pos_tags,tokens,begin_index, end_index)
            if end_index == begin_index :
                if handle_string.len_token(tokens[begin_index]) == 1:
                    continue
                mention_text = tokens[begin_index]
            else :
                mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
            mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
            last_end = end_index
            yield [
                mention_id,
                mention_text,
                doc_id,
                sentence_index,
                begin_index,
                end_index,
            ]
            continue
        limit_index = min((begin_index + 11 ), (num_tokens -1))
        limit_index = min(limit_index ,handle_string.index_of_strange(tokens,pos_tags,begin_index,num_tokens-1) )
        end_index = begin_index + 1
        predict = handle_string.find_tag_in(pos_tags,end_index,limit_index,"M")
        if(predict != -1 and pos_tags[predict-1] == "N"):
            end_index = predict
            end_index = handle_string.re_index(pos_tags,tokens,begin_index, end_index)
            if end_index == begin_index :
                    continue
            else :
                mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
            mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
            last_end = end_index
            yield [
                mention_id,
                mention_text,
                doc_id,
                sentence_index,
                begin_index,
                end_index,
            ]
            continue
        end_index = handle_string.string_of_nouns(pos_tags,tokens,begin_index,end_index)+1
        while end_index <= limit_index :                
            if (tokens[end_index] == "và" and (end_index + 1 < num_tokens)):
                end_index += 1
                continue
            else :
                break
            if(pos_tags[end_index] == "V"):
                end_index += 1
                continue
            if(pos_tags[end_index] == "A"):
                if(pos_tags[end_index+1] == "N" or pos_tags[end_index+1]== "Np"):
                    end_index = handle_string.string_of_nouns(pos_tags,tokens,begin_index,end_index)+1
                    break
                else:
                    end_index +=1
                    break
            if(pos_tags[end_index]== "N" or pos_tags[end_index] == "Np"):
                end_index = handle_string.string_of_nouns(pos_tags,tokens,begin_index,end_index)+1
                continue
            if(pos_tags[end_index] == ","):
                end_index += 1
                continue
            if(pos_tags[end_index] == "-"):
                end_index += 1
                continue
        end_index -= 1
        end_index = handle_string.re_index(pos_tags,tokens,begin_index, end_index)
        mention_id = "%s_%d_%d_%d" % (doc_id, sentence_index, begin_index, end_index)
        if end_index == begin_index :
            sum = 0
            for i in range(0,len(tokens[begin_index])):
                if tokens[begin_index][i] == '_':
                    sum += 1
            if sum == 0:
                continue
            mention_text = tokens[begin_index]
        else :
            mention_text = " ".join(map(lambda i: tokens[i], xrange(begin_index, end_index + 1)))
        last_end = end_index
        yield [
            mention_id,
            mention_text,
            doc_id,
            sentence_index,
            begin_index,
            end_index,
        ]
         