#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont
import glob
import os
import math
import re
import json
import subprocess
import time
import shlex
import asyncio
import requests 
import bs4 
from typing import Tuple
from humanfriendly import format_timespan
from pyrogram.errors.exceptions.flood_420 import FloodWait
import asyncio
import os
import time
from bot import LOGGER
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from bot.helpers.sql_helper import chidss

async def generate_screen_shots(
    video_file,
    output_directory,
    is_watermarkable,
    wf,
    min_duration,
    no_of_photos,
    locdl
    ):
    LOGGER.info(f'GENERATING SS:{video_file}')
    metadata = extractMetadata(createParser(video_file))
    duration = 0
    logo = chidss.search_url(locdl)
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_of_photos
        current_ttl = ttl_step
        for looper in range(0, no_of_photos):
            ss_img = await take_screen_shot(video_file, output_directory, current_ttl)
            current_ttl = current_ttl + ttl_step    
            ssp = "downloads/" + locdl + "/*.png"
            sso = "downloads/" + locdl + "/"
            images_path = glob.glob(ssp)
            for img_path in images_path:
                img = cv2.imread(img_path)
                if (isinstance(img, numpy.ndarray)):
                    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    draw = ImageDraw.Draw(img)
                    textSize = 50
                    fontStyle = ImageFont.truetype(
                        "font/CharlesWright-Bold.ttf", textSize, encoding="utf-8")
                    left = 100
                    top = 100
                    text =str(logo)
                    textColor = (255,0,0)
                    draw.text((left, top), text, textColor, font=fontStyle)
                    img2 = cv2.cvtColor(numpy.asarray(img), cv2.COLOR_RGB2BGR)
                    filename = os.path.basename(img_path)
                    cv2.imwrite(sso + filename, img2)
                    

            images.append(ss_img)
            
        return images
    else:
        return None

async def take_screen_shot(video_file, output_directory, ttl):

    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + str(time.time()) + ".png"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None  
async def generate_thumb(video_file, output_directory, thumbname, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
        "/" + thumbname + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None