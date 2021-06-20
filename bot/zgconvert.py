#!/usr/bin/python3
# -*- coding: utf-8 -*-
#credit Myanmartools for Zawgyi Detection
#credit for zawgyi converter
#https://github.com/kanaung/py-converter

import sys, getopt
import re
import os
import shutil
import requests
import bs4
#Zaw Gyi to Unicode Conversion
def strtr(s, repl):
  pattern = '|'.join(map(re.escape, sorted(repl, key=len, reverse=True)))
  return re.sub(pattern, lambda m: repl[m.group()], s)

## This is faster and more correct
def strtr_re(s, patterns):
  for pattern, repl in patterns.items():
    s = re.sub(pattern, repl, s)
  return s

def zg_convert(zgdetect):
    data = zgdetect
    zguni = {'ဳ' : 'ု','ဴ' : 'ူ','္' : '်','်' : 'ျ','ျ' : 'ြ','ြ' : 'ွ','ွ' : 'ှ','ၚ' : 'ါ်','ၠ' : '္က','ၡ' : '္ခ','ၢ' : '္ဂ','ၣ' : '္ဃ','ၤ' : 'င်္','ၥ' : '္စ','ၦ' : '္ဆ','ၧ' : '္ဆ','ၨ' : '္ဇ','ၩ' : '္ဈ','ၪ' : 'ဉ','ၫ' : 'ည','ၬ' : '္ဋ','ၭ' : '္ဌ','ၮ' : 'ဍ္ဍ','ၯ' : 'ဍ္ဎ','ၰ' : '္ဏ','ၱ' : '္တ','ၲ' : '္တ','ၳ' : '္ထ','ၴ' : '္ထ','ၵ' : '္ဒ','ၶ' : '္ဓ','ၷ' : '္န','ၷ' : '္ပ','ၸ' : '္ပ','ၹ' : '္ဖ','ၺ' : '္ဗ','ၻ' : '္ဘ','ၼ' : '္မ','ၽ' : 'ျ','ၾ' : 'ြ','ၿ' : 'ြ','ႀ' : 'ြ','ႁ' : 'ြ','ႂ' : 'ြ','ႃ' : 'ြ','ႄ' : 'ြ','ႅ' : '္လ','ႆ' : 'ဿ','သ္သ' : 'ဿ','ႇ' : 'ှ','ႈ' : 'ှု','ႉ' : 'ှူ','ႊ' : 'ွှ','ႏ' : 'န','႐' : 'ရ','႑' : 'ဏ္ဍ','႒' : 'ဋ္ဌ','႓' : '္ဘ','႔' : '့','႕' : '့','႗' : 'ဋ္ဋ','၈ၤ':'ဂင်္','ဧ။္':'၏','ဧ၊္':'၏','၄င္း':'၎င်း','၎':'၎င်း','၎င္း':'၎င်း','ေ၀' : 'ေဝ','ေ၇' : 'ေရ','ေ၈':'ေဂ','စ်':'ဈ','ဥာ':'ဉာ','ဥ္':'ဉ်','ၾသ':'ဩ','ေၾသာ္':'ဪ'}
    zgunicorrect = {'\\s+္':'္','([က-အ])(င်္)' : '\\2\\1','(ေ)([က-အ၀၈၇]{1}္[က-အ၀၈၇]{1})' : '\\2\\1','([ေြ]{1,2})([က-အ၀၈၇]{1})':'\\2\\1','(ေ)([ျြွှ]+)':'\\2\\1','(ှ)(ျ)':'\\2\\1','(ံ)([ုူ])':'\\2\\1','([ုူ])([ိီ])':'\\2\\1','(ော)(္[က-အ])':'\\2\\1','(ဲ)(ွ)':'\\2\\1'}
    converted = strtr(data, zguni)
    converted = strtr_re(converted, zgunicorrect)
    return converted

def mmsub_desp(mmsuburl):
    url = str(mmsuburl).replace(' ', '')
   
    request_result = requests.get( url )
    soup = bs4.BeautifulSoup( request_result.text 
                            , "html.parser" )
   
    mmsubdiv = soup.find_all("div", {"class": "wp-content"})
        
    raw = str(mmsubdiv).replace('[<div class="wp-content" itemprop="description">', '').replace('<p>', '').replace('</p>', '').replace('<ul>','').replace('<li>', '').replace('</li>', '').replace('</ul>', '').replace('</div>]', '')
    mmsubdesp = raw + "\n" + url
    return mmsubdesp