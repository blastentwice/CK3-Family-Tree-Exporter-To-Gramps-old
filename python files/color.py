#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from PIL import Image,ImageOps,ImageDraw
import re
import sys
import json
import pickle
from collections import OrderedDict
import os
from collections.abc import Iterable
import time
import logging
logger=logging.getLogger(__name__)


# In[ ]:


def timer(start,end):
    minutes, seconds = divmod(end-start, 60)
    print("Finished in {:0>2}m {:05.2f}s".format(int(minutes),seconds))
    


# In[ ]:


def make_unique(key, dct):
    counter = 0
    unique_key = key

    while unique_key in dct:
        counter += 1
        unique_key = '{}_{}'.format(key, counter)
    return unique_key


def parse_object_pairs(pairs):
    dct = OrderedDict()
    for key, value in pairs:
        if key in dct:
            key = make_unique(key, dct)
        dct[key] = value
    return dct
def FindColor(width,height,img,r,g,b):
    for x in range(0,width):
        for y in range(0,height):
            px = img.getpixel((x, y))
            if px[0] == r and px[1] == g and px[2] == b:
                return True
            else:
                continue
    return False
def FindGreen(width,height,img):
    for x in range(0,width):
        for y in range(0,height):
            px = img.getpixel((x, y))
            if px[1] > 0:
                return True
            else:
                continue
    return False
def FindBlue(width,height,img):
    for x in range(0,width):
        for y in range(0,height):
            px = img.getpixel((x, y))
            if px[2] > 0:
                return True
            else:
                continue
    return False
def FindRed(width,height,img):
    for x in range(0,width):
        for y in range(0,height):
            px = img.getpixel((x, y))
            if px[0] > 0:
                return True
            else:
                continue
    return False


# In[ ]:


def getcoa(idnum):
    #global pathpat
    
    allembcolor=[]
    pathemb=[]
    position=[]
    scale=[]
    rotation=[]
    patcolor=[]
    embcolor1st=[]
    mylist=[]
    for i in coa[idnum]:
        if i=='pattern':
            pathpat=coa[idnum][i]
        elif re.search('color\d',i) is not None:
            patcolor.append(coa[idnum][i])
    if bool(patcolor) is False and bool(pathpat) is False:
        pathpat='pattern_solid.dds'
        patcolor.append(colordict['default'])
    elif bool(patcolor) is False and bool(pathpat) is True:
        patcolor.append(colordict['default'])
        patcolor.append(colordict['default'])
        
    elif bool(patcolor) is True and bool(pathpat) is False:
        pathpat='pattern_solid.dds'
    
    for i in coa[idnum]:
        count=0
        embcolor1st=[]
        if re.search('colored_emblem',i) is not None:
            for j in coa[idnum][i]:
                if re.search('color\d',j) is not None:
                    embcolor1st.append(coa[idnum][i][j])
                elif j=='texture' and 'instance' not in coa[idnum][i]:
                    mylist.append(i)
                    pathemb.append(coa[idnum][i][j])
                    position.append([0.5,0.5])
                    scale.append([1,1])
                    rotation.append(0)
                elif re.search('instance',j) is not None:
                    mylist.append(i)
                    pathemb.append((coa[idnum][i]['texture']))
                    haspos=False
                    hasscale=False
                    hasrot=False
                    for k in coa[idnum][i][j]:
                        if k=='position':
                            position.append(coa[idnum][i][j][k])
                            haspos=True
                        elif k=='scale':
                            scale.append(coa[idnum][i][j][k])
                            hasscale=True
                        elif k=='rotation':
                            rotation.append(coa[idnum][i][j][k])
                            hasrot=True
                    if haspos is False:
                        position.append([0.5,0.5])
                    if hasscale is False:
                        scale.append([1,1])
                    if hasrot is False:
                        rotation.append(0)
        if re.search('colored_emblem',i) is not None:
            allembcolor.append(embcolor1st)
            for key, value in coa[idnum][i].items():
                if key.startswith('instance'):
                    count+=1
            for _ in range(count-1):
                allembcolor.append(embcolor1st)
                
    return allembcolor,pathemb,position,scale,rotation,patcolor,mylist,pathpat


# In[ ]:


def getcadet(idnum):
    patpos=[]
    patscale=[]
    patrot=[]
    patcolor1st=[]
    allpatcolor=[]
    allembcolor=[]
    pathemb=[]
    position=[]
    scale=[]
    rotation=[]
    subpat=[]
    patcolor=[]
    embcolor1st=[]
    mylist=[]
    mysub=[]
    allsubpat=[]
    mask2allsub={}
    maskcount=-1
    subcount=-1
    for i in coa[idnum]:
        if i=='pattern':
            pathpat=coa[idnum][i]
        elif re.search('color\d',i) is not None:
            patcolor.append(coa[idnum][i])
    if bool(patcolor) is False and bool(pathpat) is False:
        pathpat='pattern_solid.dds'
        patcolor.append(colordict['default'])
    if bool(patcolor) is False:
        patcolor.append(colordict['default'])
        patcolor.append(colordict['default'])            
        
    for pattern in coa[idnum]:
        patcolor1st=[]
        if re.search('sub',pattern) is not None:
            subcount+=1
            for sub in coa[idnum][pattern]:
                count=0
                embcolor1st=[]
                if re.search('pattern',sub) is not None:
                    subpat.append(coa[idnum][pattern][sub])     
                if re.search('color\d',sub) is not None:
                    patcolor1st.append(coa[idnum][pattern][sub])
                elif re.search('instance',sub) is not None:
                    haspos=False
                    hasscale=False
                    hasrot=False
                    for insval in coa[idnum][pattern][sub]:
                        if insval=='offset':
                            parentoffset=coa[idnum][pattern][sub][insval]
                            patpos.append(coa[idnum][pattern][sub][insval])
                            haspos=True
                        elif insval=='scale':
                            parentscale=coa[idnum][pattern][sub][insval]
                            patscale.append(coa[idnum][pattern][sub][insval])
                            hasscale=True
                        elif insval=='rotation':
                            patrot.append(coa[idnum][pattern][sub][insval])
                            hasrot=True
                    if haspos is False:
                        parentoffset=[0,0]
                        patpos.append([0,0])
                    if hasscale is False:
                        parentscale=[1,1]
                        patscale.append([1,1])
                    if hasrot is False:
                        patrot.append(0)
                elif re.search('colored_emblem',sub) is not None:
                    for emblem in coa[idnum][pattern][sub]:
                        if re.search('color\d',emblem) is not None:
                            embcolor1st.append(coa[idnum][pattern][sub][emblem])
                        elif emblem=='texture' and 'instance' not in coa[idnum][pattern][sub]:
                            maskcount+=1
                            mask2allsub[maskcount]=subcount
                            mylist.append(sub)
                            mysub.append(pattern)
                            pathemb.append(coa[idnum][pattern][sub][emblem])
                            position.append([parentoffset[0]+0.5*parentscale[0],parentoffset[1]+0.5*parentscale[1]])
                            scale.append([1*parentscale[0],1*parentscale[1]])
                            rotation.append(0)
                        elif re.search('instance',emblem) is not None:
                            maskcount+=1
                            mask2allsub[maskcount]=subcount
                            mylist.append(sub)
                            mysub.append(pattern)
                            pathemb.append((coa[idnum][pattern][sub]['texture']))
                            haspos=False
                            hasscale=False
                            hasrot=False
                            for embval in coa[idnum][pattern][sub][emblem]:
                                if embval=='position':
                                    childpos=coa[idnum][pattern][sub][emblem][embval]
                                    modpos=[parentoffset[0]+childpos[0]*parentscale[0],parentoffset[1]+childpos[1]*parentscale[1]]
                                    position.append(modpos)
                                    haspos=True
                                elif embval=='scale':
                                    childscale=coa[idnum][pattern][sub][emblem][embval]
                                    modscale=[childscale[0]*parentscale[0],childscale[1]*parentscale[1]]
                                    scale.append(modscale)
                                    hasscale=True
                                elif embval=='rotation':
                                    rotation.append(coa[idnum][pattern][sub][emblem][embval])
                                    hasrot=True
                            if haspos is False:
                                position.append([parentoffset[0]+0.5*parentscale[0],parentoffset[1]+0.5*parentscale[1]])
                            if hasscale is False:
                                scale.append([1*parentscale[0],1*parentscale[1]])
                            if hasrot is False:
                                rotation.append(0)
                    if re.search('colored_emblem',sub) is not None:
                        allembcolor.append(embcolor1st)
                        for key, value in coa[idnum][pattern][sub].items():
                            if key.startswith('instance'):
                                count+=1
                        for _ in range(count-1):
                            allembcolor.append(embcolor1st)
                            
            
        if re.search('sub',pattern) is not None:
            allpatcolor.append(patcolor1st)
                    
                



    return patpos,patscale,patrot,allpatcolor,allembcolor,pathemb,position,scale,rotation,subpat,patcolor,mylist,pathpat,mysub,mask2allsub


# In[ ]:


def pattern(pathpat,patcolor):
    pngpath=re.sub('(.*).dds',r'\1.png',pathpat)
    img= Image.open(fr'coa_icon/patterns/{pngpath}')
    if img.size!=(256,256):
        img=img.resize((256,256),Image.NEAREST)
    patarray= np.array(img)
    width, height = img.size
    if FindColor(width,height,img,255,0,0) is True and FindColor(width,height,img,255,255,0) is True and FindColor(width,height,img,255,255,255) is True :
        if len(patcolor)==2:
            patcolor.append(colordict['default'])
        elif len(patcolor)==1:
            patcolor.append(colordict['default'])
            patcolor.append(colordict['default'])
        elif bool(patcolor) is False:
            patcolor.append(colordict['default'])
            patcolor.append(colordict['default'])
            patcolor.append(colordict['default'])
        #patterns
        red, green, blue, alpha = patarray.T 
        # Red
        toreplace= (red==255) & (blue==0) & (green==0)
        patarray[..., :-1][toreplace.T] = (patcolor[0]) 
        #Yellow
        toreplace= (red==255) & (blue==0) & (green==255)
        patarray[..., :-1][toreplace.T] = (patcolor[1]) 
        #White
        toreplace= (red==255) & (blue==255) & (green==255)
        patarray[..., :-1][toreplace.T] = (patcolor[2])
        patdata = Image.fromarray(patarray)

    elif FindColor(width,height,img,255,0,0) is True and FindColor(width,height,img,255,255,0) is True:
        if len(patcolor)==1:
            patcolor.append(colordict['default'])
            patcolor.append(colordict['default'])
        elif bool(patcolor) is False:
            patcolor.append(colordict['default'])
            patcolor.append(colordict['default'])
            patcolor.append(colordict['default'])
        #patterns
        red, green, blue, alpha = patarray.T 
        ######RED

        # Red
        toreplace= (red==255) & (blue==0) & (green==0)
        patarray[..., :-1][toreplace.T] = (patcolor[0]) 
        #Yellow
        toreplace= (red==255) & (blue==0) & (green==255)
        patarray[..., :-1][toreplace.T] = (patcolor[1]) 
        patdata = Image.fromarray(patarray)        
        
    elif FindColor(width,height,img,255,0,0) is True:
                #patterns
        red, green, blue, alpha = patarray.T 
        # Red
        toreplace= (red==255) & (blue==0) & (green==0)
        patarray[..., :-1][toreplace.T] = (patcolor[0]) 
        patdata = Image.fromarray(patarray)
       
        
    #red mask
    redmask=img.copy()
    redmask= np.array(redmask)
    red, green, blue, alpha = redmask.T 
    toreplace= (red>0) & (blue==0) & (green==0) &(alpha>0)
    redmask[toreplace.T] = (255,255,255,0)
    toreplace= (red>0) & (blue==0) & (green>0)
    redmask[..., :-1][toreplace.T] = (255,255,255)
    redmask = Image.fromarray(redmask)


    #yellow mask
    yellowmask=img.copy()
    yellowmask= np.array(yellowmask)
    red, green, blue, alpha = yellowmask.T 
    toreplace= (red>0) & (blue==0) & (green>0) &(alpha>0)
    yellowmask[toreplace.T] = (255,255,255,0)
    toreplace= (red>0) & (blue==0) & (green==0)
    yellowmask[..., :-1][toreplace.T] = (255,255,255)
    yellowmask = Image.fromarray(yellowmask)
    return patdata,redmask,yellowmask
    #patdata.save('test.png')


# In[ ]:


def subpattern(subpat,allpatcolor,patscale):
    patall=[]
    redmasklist=[]
    yellowmasklist=[]
    for i in range(len(subpat)):
        pngpath=re.sub('(.*).dds',r'\1.png',subpat[i])
        img= Image.open(fr'coa_icon/patterns/{pngpath}')
        if img.size!=(256,256):
            img=img.resize((256,256),Image.NEAREST)
        patarray= np.array(img)
        width, height = img.size
        if FindColor(width,height,img,255,0,0) is True and FindColor(width,height,img,255,255,0) is True and FindColor(width,height,img,255,255,255) is True :
            #patterns
            red, green, blue, alpha = patarray.T 
            # Red
            toreplace= (red==255) & (blue==0) & (green==0)
            patarray[..., :-1][toreplace.T] = (allpatcolor[i][0]) 
            #Yellow
            toreplace= (red==255) & (blue==0) & (green==255)
            patarray[..., :-1][toreplace.T] = (allpatcolor[i][1]) 
            #White
            toreplace= (red==255) & (blue==255) & (green==255)
            patarray[..., :-1][toreplace.T] = (allpatcolor[i][2])
            patdata = Image.fromarray(patarray)
            nw=int(patscale[i][0]*width)
            nh=int(patscale[i][1]*height)
            patdata=patdata.resize((nw,nh),Image.NEAREST)
            patall.append(patdata)
        elif FindColor(width,height,img,255,0,0) is True and FindColor(width,height,img,255,255,0) is True:
                    #patterns
            red, green, blue, alpha = patarray.T 
            ######RED

            # Red
            toreplace= (red==255) & (blue==0) & (green==0)
            patarray[..., :-1][toreplace.T] = (allpatcolor[i][0]) 
            #Yellow
            toreplace= (red==255) & (blue==0) & (green==255)
            patarray[..., :-1][toreplace.T] = (allpatcolor[i][1]) 
            patdata = Image.fromarray(patarray)
            nw=int(patscale[i][0]*width)
            nh=int(patscale[i][1]*height)
            patdata=patdata.resize((nw,nh),Image.NEAREST)
            patall.append(patdata)
        elif FindColor(width,height,img,255,0,0) is True:
                    #patterns
            red, green, blue, alpha = patarray.T 
            # Red
            toreplace= (red==255) & (blue==0) & (green==0)
            patarray[..., :-1][toreplace.T] = (allpatcolor[i][0]) 
            patdata = Image.fromarray(patarray)
            nw=int(patscale[i][0]*width)
            nh=int(patscale[i][1]*height)
            patdata=patdata.resize((nw,nh),Image.NEAREST)
            patall.append(patdata)
        #red mask
        
        redmask=img.copy()
        redmask=redmask.resize((nw,nh),Image.NEAREST)
        redmask= np.array(redmask)
        red, green, blue, alpha = redmask.T 
        toreplace= (red>0) & (blue==0) & (green==0) &(alpha>0)
        redmask[toreplace.T] = (255,255,255,0)
        toreplace= (red>0) & (blue==0) & (green>0)
        redmask[..., :-1][toreplace.T] = (255,255,255)
        redmask = Image.fromarray(redmask)
        redmasklist.append(redmask)

        #yellow mask
        yellowmask=img.copy()
        yellowmask=yellowmask.resize((nw,nh),Image.NEAREST)
        yellowmask= np.array(yellowmask)
        red, green, blue, alpha = yellowmask.T 
        toreplace= (red>0) & (blue==0) & (green>0) &(alpha>0)
        yellowmask[toreplace.T] = (255,255,255,0)
        toreplace= (red>0) & (blue==0) & (green==0)
        yellowmask[..., :-1][toreplace.T] = (255,255,255)
        yellowmask = Image.fromarray(yellowmask)
        yellowmasklist.append(yellowmask)
    return patall,redmasklist,yellowmasklist
        #patdata.save('test.png')


# In[ ]:


def emblem(pathemb,allembcolor,scale,rotation):
    emball=[]
    for i in range(len(pathemb)):
        pngpath=re.sub('(.*).dds',r'\1.png',pathemb[i])
        img= Image.open(fr'coa_icon/colored_emblems/{pngpath}')
        if img.size!=(256,256):
            img=img.resize((256,256),Image.NEAREST)
            
        emb= np.array(img) 
        width, height = img.size
        if pngpath=='ce_blank.png' or pngpath=='ce_empty.png':
            emball.append(img)

            
        elif FindGreen(width,height,img) is True and FindBlue(width,height,img) is True:
            # G
            data2 = emb.copy()
            data2[:, :, 0] = 0
            data2[:, :, 2] = 0
            g = (Image.fromarray(data2)).copy()
            #B
            data3 = emb.copy()
            data3[:, :, 0] = 0
            data3[:, :, 1] = 0
            b = (Image.fromarray(data3)).copy()
            if len(allembcolor[i])>=2:  
                rwith1=allembcolor[i][0]
                rwith2=allembcolor[i][1]
            elif len(allembcolor[i])==1:
                rwith1=allembcolor[i][0]  
                rwith2=(colordict['default'])
            elif bool(allembcolor) is False:
                rwith1=(colordict['default']) 
                rwith2=(colordict['default'])
            
        ####################GREEN
            
            red, green, blue, alpha = data2.T 
            toreplace = (red>=0) & (blue>=0) & (green<100) &(alpha>0)
            data2[toreplace.T] = (255,255,255,0) # Transpose back needed
            toreplace = (red==0) & (blue==0) &(green>0)
            data2[..., :-1][toreplace.T] = rwith2 # Transpose back needed
            nw=int(scale[i][0]*width)
            nh=int(scale[i][1]*height)
            newimg=Image.fromarray(data2)
            if nw<0:
                newimg=ImageOps.mirror(newimg)
                nw=nw*-1
            if nh<0:
                newimg=ImageOps.flip(newimg)
                nh=nh*-1
            if nw!=256 or nh!=256:
                greendata=newimg.resize((nw,nh),Image.NEAREST)
            else:
                greendata=newimg
            ######BLUE
            red, green, blue, alpha = data3.T 
            toreplace = (red>=0) & (blue<100) & (green>=0) &(alpha>0)
            data3[toreplace.T] = (255,255,255,0) # Transpose back needed
            toreplace = (red == 0) & (blue>0) & (green== 0)
            data3[..., :-1][toreplace.T] = rwith1 # Transpose back needed
            nw=int(scale[i][0]*width)
            nh=int(scale[i][1]*height)
            newimg=Image.fromarray(data3)
            if nw<0:
                newimg=ImageOps.mirror(newimg)
                nw=nw*-1
            if nh<0:
                newimg=ImageOps.flip(newimg)
                nh=nh*-1
            if nw!=256 or nh!=256:
                bluedata=newimg.resize((nw,nh),Image.NEAREST)
            else:
                bluedata=newimg
            ############COMBINE
            if rotation[i]<0:
                rot=rotation[i]+360
                greendata=greendata.rotate(rot)
                bluedata=bluedata.rotate(rot)
            elif rotation[i]>0:
                  bluedata=bluedata.rotate(rotation[i])
            blueb= bluedata.copy()
            blueb.paste(greendata, (0, 0), greendata)
            emball.append(blueb)  
            
        elif FindBlue(width,height,img) is True:
            #B
            data3 = emb.copy()
            data3[:, :, 0] = 0
            data3[:, :, 1] = 0
            b = (Image.fromarray(data3)).copy
            if len(allembcolor[i])>0:
                rwith1=allembcolor[i][0]
            elif bool(allembcolor) is False:
                rwith1=((114,59,29)) 
            ###########BLUE
            red, green, blue, alpha = data3.T 
            toreplace = (red>=0) & (blue<100) & (green>=0) &(alpha>0)
            data3[toreplace.T] = (255,255,255,0) # Transpose back needed
            toreplace = (red == 0) & (blue<=255) & (green== 0)
            data3[..., :-1][toreplace.T] = rwith1 # Transpose back needed
            nw=int(scale[i][0]*width)
            nh=int(scale[i][1]*height)
            newimg=Image.fromarray(data3)
            if nw<0:
                newimg=ImageOps.mirror(newimg)
                nw=nw*-1
            if nh<0:
                newimg=ImageOps.flip(newimg)
                nh=nh*-1
                
            if nw!=256 or nh!=256:
                bluedata=newimg.resize((nw,nh),Image.NEAREST)
                
            else:
                bluedata=newimg
            ############COMBINE
            if rotation[i]<0:
                rot=rotation[i]+360
                bluedata=bluedata.rotate(rot)
            elif rotation[i]>0:
                bluedata=bluedata.rotate(rotation[i])
            blueb= bluedata.copy()
            emball.append(blueb)  
        else:
            print('false')
    return emball


# In[ ]:


def masking(emball,position,yellowmask,redmask,idnum,mylist):
    for i in range(len(emball)):
        if 'mask' in coa[idnum][mylist[i]] and coa[idnum][mylist[i]]['mask'][0]==1:
            blank = Image.new('RGBA', (256, 256))
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            blank.paste(emball[i],offset)
            emball[i]=Image.composite(redmask,blank,redmask)
            emball[i]= np.array(emball[i])
            red, green, blue, alpha = emball[i].T 
            toreplace= (red==255) & (blue==255) & (green==255) &(alpha>0)
            emball[i][toreplace.T] = (255,255,255,0)
            emball[i] = Image.fromarray(emball[i])
        elif 'mask' in coa[idnum][mylist[i]] and coa[idnum][mylist[i]]['mask'][1]==2:
            blank = Image.new('RGBA', (256, 256))
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            blank.paste(emball[i],offset)
            emball[i]=Image.composite(yellowmask,blank,yellowmask)
            emball[i]= np.array(emball[i])
            red, green, blue, alpha = emball[i].T 
            toreplace= (red==255) & (blue==255) & (green==255) &(alpha>0)
            emball[i][toreplace.T] = (255,255,255,0)
            emball[i] = Image.fromarray(emball[i])
        else:
            blank = Image.new('RGBA', (256, 256))
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            blank.paste(emball[i],offset)
            emball[i]=blank.copy()
    return emball


# In[ ]:


def coamasking(emball,position,yellowmasklist,redmasklist,idnum,mylist,mask2allsub,mysub,patpos):
    ismask=[]
    for i in range(len(emball)):
        
        if 'mask' in coa[idnum][mysub[i]][mylist[i]] and coa[idnum][mysub[i]][mylist[i]]['mask'][0]==1:
            masknum=mask2allsub[i]
            

            blank = Image.new('RGBA', (256, 256))
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            blank.paste(emball[i],offset)

            blank2 = Image.new('RGBA', (256, 256))
            width,height=redmasklist[masknum].size      
            offset =(256*patpos[masknum][0],256*patpos[masknum][1])
            offset=(int(offset[0]),int(offset[1]))
            blank2.paste(redmasklist[masknum],offset)


            emball[i]=Image.composite(blank2,blank,blank2)
            emball[i]= np.array(emball[i])
            red, green, blue, alpha = emball[i].T 
            toreplace= (red==255) & (blue==255) & (green==255) &(alpha>0)
            emball[i][toreplace.T] = (255,255,255,0)
            emball[i] = Image.fromarray(emball[i])
            ismask.append(i)

            
        elif 'mask' in coa[idnum][mysub[i]][mylist[i]] and coa[idnum][mysub[i]][mylist[i]]['mask'][1]==2:
            masknum=mask2allsub[i]
            
            blank = Image.new('RGBA', (256, 256))
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            blank.paste(emball[i],offset)

            blank2 = Image.new('RGBA', (256, 256))
            width,height=yellowmasklist[masknum].size      
            offset =(256*patpos[masknum][0],256*patpos[masknum][1])
            offset=(int(offset[0]),int(offset[1]))
            blank2.paste(yellowmasklist[masknum],offset)


            emball[i]=Image.composite(blank2,blank,blank2)
            emball[i]= np.array(emball[i])
            red, green, blue, alpha = emball[i].T 
            toreplace= (red==255) & (blue==255) & (green==255) &(alpha>0)
            emball[i][toreplace.T] = (255,255,255,0)
            emball[i] = Image.fromarray(emball[i])
            ismask.append(i)
        
           
    return emball,ismask


# In[ ]:


def testmask(mylist,idnum):
    for i in range(len(mylist)):
        if 'mask' in coa[idnum][mylist[i]]:
            return True
    return False
def testmaskcadet(mylist,idnum,mysub):
    for i in range(len(mylist)):
        if 'mask' in coa[idnum][mysub[i]][mylist[i]]:
            return True
    return False        


# In[ ]:


def coat(emball,position,istrue,patb):
    if istrue is False:
        for i in range(len(emball)):
            if position[i]==[0, 0]:
                patb.paste(emball[i],emball[i])
                continue
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            patb.paste(emball[i],offset,emball[i])
    elif istrue is True:
        for i in range(len(emball)):
            if position[i]==[0, 0]:
                patb.paste(emball[i],emball[i])
                continue
            width,height=emball[i].size
            offset2=(width/2,height/2)        
            offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
            offset=(int(offset[0]),int(offset[1]))
            patb.paste(emball[i],emball[i])
    
    return patb


# In[ ]:


def cadetcoat(patall,emball,patpos,position,patb,ismask):
    
    for i in range (len(patall)):
       # width,height=emball[i].size
        offset =((256*patpos[i][0]),(256*patpos[i][1]))
        offset=(int(offset[0]),int(offset[1])) 
        patb.paste(patall[i],offset,patall[i])
    
    for i in range(len(emball)):
        if position[i]==[0, 0]:
            patb.paste(emball[i],emball[i])
            continue 
        if i in ismask:
            patb.paste(emball[i],emball[i])
            continue 
        width,height=emball[i].size
        offset2=(width/2,height/2)        
        offset =((256*position[i][0])-offset2[0],(256*position[i][1])-offset2[1])
        offset=(int(offset[0]),int(offset[1]))
        patb.paste(emball[i],offset,emball[i])
    return patb


# In[ ]:


def prepareborder():
#RENKNOWN BORDER

    mask=Image.open('coa_icon/rank/house_115.png')
    house_mask=Image.open('coa_icon/rank/house_mask.png')
    house_mask= house_mask.resize((256,256))
    b1= mask.crop((0*153,0*150,1*153,1*150))
    b1=b1.resize((330,330))
    b2= mask.crop((1*153,0, 153*2, 150))
    b2=b2.resize((330,330))
    b3=mask.crop((2*153,0, 153*3, 150))
    b3=b3.resize((330,330))
    b4=mask.crop((3*153,0, 153*4, 150))
    b4=b4.resize((330,330))
    b5=mask.crop((4*153,0, 153*5, 150))
    b5=b5.resize((330,330))
    b6=mask.crop((5*153,0, 153*6, 150))
    b6=b6.resize((330,330))    
#TITLE RANK BORDER
    title_mask=Image.open('coa_icon/rank/title_mask.png')
    title_mask= title_mask.resize((256,256))
    mask2=Image.open('coa_icon/rank/title_86.png')
    mask2= mask2.resize((290,290))
    crowns=Image.open('coa_icon/rank/crown_strip_115_gameconcept.png')
    merc=Image.open('coa_icon/rank/mercenary_topframe_115.png')
    c1= crowns.crop((0*104,0*104,1*104,1*104))
    c1=c1.resize((290,290))
    c2= crowns.crop((1*104,0, 104*2, 104))
    c2=c2.resize((290,290))
    c3=crowns.crop((2*104,0, 104*3, 104))
    c3=c3.resize((290,290))
    c4=crowns.crop((3*104,0, 104*4, 104))
    c4=c4.resize((290,290))
    c5=crowns.crop((4*104,0, 104*5, 104))
    c5=c5.resize((290,290))
    cx=merc.resize((290,128))
    return b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,cx,title_mask,mask2,house_mask


# In[ ]:


def addborder(patb,idnum,isdyn,istitle,b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,cx,title_mask,mask2,house_mask):
#DYNASTY RENOWN
    if isdyn is True:
        spec=patb.copy()
        wmask=Image.composite(spec,house_mask,house_mask)
        blank = Image.new('RGBA', (325, 325))
        offset =((330-256)//2,(330-256)//2)
        blank.paste(wmask,offset)

        if dynprespic[idnum]>=0 and dynprespic[idnum]<1000:
            blank.paste(b1,b1)
        elif dynprespic[idnum]>=1000 and  dynprespic[idnum]<4000:
            blank.paste(b2,b2)
        elif  dynprespic[idnum]>=4000 and  dynprespic[idnum]<11000:
              blank.paste(b3,b3)        
        elif  dynprespic[idnum]>=11000 and dynprespic[idnum]<22000:
            blank.paste(b4,b4)
        elif dynprespic[idnum]>=22000 and dynprespic[idnum]<37000:
            blank.paste(b5,b5)
        elif dynprespic[idnum]>=37000:
            blank.paste(b6,b6)
        final=blank
#TITLE
    elif istitle is True:
        spec2=patb.copy()

        wmask2=Image.composite(spec2,title_mask,title_mask)
        blank2 = Image.new('RGBA', (290, 290))
        offset2 =((290-256)//2,(290-256)//2)
        blank2.paste(wmask2,offset2)
        blank2.paste(mask2,mask2)

        blank3 = Image.new('RGBA', (480, 480))
        offset3 =((480-290)//2,(480-290)//2)

        blank3.paste(blank2,(95,197))
        offset4 =((480-290)//2,(480-290)//2)

        if titlerankpic[idnum]=='b':
             blank3.paste(c1,(100,16),c1)
        elif titlerankpic[idnum]=='c':
            blank3.paste(c2,(98,-3),c2)
        elif titlerankpic[idnum]=='d':
            blank3.paste(c3,(100,-5),c3)
        elif titlerankpic[idnum]=='k':
            blank3.paste(c4,(95,-25),c4)    
        elif titlerankpic[idnum]=='e':
            blank3.paste(c5,(95,-33),c5)
        elif titlerankpic[idnum]=='x':
            blank3.paste(cx,(95,85),cx)
        
        final=blank3
    return final


# In[ ]:


with open(r'.\pickle\pic.pickle','rb') as f:
        traitpic=pickle.load(f)
        faithpic=pickle.load(f)
        dyncoapic=pickle.load(f)
        titlecoapic=pickle.load(f)
        dynprespic=pickle.load(f)
        titlerankpic=pickle.load(f)
with open(r'.\pickle\json.pickle','rb') as f:
    data=pickle.load(f)
colordict={
'red':(114,33,22),
'blue':(20,62,102),
'yellow':(191,133,47),
'green':(30,76,35),
'black':(25,22,19),
'white':(204,201,199),
'purple':(89,26,64),
'orange':(153,58,0),
'grey':(127,127,127),
'brown':(114,59,29),
'blue_light':(42,93,140),
'green_light':(51,102,56),
'yellow_light':(255,173,50),
'default':(60,13,5)
}        

live=data['living']
faithde=data['religion']['faiths']
faithre=data['religion']['religions']
cult=data['culture_manager']['cultures']
live=data['living']
dead=data['dead_unprunable']
other=data['characters']['dead_prunable']
dyn=data['dynasties']['dynasty_house']
title=data['landed_titles']
coa=data['coat_of_arms']['coat_of_arms_manager_database']
coafind=data['dynasties']['dynasties']        

newdyn=[i for i in dyncoapic.values()]  
newtitle=[i for i in titlecoapic.values()]
allcoa=newdyn+newtitle
setcoa=set(allcoa)
setcoa=list(map(int,setcoa))
setcoa=(sorted(setcoa))
setcoa=list(setcoa)
coalist=list(map(str,setcoa))


# In[ ]:


def maincoaex(mydir):

    count=0
    b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,cx,title_mask,mask2,house_mask=prepareborder()
    start = time.time()
    
        
    for idnum in coalist:
        try:
            if os.path.isfile(fr'./COA/{idnum}.png') is True:
                count+=1
                print(f'{count}/{len(coalist)} COA PROCESSED')
                continue
            else:
                pass
            isdyn=False
            istitle=False
            if idnum in dynprespic:
                isdyn=True
            elif idnum in titlerankpic:
                istitle=True
            #CADET
            if 'sub' in coa[idnum]:
                patpos,patscale,patrot,allpatcolor,allembcolor,pathemb,position,scale,rotation,subpat,patcolor,mylist,pathpat,mysub,mask2allsub=getcadet(idnum)
                patcolor=[ colordict.get(item,item) for item in patcolor ]
                allembcolor=[ [colordict.get(item,item) for item in somethings]  for somethings in allembcolor]
                allpatcolor=[ [colordict.get(item,item) for item in somethings]  for somethings in allpatcolor]
                patdata,redmask,yellowmask=pattern(pathpat,patcolor)
                patb=patdata.copy()
                patall,redmasklist,yellowmasklist=subpattern(subpat,allpatcolor,patscale)
                emball=emblem(pathemb,allembcolor,scale,rotation)

                if testmaskcadet(mylist,idnum,mysub) is True:
                    emball,ismask=coamasking(emball,position,yellowmasklist,redmasklist,idnum,mylist,mask2allsub,mysub,patpos)
                else:
                    ismask=[]

                patb=cadetcoat(patall,emball,patpos,position,patb,ismask)
                final=addborder(patb,idnum,isdyn,istitle,b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,cx,title_mask,mask2,house_mask)   
                final.save(f'{mydir}/{idnum}.png')

            elif 'sub' not in coa[idnum]:
                allembcolor,pathemb,position,scale,rotation,patcolor,mylist,pathpat=getcoa(idnum)
                patcolor=[ colordict.get(item,item) for item in patcolor ]
                allembcolor=[ [colordict.get(item,item) for item in somethings]  for somethings in allembcolor]
                patdata,redmask,yellowmask=pattern(pathpat,patcolor)
                emball=emblem(pathemb,allembcolor,scale,rotation)
                if testmask(mylist,idnum) is True:
                    istrue=True
                    emball=masking(emball,position,yellowmask,redmask,idnum,mylist)
                else:
                    istrue=False
                patb=patdata.copy()
                patb=coat(emball,position,istrue,patb)
                final=addborder(patb,idnum,isdyn,istitle,b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,cx,title_mask,mask2,house_mask)
                final.save(f'{mydir}/{idnum}.png')
            count+=1
            print(f'{count}/{len(coalist)} COA PROCESSED')
        except Exception as e:
            print(e)
            logging.error(e, exc_info=True)
            raise
            break
    end = time.time()
    timer(start,end)

