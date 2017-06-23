# coding:utf-8
from sqlalchemy import text
from db.basic_db import db_session
from db.models import WeiboData
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
def insert_weibo_data(weibo_data):
    # 存入数据的时候从更高一层判断是否会重复，不在该层做判断
    weibo_data.weibo_cont = process(weibo_data.weibo_cont)
    db_session.add(weibo_data)
    db_session.commit()


def get_wb_by_mid(mid):
    """
    :param mid: 微博id
    :return: 
    """
    return db_session.query(WeiboData).filter(WeiboData.weibo_id == mid).first()


@db_commit_decorator
def insert_weibo_datas(weibo_datas):
    for data in weibo_datas:
        r = get_wb_by_mid(data.weibo_id)
        if not r:
            weibo_data.weibo_cont = process(weibo_data.weibo_cont)
            db_session.add(data)
    db_session.commit()


@db_commit_decorator
def set_weibo_comment_crawled(mid):
    """
    如果存在该微博，那么就将comment_crawled字段设置为1;不存在该微博，就不做任何操作
    :param mid: 
    :return: 
    """
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.comment_crawled = 1
        db_session.commit()


def get_weibo_comment_not_crawled():
    return db_session.query(WeiboData.weibo_id).filter(text('comment_crawled=0')).all()


def get_weibo_repost_not_crawled():
    return db_session.query(WeiboData.weibo_id, WeiboData.uid).filter(text('repost_crawled=0')).all()


@db_commit_decorator
def set_weibo_repost_crawled(mid):
    """
    如果存在该微博，那么就将repost_crawled字段设置为1;不存在该微博，就不做任何操作
    :param mid: 
    :return: 
    """
    weibo_data = get_wb_by_mid(mid)
    if weibo_data:
        weibo_data.repost_crawled = 1
        db_session.commit()




