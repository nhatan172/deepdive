#!/usr/bin/env python
# -*- coding:utf8 -*-

def to_unicode(string, encoding = 'utf-8'):
    if isinstance(string, basestring):
        if not isinstance(string, unicode):
            string = unicode(string, encoding)
    return string
def is_upper(string):
    s = to_unicode(string)
    symbol = [".", "\\" ,"/", "+","*","?","%","_","<",">",",",":",";","\'","\"","[","]","|","{","}"]
    if string[0] in symbol:
        False
    return (s[0].isupper() and s[0].isalpha())
#all return at atleast index still be comfortable for ORG
#end_index follow limit of index (not length)

def len_token(string):
    sum = 0
    for i in range(0,len(string)):
        if(string[i]=='_'): 
            sum+=1
    sum += 1
    return sum
def find_tag_in(pos_tags,begin_index,end_index,search_tag):
    while(begin_index<=end_index):
        if(pos_tags[begin_index] == search_tag):
            return begin_index
        else :
            begin_index += 1
    return -1

def string_of_nouns(pos_tags,tokens,begin_index,end_index):
    symbol = [".", "\\" ,"/", "+","*","?","%","_","<",">",",",":",";","\'","\"","[","]","|","{","}"]
    while(begin_index<=end_index):
        if(pos_tags[begin_index] == "N" or pos_tags[begin_index] == "Np" ):
            if (tokens[begin_index][0] in symbol):
                return begin_index - 1
            begin_index += 1
        elif pos_tags[begin_index] == ",":
            predict = find_tag_in(pos_tags,begin_index+1,end_index,"N")
            if(predict == -1):
                return begin_index -1
            begin_index = predict
        else :
            return begin_index - 1 
    return begin_index
def index_of_strange(tokens,pos_tags,begin_index,end_index):
    need_tags = ["N","Np","V","A", ",","M","-"]
    symbol = [".", "\\" ,"/", "+","*","?","%"]
    while(begin_index<=end_index):
        if(pos_tags[begin_index] == "CC" and  tokens[begin_index] == "và"):
            begin_index += 1
        elif (pos_tags[begin_index] in need_tags) and  not(tokens[begin_index][0] in symbol) :
            begin_index += 1
        else :
            return begin_index -1
    return begin_index
def re_index(pos_tags,tokens,begin_index, end_index):
    need_tags = ["N","Np","V","A","M"]
    symbol = [".", "\\" ,"/", "+","*","?","%","_","<",">",",",":",";","\'","\"","[","]","|","{","}"]
    while begin_index<end_index:
        if (tokens[end_index][0] in symbol) or not(pos_tags[end_index] in need_tags) :
            end_index -= 1
        else:
            break
    return end_index
def replace_underscore(string):
	s = to_unicode(string)
	s = s.lower()
	s = s.replace("_"," ")
	s2 = s.encode('utf-8')
	return s2
def find_contain(string, array):
    s = to_unicode(string)
    s = s.lower()
    for i in array:
        s2 = to_unicode(i)
        s2 = s2.lower()
        j = s.find(s2)
        if(j != -1):
            return True
    return False
def lenIterator(list):
    sum = 0
    for i in list :
        sum += 1
    return sum 
def getNumericalSymbol(sentence_text) :
    match = re.finditer(r"[0-9]*(/[0-9]*)*((/|-)[A-ZĐ]*[0-9]*)+", sentence_text)
    
    for i in match:
        return sentence_text[i.span()[0]:i.span()[1]]
    return None
def toLowerCase(string):
    s = to_unicode(string)
    s = s.lower()
    s = s.encode('utf-8')
    return s
def toUpperCase(string):
    s = to_unicode(string)
    s = s.upper()
    s = s.encode('utf-8')
    return s
def standardString(string):
    return toLowerCase(string.strip())
    # s = to_unicode(string)
    # match = re.finditer(r"[0-9]", s)
    # for i in match:
    #     start = i.span()[0]
    #     end = start
    #     for i in range(start,len(s)):
    #         if s[i].isdigit():
    #             continue
    #         elif s[i] == '/':
    #             continue
    #         elif s[i] == '-':
    #             continue
    #         elif s[i].isupper() and s[i].isalpha():
    #             continue
    #         else:
    #             break
    #     metionNumber = s[start:end]
    #     if metionNumber.find(m)