#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/28 13:05
# @Author  : duocai

# 导入:
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'users'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    passwd = Column(String(20))



