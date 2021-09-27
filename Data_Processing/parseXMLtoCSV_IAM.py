from Data_Processing.Data_Transformation import apply_splitted_data
import os
import pandas as pd
import numpy as np
import sys
import xml.etree.ElementTree as ET 
from xml.sax.saxutils import unescape as unescape_
import json
from collections import defaultdict
#import imageio
import argparse

def unescape(s):
    return unescape_(s).replace('&quot;','"')

def getWordAndLineBoundaries(xmlPath):
    lines=[]
    w_lines=[]
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    writer = root.attrib['writer-id']
    allHs=0
    for line in root.findall('./handwritten-part/line'):
        line_id = line.attrib['id']
        trans=unescape(line.attrib['text'])
        minX=99999999
        maxX=-1
        minY=99999999
        maxY=-1
        words=[]
        for word in line.findall('word'):
            w_trans=unescape(word.attrib['text'])
            w_id=word.attrib['id']
            #print(w_trans)
            w_minX=99999999
            w_maxX=-1
            w_minY=99999999
            w_maxY=-1
            for cmp in word.findall('cmp'):
                x = int(cmp.attrib['x'])
                y = int(cmp.attrib['y'])
                w = int(cmp.attrib['width'])
                h = int(cmp.attrib['height'])
                #option1
                #maxX = max(maxX,x+w//2)
                #minX = min(minX,x-w//2)
                #maxY = max(maxY,y+h//2)
                #minY = min(minY,y-h//2)
                #option2
                maxX = max(maxX,x+w)
                minX = min(minX,x)
                maxY = max(maxY,y+h)
                minY = min(minY,y)
                w_maxX = max(w_maxX,x+w)
                w_minX = min(w_minX,x)
                w_maxY = max(w_maxY,y+h)
                w_minY = min(w_minY,y)
            words.append(([w_minY,w_maxY+1,w_minX,w_maxX+1],w_trans,w_id))

        
        #lineImg = formImg[minY:maxY+1,minX:maxX+1]
        lines.append(([minY,maxY+1,minX,maxX+1],trans,line_id))
        w_lines.append(words)
        allHs+=1+maxY-minY
    meanH = allHs/len(lines)
    newLines=[]
    for bounds,trans, line_id in lines:
        diff = meanH-(bounds[1]-bounds[0])
        if diff>0:
            bounds[0]-=diff/2
            bounds[1]+=diff/2
        bounds[2]-= meanH/4
        bounds[3]+= meanH/4
        bounds = [round(v) for v in bounds]
        #lineImg = formImg[bounds[0]:bounds[1],bounds[2]:bounds[3]]
        newLines.append((bounds,trans, line_id))
    newW_lines=[]
    for words in w_lines:
        newWords=[]
        for bounds,trans,id in words:
            diff = meanH-(bounds[1]-bounds[0])
            if diff>0:
                bounds[0]-=diff/2
                bounds[1]+=diff/2
            bounds[2]-= meanH/4
            bounds[3]+= meanH/4
            bounds = [round(v) for v in bounds]
            #lineImg = formImg[bounds[0]:bounds[1],bounds[2]:bounds[3]]
            newWords.append((bounds,trans,id))
        newW_lines.append(newWords)
    return  newW_lines,newLines, writer

def getLineBoundaries(xmlPath):
    lines=[]
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    writer = root.attrib['writer-id']
    allHs=0
    for line in root.findall('./handwritten-part/line'):

        trans=unescape(line.attrib['text'])
        assert('&' not in trans or ';' not in trans)
        minX=99999999
        maxX=-1
        minY=99999999
        maxY=-1
        for word in line.findall('word'):
            for cmp in word.findall('cmp'):
                x = int(cmp.attrib['x'])
                y = int(cmp.attrib['y'])
                w = int(cmp.attrib['width'])
                h = int(cmp.attrib['height'])
                #option1
                #maxX = max(maxX,x+w//2)
                #minX = min(minX,x-w//2)
                #maxY = max(maxY,y+h//2)
                #minY = min(minY,y-h//2)
                #option2
                maxX = max(maxX,x+w)
                minX = min(minX,x)
                maxY = max(maxY,y+h)
                minY = min(minY,y)

        
        #lineImg = formImg[minY:maxY+1,minX:maxX+1]
        lines.append(([minY,maxY+1,minX,maxX+1],trans))
        allHs+=1+maxY-minY
    meanH = allHs/len(lines)
    newLines=[]
    for bounds,trans in lines:
        diff = meanH-(bounds[1]-bounds[0])
        if diff>0:
            bounds[0]-=diff/2
            bounds[1]+=diff/2
        bounds[2]-= meanH/4
        bounds[3]+= meanH/4
        bounds = [round(v) for v in bounds]
        #lineImg = formImg[bounds[0]:bounds[1],bounds[2]:bounds[3]]
        newLines.append((bounds,trans))
    return newLines, writer

def getLineBoundariesWithID(xmlPath):
    lines=[]
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    writer = root.attrib['writer-id']
    allHs=0
    for line in root.findall('./handwritten-part/line'):
        line_id = line.attrib['id']
        trans=unescape(line.attrib['text'])
        assert('&' not in trans or ';' not in trans)
        minX=99999999
        maxX=-1
        minY=99999999
        maxY=-1
        for word in line.findall('word'):
            for cmp in word.findall('cmp'):
                x = int(cmp.attrib['x'])
                y = int(cmp.attrib['y'])
                w = int(cmp.attrib['width'])
                h = int(cmp.attrib['height'])
                #option1
                #maxX = max(maxX,x+w//2)
                #minX = min(minX,x-w//2)
                #maxY = max(maxY,y+h//2)
                #minY = min(minY,y-h//2)
                #option2
                maxX = max(maxX,x+w)
                minX = min(minX,x)
                maxY = max(maxY,y+h)
                minY = min(minY,y)

        
        #lineImg = formImg[minY:maxY+1,minX:maxX+1]
        lines.append(([minY,maxY+1,minX,maxX+1],trans,line_id))
        allHs+=1+maxY-minY
    meanH = allHs/len(lines)
    newLines=[]
    for bounds,trans,line_id in lines:
        #if id==line_id:
        diff = meanH-(bounds[1]-bounds[0])
        if diff>0:
            bounds[0]-=diff/2
            bounds[1]+=diff/2
        bounds[2]-= meanH/4
        bounds[3]+= meanH/4
        bounds = [round(v) for v in bounds]
        #lineImg = formImg[bounds[0]:bounds[1],bounds[2]:bounds[3]]
        newLines.append((bounds,trans,line_id))
    return newLines, writer
    #        return bounds,trans,writer
    #raise ValueError('id {} not in {}'.format(id,xmlPath))

def getLines(imagePath,xmlPath):
    formImg = imageio.imread(imagePath)
    lines=[]
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    writer = root.attrib['writer-id']
    print(writer)
    allHs=0
    for line in root.findall('./handwritten-part/line'):

        trans=unescape(line.attrib['text'])
        minX=99999999
        maxX=-1
        minY=99999999
        maxY=-1
        for word in line.findall('word'):
            for cmp in word.findall('cmp'):
                x = int(cmp.attrib['x'])
                y = int(cmp.attrib['y'])
                w = int(cmp.attrib['width'])
                h = int(cmp.attrib['height'])
                #option1
                #maxX = max(maxX,x+w//2)
                #minX = min(minX,x-w//2)
                #maxY = max(maxY,y+h//2)
                #minY = min(minY,y-h//2)
                #option2
                maxX = max(maxX,x+w)
                minX = min(minX,x)
                maxY = max(maxY,y+h)
                minY = min(minY,y)

        
        #lineImg = formImg[minY:maxY+1,minX:maxX+1]
        lines.append(([minY,maxY+1,minX,maxX+1],trans))
        allHs+=1+maxY-minY
    meanH = allHs/len(lines)
    newLines=[]
    for bounds,trans in lines:
        diff = meanH-(bounds[1]-bounds[0])
        if diff>0:
            bounds[0]-=diff/2
            bounds[1]+=diff/2
        bounds[2]-= meanH/4
        bounds[3]+= meanH/4
        bounds = [round(v) for v in bounds]
        lineImg = formImg[bounds[0]:bounds[1],bounds[2]:bounds[3]]
        newLines.append((lineImg,trans))
    return newLines

def getWordAndLineIDs(xmlPath):
    lines=[]
    words=[]
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    writer = root.attrib['writer-id']
    allHs=0
    for line in root.findall('./handwritten-part/line'):

        line_id=line.attrib['id']
        lines.append(line_id)
        for word in line.findall('word'):
            w_id=word.attrib['id']
            w_trans=unescape(word.attrib['text'])
            words.append((w_id,w_trans,line_id))
    return words,lines


def getTextBoundaries(lines_bb):
  text_bb = []
  for line in lines_bb:
    text_bb.append(line[0])

  text_bb = np.array(text_bb)
  # print(text_bb)
  # print(text_bb.shape)
  minCoord = np.min(text_bb, axis=0)
  maxCoord = np.max(text_bb, axis=0)

  return [minCoord[0], maxCoord[1], minCoord[2], maxCoord[3]]

def parseXMLtoCSV_IAM(xml_path, csv_path):
    for xml in os.listdir(xml_path):
        tree = ET.parse(xml).getroot()
        df = pd.DataFrame(columns=['id', 'attrType', 'y_min', 'y_max'	,'x_min'	,'x_max'	,'text'])

        rows = []
        text = tree.find('machine-printed-part')
        text_content = ''
        for line in text.findall('machine-print-line'):
        # print(line.attrib['text'])
        # print(type(line.attrib['text']))
            text_content += line.attrib['text'] + ' '

        word_id, line_id = getWordAndLineIDs(xml)
        words_bb, lines_bb, wr_id = getWordAndLineBoundaries(xml)
        text_bb = getTextBoundaries(lines_bb)
        #row = ['id', 'attrType', 'y_min', 'y_max'	,'x_min'	,'x_max'	,'text']
        text_row_append = [wr_id, '3', text_bb[0], text_bb[1], text_bb[2], text_bb[3], text_content]
        text_row_series = pd.Series(text_row_append, index=df.columns)
        df = df.append(text_row_series, ignore_index=True)

        for i in range(len(lines_bb)):
        # print(lines_bb[i])
            bbox = lines_bb[i][0]
            context = lines_bb[i][1]
            line_id = lines_bb[i][2]
            # ['id', 'attrType', 'y_min', 'y_max'	,'x_min'	,'x_max'	,'text']
            line_row_append = [line_id, '2', bbox[0], bbox[1], bbox[2], bbox[3], context]
            line_row_series = pd.Series(line_row_append, index=df.columns)
            df = df.append(line_row_series, ignore_index=True)
            for word in words_bb[i]:
                # print(word)
                bbox = word[0]
                context = word[1]
                word_id = word[2]
                # ['id', 'attrType', 'y_min', 'y_max'	,'x_min'	,'x_max'	,'text']
                word_row_append = [word_id, '1', bbox[0], bbox[1], bbox[2], bbox[3], context]
                word_row_series = pd.Series(word_row_append, index=df.columns)
                df = df.append(word_row_series, ignore_index=True)
            # print(words_bb)
            # print(len(words_bb))
            # print(lines_bb)
            # print(len(lines_bb))
        csv_file_path = csv_path + '/' + xml[0:len(xml)-4] + '.csv'
        # print(csv_file_path) 
        df.to_csv(csv_file_path, index=True)


if __name__ == 'main':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--foo', help='foo help')
    argparser.add_argument('-c', '--config',  default=None, type=str, help='config file path (default: None)')
    argparser.add_argument('-p', '--path', default=None, type=str, help='Original path')
    argparser.add_argument('-d', '--destination', default=None, type=str, help='Destination path')

    args = argparser.parse_args()
    if args.config is not None and (args.path is not None and args.destination is not None):
        print('WARNING! Choose --config for configurable file or --path/--desetiation for optimal path')
    else:
        if args.config is not None:
            if not os.path.isfile(args.config): 
                print('WARNING! The path does not exist')
            else:
                configs = json.load(open(args.config))
                xml_path = configs['IAM_xmltocsv']['xml_path']
                csv_path = configs['IAM_xmltocsv']['csv_path']
                parseXMLtoCSV_IAM(xml_path, csv_path)
               