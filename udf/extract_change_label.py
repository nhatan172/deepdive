#!/usr/bin/env python
# -*- coding:utf8 -*-

from deepdive import *
import re
import handle_string

@tsv_extractor
@returns(lambda
        doc_id      = "text",
        label       ="boolean",
        change_in   = "text",
        numerical_symbol = "text"
    :[])
def extract(
        doc_id         = "text",
        sentence_text = "text"
    ):
    
    symbol = ["`","~","!","@","#","$","%","^","&","*","_","+","=","{","}","[","]","|","\\",":",";","<",">","?","(",")"]

    match = re.finditer(r"ban(\s|_)hành.*sửa(\s|_)đổi , bổ(\s|_)sung", sentence_text)

    if handle_string.lenIterator(match) == 0:
        yield[
        doc_id,
        False,
        "",
        "",
        ]
    else :
        for match1 in match :
            start_change =  match1.span()[1] + 1
            s = "của"
            a = []
            a.append(s)
            j = sentence_text.find(s,start_change)
            if j == -1 :
                j = start_change
            else :
                j+= 6
            start_change = j
            for k in range(j,len(sentence_text)):
                if sentence_text[k] in symbol:
                    if sentence_text[k-1] == ' ' or sentence_text[k-1] == ',':
                        end_change = k -2
                    else:
                        end_change = k -1
                    break
                elif k == len(sentence_text) - 1:
                    end_change = k +1
            
            yield[
            doc_id,
            True,
            sentence_text[start_change:end_change],
            handle_string.getNumericalSymbol(sentence_text),
            ]
            break