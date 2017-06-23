# coding:utf-8
from db.basic_db import db_session
from db.models import WeiboComment
from decorators.decorator import db_commit_decorator


import os
import sys
import base64
from array import array
import re
import time



patternHttp = re.compile(r'http[\w\?\\/:\.]*')
patternRepMark = re.compile(r'\,+|\.+|\。+|\，+')
patternKeyWord = re.compile(r'#')
patternTitle = re.compile('【[^】]+】')
patternForward = re.compile(r'//@[^:]+\:')
patternAt = re.compile(r'@[\S]+\s')

def filterUrl(line):
    return patternHttp.sub('',line)

def _removeRep(match):
    return match.group(0)[0]
def filterRepMark(line):
    return patternRepMark.sub(_removeRep,line)

def filterKeyWord(line):
    return patternKeyWord.sub('',line)

def filterTitle(line):
    return patternTitle.sub('',line)

def filterAt(line):
    return patternAt.sub('',line)

def filterForward(line):
    #match = re.match(r'//@.*', line)
    #match = re.match(r'(\w+) (\w+)(?P<sign>.*)', 'hello world!')
    match = patternForward.split(line)
    res = ''
    i = len(match) - 1
    while i>=0:
        res=res+match[i]
        i = i-1
    #print res
    return res

def process(line):
    line = filterForward(line)
    line = filterTitle(line)
    line = filterAt(line)
    line = filterKeyWord(line)
    line = filterRepMark(line)
    line = filterUrl(line)
    return line



@db_commit_decorator
def save_comments(comment_list):
    for comment in comment_list:
        r = get_comment_by_id(comment.comment_id)
        if not r:
            save_comment(comment)
    db_session.commit()


@db_commit_decorator
def save_comment(comment):
  comment.comment_cont = process(comment.comment_cont)
    db_session.add(comment)
    db_session.commit()


def get_comment_by_id(cid):
    return db_session.query(WeiboComment).filter(WeiboComment.comment_id == cid).first()

