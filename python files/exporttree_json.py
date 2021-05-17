#!/usr/bin/env python
# coding: utf-8

# In[6]:


import json
import re
import time
import pandas as pd
import warnings
import os
import csv
import unidecode 
import pickle
import zipfile
import json
import subprocess
import xml.etree.ElementTree as ET
import gzip
import traceback
import logging
import sys
from collections import OrderedDict
import numpy as np
from PIL import Image,ImageOps,ImageDraw
import datetime as dt 
import importlib
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
logging.basicConfig(filename='exporter.log', level=logging.DEBUG)
logger=logging.getLogger(__name__)


# In[ ]:


def excel_format(num):
    res = ""
    while num:
        mod = (num - 1) % 26
        res = chr(65 + mod) + res
        num = (num - mod) // 26
    return res

def full_format(num, d=3):
    chars = num // (10**d-1) + 6 # this becomes   A..ZZZ
    digit = num %  (10**d-1) + 1 # this becomes 001..999
    return excel_format(chars) + "{:0{}d}".format(digit, d)

def timer(start,end):
    minutes, seconds = divmod(end-start, 60)
    print("Finished in {:0>2}m {:05.2f}s".format(int(minutes),seconds))



# In[ ]:


#Load all the second time
def loadall(jsondir,gamedir):
    try:
        with open(jsondir,encoding='utf-8') as f:
            data=json.load(f)
        with open (fr'{gamedir}\localization\english\names\character_names_l_english.yml',encoding='utf-8') as f:
            locnames=f.read()
        with open (fr'{gamedir}\localization\english\dynasties\dynasty_names_l_english.yml',encoding='utf-8') as f:
            dynloc=f.read()
        with open (fr'{gamedir}\localization\english\culture\cultures_l_english.yml',encoding='utf-8') as f:
            loccult=f.read()
        allines=[]
        for filename in os.listdir(fr'{gamedir}\localization\english\religion'):
            with open (os.path.join(fr'{gamedir}\localization\english\religion', filename), 'r',encoding='utf-8') as f:
                allines.append(f.read())
        allines=''.join(allines)
        with open(r'.\traits\traits.csv',encoding='utf-8') as f:
            mtraits=pd.read_csv(f,header=None)
            mtraits = mtraits.astype(str)
            mtraits=mtraits.set_index(0)
            mdictraits=mtraits.T.to_dict(orient='records')
            mdictraits=mdictraits[0]
        with open(r'.\traits\ftraits.csv',encoding='utf-8') as f:
            ftraits=pd.read_csv(f,header=None)
            ftraits = ftraits.astype(str)
            ftraits=ftraits.set_index(0)
            fdictraits=ftraits.T.to_dict(orient='records')
            fdictraits=fdictraits[0]
        with open(r'.\traits\traitcode.csv',encoding='utf-8') as f:
            traitcode=pd.read_csv(f,header=None)
            traitcode = traitcode.astype(str)
            traitcode=traitcode.set_index(0)
            traitcode=traitcode.T.to_dict(orient='records')
            traitcode=traitcode[0]
        return data,locnames,dynloc,loccult,allines,mdictraits,fdictraits,traitcode
    except(NameError,IndexError,FileNotFoundError):
        print('Invalid directories')
        return False
        pass
    


# In[ ]:


#Prompt:Directory
def loading_files():
    if os.path.isfile(r'.\pickle\json.pickle') is True and os.path.isfile(r'.\pickle\locfiles.pickle') is True and os.path.isfile(r'.\pickle\dir.pickle') is True  :
        prev=True
    else:
        prev=False
    if prev is True:
        with open(r'.\pickle\dir.pickle','rb') as f:
            jsondir=pickle.load(f)
            gamedir=pickle.load(f)
        print(f'Would you like to use your previous JSON file {jsondir}? y/n:')
        usepre=input() 
    else:
        usepre=None
    if usepre=='y':
        with open(r'.\pickle\locfiles.pickle','rb') as f:
            locnames=pickle.load(f)
            dynloc=pickle.load(f)
            loccult=pickle.load(f)
            allines=pickle.load(f)
            mdictraits=pickle.load(f)
            fdictraits=pickle.load(f)
            traitcode=pickle.load(f)
        with open(r'.\pickle\json.pickle','rb') as f:
            data=pickle.load(f)
        return data,locnames,dynloc,loccult,allines,mdictraits,fdictraits,traitcode
    elif usepre=='n':
        pass
    else:
        usepre=None
    while prev is True and usepre=='n':            
        try:
            print(r'Enter your new JSON directory:')
            jsondir = input()
            with open(jsondir,encoding='utf-8') as f:
                data=json.load(f)
            with open(r'.\pickle\locfiles.pickle','rb') as f:
                locnames=pickle.load(f)
                dynloc=pickle.load(f)
                loccult=pickle.load(f)
                allines=pickle.load(f)
                mdictraits=pickle.load(f)
                fdictraits=pickle.load(f)  
                traitcode=pickle.load(f)
            with open(r'.\pickle\json.pickle','wb') as f:
                pickle.dump(data,f)
            with open(r'.\pickle\dir.pickle','wb') as f:
                pickle.dump(jsondir,f)
                pickle.dump(gamedir,f)
            print('Changed JSON file and created new pickle binary for future use.')
            return data,locnames,dynloc,loccult,allines,mdictraits,fdictraits,traitcode
        except (FileNotFoundError, ValueError):
            print("Invalid File. Please try again.")
            continue
    while usepre is None:
        try:
            print(r'Enter your JSON savefile (eg. mysave.json):')
            jsondir = input()
            print(r'Enter your ck3 game directory (eg. C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game):')
            gamedir= input()
            if loadall(jsondir,gamedir):
                data,locnames,dynloc,loccult,allines,mdictraits,fdictraits,traitcode=loadall(jsondir,gamedir)
            else:
                continue    
            os.makedirs('pickle',exist_ok=True)
            with open(r'.\pickle\locfiles.pickle','wb') as f:
                pickle.dump(locnames,f)
                pickle.dump(dynloc,f)
                pickle.dump(loccult,f)
                pickle.dump(allines,f)
                pickle.dump(mdictraits,f)
                pickle.dump(fdictraits,f)
                pickle.dump(traitcode,f)
            with open(r'.\pickle\json.pickle','wb') as f:
                pickle.dump(data,f)
            with open(r'.\pickle\dir.pickle','wb') as f:
                pickle.dump(jsondir,f)
                pickle.dump(gamedir,f)
                
            print('Directories are saved as pickle binaries for future use')
            return data,locnames,dynloc,loccult,allines,mdictraits,fdictraits,traitcode
        except (FileNotFoundError, ValueError):
            print("One or more file directory is incorrectly inputted or invalid. Please try again.")
            continue   


# In[ ]:


def getinfo():
    while True:
        print("Type your house name:")
        dynastyname=input()
        print("Type your character's id  (Can be found by running CK3 in Debug Mode.):")
        idnum=input()
        print('Include cadet families? y/n')
        cadet=input()
        print('House Name: '+dynastyname+'\n'+'ID: '+idnum+'\n'+'Include cadet families?: '+cadet+'\n')
        print("Proceed with these inputs? y/n:")
        confirm=input()
        if confirm=="y":
            return dynastyname,idnum,cadet
        elif confirm!="y":
            continue


# In[ ]:


def variables():
    start=time.time()
    #defining variables to use
    faithde=data['religion']['faiths']
    faithre=data['religion']['religions']
    cult=data['culture_manager']['cultures']
    live=data['living']
    dead=data['dead_unprunable']
    other=data['characters']['dead_prunable']
    dyn=data['dynasties']['dynasty_house']
    title=data['landed_titles']
    skillist=['DIP ','STE ','MAR ','INT ','LEA ','PRO ']
    coafind=data['dynasties']['dynasties']
    if idnum in live:
        houseid=live[idnum]["dynasty_house"]
    elif idnum in dead:
        houseid=dead[idnum]["dynasty_house"]
    elif idnum in other:
        houseid=other[idnum]["dynasty_house"]
    else:
        print('none')
    return faithde,faithre,cult,live,dead,other,dyn,title,houseid,skillist,start,coafind


# In[ ]:


def getid():
    onlyhouse=[idnum]
    peep=[idnum]
    idlist=[houseid]
    if cadet=='y':
        bid=[i for i in dyn if "parent_dynasty_house" in dyn[i] and dyn[i]['parent_dynasty_house']==houseid]
        bid= [int(i) for i in bid]
        idlist.extend(bid)
    else:
        pass
    for i in peep:
        if peep.index(i)==0:
            pass
        elif i in live:
            if 'dynasty_house' in live[i] and live[i]["dynasty_house"] in idlist:
                onlyhouse.append(i)
            else:
                pass
        elif i in dead:
            if 'dynasty_house' in dead[i] and dead[i]["dynasty_house"] in idlist:
                onlyhouse.append(i)
            else:
                pass
        elif i in other:
            if 'dynasty_house' in other[i] and other[i]["dynasty_house"]in idlist:
                onlyhouse.append(i)
            else:
                pass
        if i in live:
            if 'dynasty_house' in live[i] and live[i]["dynasty_house"] in idlist and 'family_data' in live[i] and 'child' in live[i]['family_data']:
                livk=live[i]['family_data']['child']
                livk=list(map(str,livk))
                peep.extend(livk)
                seen = set()
                peep[:] = [item for item in peep
                                                   if item not in seen and not seen.add(item)]
            else:
                pass
        elif i in dead:
            if 'dynasty_house' in dead[i] and dead[i]["dynasty_house"] in idlist and 'family_data' in dead[i] and 'child' in dead[i]['family_data']:
                dedk=dead[i]['family_data']['child'] 
                dedk=list(map(str,dedk))
                peep.extend(dedk)
                seen = set()
                peep[:] = [item for item in peep
                                                   if item not in seen and not seen.add(item)]
            else:
                pass
        elif i in other:
            if 'dynasty_house' in other[i] and other[i]["dynasty_house"] in idlist and 'family_data' in other[i] and 'child' in other[i]['family_data']:
                etck=other[i]['family_data']['child']
                etck=list(map(str,etck))
                peep.extend(etck)
                seen = set()
                peep[:] = [item for item in peep
                                                   if item not in seen and not seen.add(item)]
            else:
                pass


    #sort to order all people. Use for person data
    setli=set(peep)
    setli=list(map(int,setli))
    setli=(sorted(setli))
    setlist=list(setli)
    setlist=list(map(str,setlist))
    #for changing id length
    maxlen=len(max(setlist, key = len))

    #sort to order. use for famdata and marrydata
    setli2=set(onlyhouse)
    setli2=list(map(int,setli2))
    setli2=(sorted(setli2))
    setlist2=list(setli2)
    setlist2=list(map(str,setlist2))
    return setlist,setlist2,maxlen


# In[ ]:


def getfamily():
    famidlist=[]
    for i in range(len(setlist)):
        i, full_format(i, d=4)
        fid1=full_format(i, d=4)
        fid2=famidlist.append(fid1)
    marrydata= pd.DataFrame(columns=['marriage','husband','wife'])
    famdata= pd.DataFrame(columns=['family','child'])
    for i in setlist2:
        if i in live and 'family_data' in live[i] and 'child' in live[i]['family_data'] and 'female'in live[i]:
            famid=famidlist[0]
            famidlist.pop(0)
            husband=''
            wife=i
            d2={'marriage':famid,'husband':husband,'wife':wife}
            d3= {'family': famid, 'child': live[i]['family_data']['child']}
            marrydata2 = pd.DataFrame(data=d2,index=[0])
            famdata2 = pd.DataFrame(data=d3)
            marrydata=marrydata.append(marrydata2,ignore_index=True)
            famdata=famdata.append(famdata2,ignore_index=True)
        elif i in live and 'family_data' in live[i] and 'child' in live[i]['family_data']:
            famid=famidlist[0]
            famidlist.pop(0)
            husband=i
            wife=''
            d2={'marriage':famid,'husband':husband,'wife':wife}
            d3= {'family': famid, 'child': live[i]['family_data']['child']}
            marrydata2 = pd.DataFrame(data=d2,index=[0])
            famdata2 = pd.DataFrame(data=d3)
            marrydata=marrydata.append(marrydata2,ignore_index=True)
            famdata=famdata.append(famdata2,ignore_index=True)
        elif i in dead and 'family_data' in dead[i] and 'child' in dead[i]['family_data'] and 'female'in dead[i]:
            famid=famidlist[0]
            famidlist.pop(0)
            husband=''
            wife=i
            d2={'marriage':famid,'husband':husband,'wife':wife}
            d3= {'family': famid, 'child': dead[i]['family_data']['child']}
            marrydata2 = pd.DataFrame(data=d2,index=[0])
            famdata2 = pd.DataFrame(data=d3)
            marrydata=marrydata.append(marrydata2,ignore_index=True)
            famdata=famdata.append(famdata2,ignore_index=True)
        elif i in dead and 'family_data' in dead[i] and 'child' in dead[i]['family_data']:
            famid=famidlist[0]
            famidlist.pop(0)
            husband=i
            wife=''
            d2={'marriage':famid,'husband':husband,'wife':wife}
            d3= {'family': famid, 'child': dead[i]['family_data']['child']}
            marrydata2 = pd.DataFrame(data=d2,index=[0])
            famdata2 = pd.DataFrame(data=d3)
            marrydata=marrydata.append(marrydata2,ignore_index=True)
            famdata=famdata.append(famdata2,ignore_index=True)
        elif i in other and 'family_data' in other[i] and 'child' in other[i]['family_data'] and 'female'in other[i]:
            famid=famidlist[0]
            famidlist.pop(0)
            husband=''
            wife=i
            d2={'marriage':famid,'husband':husband,'wife':wife}
            d3= {'family': famid, 'child': other[i]['family_data']['child']}
            marrydata2 = pd.DataFrame(data=d2,index=[0])
            famdata2 = pd.DataFrame(data=d3)
            marrydata=marrydata.append(marrydata2,ignore_index=True)
            famdata=famdata.append(famdata2,ignore_index=True)
        elif i in other and 'family_data' in other[i] and 'child' in other[i]['family_data']:
            famid=famidlist[0]
            famidlist.pop(0)
            husband=i
            wife=''
            d2={'marriage':famid,'husband':husband,'wife':wife}
            d3= {'family': famid, 'child': other[i]['family_data']['child']}
            marrydata2 = pd.DataFrame(data=d2,index=[0])
            famdata2 = pd.DataFrame(data=d3)
            marrydata=marrydata.append(marrydata2,ignore_index=True)
            famdata=famdata.append(famdata2,ignore_index=True)
        else:
            pass
    return marrydata,famdata


# In[ ]:


def getperson():
    allist=[]
    allfaith=[]
    faithpic={}
    traitpic={}
    dyncoapic={}
    titlecoapic={}
    dynprespic={}
    titlerankpic={}
    #-------------------------------------------LIVING-------------------------------------------------------
    for i in setlist:
        if i in live:
    # LIVE NAME
            itername=live[i]['first_name']
            if re.search(fr'(?<=\s){itername}\b',locnames) is not None:
                itername=re.findall(fr'(?<=\s){itername}\b:.*"(.*)"',locnames)
                itername=itername[0]
            accented='\n'+'Name: '+itername
            itername= unidecode.unidecode(itername)
            itername=itername.title()

    # LIVE DYNASTY 
            if 'dynasty_house' in live[i]:
                iterhouse1=live[i]['dynasty_house']                    
                if 'key' in dyn[str(iterhouse1)]:
                    iterhouse2=dyn[str(iterhouse1)]['key']
                    iterhouse3=re.findall('(?<=_)[^_]+$',iterhouse2)
                    iterhouse3=iterhouse3[0]
                    iterhouse3=iterhouse3.title()
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
                elif 'name' in dyn[str(iterhouse1)]:
                    iterhouse2=dyn[str(iterhouse1)]['name']
                    iterhouse3=re.findall(fr'\b{iterhouse2}\b:.*"(.*)"',dynloc)
                    iterhouse3=iterhouse3[0]
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
                elif 'localized_name' in dyn[str(iterhouse1)]:
                    iterhouse3=dyn[str(iterhouse1)]['localized_name']
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
                    
#LIVE COA           
                
                if 'coat_of_arms_id' in dyn[f'{iterhouse1}']:
                    coa_id=dyn[f'{iterhouse1}']['coat_of_arms_id']
                    dyncoapic[i.zfill(maxlen)]=str(coa_id)
                    dynpres=dyn[f'{iterhouse1}']['dynasty']
#LIVE DYN PRES                         
                    if str(coa_id) not in dynprespic:
                        dynacc=coafind[f'{dynpres}']['prestige']['accumulated']
                        dynprespic[str(coa_id)]=dynacc                              
             
                else:
                    nestdyn=dyn[f'{iterhouse1}']['dynasty']
                    if 'coat_of_arms_id' in coafind[f'{nestdyn}']:
                        coa_id=coafind[f'{nestdyn}']['coat_of_arms_id']                            
                        dyncoapic[i.zfill(maxlen)]=str(coa_id)
                        
                        if str(coa_id) not in dynprespic:
                            dynacc=coafind[f'{nestdyn}']['prestige']['accumulated']
                            dynprespic[str(coa_id)]=dynacc                       
            else:
                iterhouse3=''
    # LIVE GENDER
            if 'sexuality' in live[i]:
                sexo=live[i]['sexuality']
                sexo=re.sub('as','Asexual',sexo)
                sexo=re.sub('bi','Bisexual',sexo)
                sexo=re.sub('ho','Homosexual',sexo)
            else: 
                sexo='Heterosexual'
            if 'female' in live[i]:
                sex='Female'
            else:
                sex='Male'
            gendernote='\n'+'Sex: '+sex+'\n'+'Sexual Orientation: '+sexo
    #LIVE TITLE
            if 'landed_data' in live[i] and 'domain' in live[i]['landed_data']:
                itertitle=live[i]['landed_data']['domain'][0]
                iterrank=title['landed_titles'][str(itertitle)]['key']
#LIVE TITLE COA
                titlecoa=title['landed_titles'][str(itertitle)]['coat_of_arms_id']
                titlecoapic[i.zfill(maxlen)]=str(titlecoa)                
                iterrank=re.sub('(.)_.*',r'\1',iterrank)
                if str(coa_id) not in titlerankpic:
                    titlerankpic[str(titlecoa)]=iterrank
                itertitle=title['landed_titles'][str(itertitle)]['name']
                
                if 'b' in iterrank and sex!='Female':
                    iterrank="Baron of "
                    
                elif 'b' in iterrank and sex=='Female':
                    iterrank="Baroness of "
                elif 'c' in iterrank and sex!='Female':
                    iterrank="Count of "
                elif 'c' in iterrank and sex=='Female':
                    iterrank="Countess of "
                elif 'd' in iterrank and sex!='Female':
                    iterrank="Duke of "
                elif 'd' in iterrank and sex=='Female':
                    iterrank="Duchess of "
                elif 'k' in iterrank and sex!='Female':
                    iterrank="King of "
                elif 'k' in iterrank and sex=='Female':
                    iterrank="Queen of "
                elif 'e' in iterrank and sex!='Female':
                    iterrank="Emperor of "
                elif 'e' in iterrank and sex=='Female':
                    iterrank="Empress of "
                elif 'x' in iterrank:
                    iterrank="Leader of the " 
                else: 
                    iterrank="Titled"
                itertitle=iterrank+itertitle
                titlenote='\n'+'Title: '+itertitle
                itertitle= unidecode.unidecode(itertitle)
                itertitle=itertitle.title()
            
            else:
                itertitle=''
                titlenote=''
    # LIVE BIRTH
            birth=live[i]['birth']
            birth=birth.replace(".", "-")
            birthnote='\n'+'Born: '+birth
    # LIVE DEATH
            death=''

    # LIVE Skills AND TRAITS
            traitpic[i.zfill(maxlen)]=[]
            if 'skill' in live[i]:
                skill=[live[i]['skill'][j] for j in range(6)]
                skill=[str(skillist[x])+str(skill[x]) for x in range(6)]
                skill='Skills: '+str(skill)
            else:
                skill=[]
            if 'traits' in live[i]:
                traits=live[i]['traits']
                traits=set(traits)
                traits=(sorted(traits))
                traits=list(traits)
                traits=list(map(str,traits))
                traitxml=[traitcode.get(item,item) for item in traits]
                traitpic[i.zfill(maxlen)]=traitxml
                if sex=='Female':
                    traits=[ fdictraits.get(item,item) for item in traits ]
                else:
                    traits=[ mdictraits.get(item,item) for item in traits ]
                traits='Traits: '+str(traits)
            else:
                traits=[]
            if 'recessive_traits' in live[i]:
                retraits=live[i]['recessive_traits']
                retraits=set(retraits)
                retraits=(sorted(retraits))
                retraits=list(retraits)
                retraits=list(map(str,retraits))
                traitxml2=[traitcode.get(item,item) for item in retraits]
                traitpic[i.zfill(maxlen)].extend(traitxml2)
                if sex=='Female':
                    retraits=[ fdictraits.get(item,item) for item in retraits ]
                else:
                    retraits=[ mdictraits.get(item,item) for item in retraits ]
                retraits='Inherited Traits: '+str(retraits) 
            else:
                retraits=[]
            if '[]' in traits:
                traits=''
            if '[]' in retraits:
                retraits=''
            if bool(traits) is True and bool(retraits) is True:
                d='\n'+traits+'\n'+retraits
            elif bool(traits) is True and bool(retraits) is False:
                d='\n'+traits
            elif bool(traits) is False and bool(retraits) is True:
                d='\n'+retraits
            elif bool(traits) is False and bool(retraits) is False:
                d=''
            if bool(d) is False:
                satli='\n'+skill
            else:
                satli='\n'+skill+d
    # LIVE FAITH

            if 'faith' in live[i]:
                pfaith=live[i]['faith']
                if 'name' in faithde[str(pfaith)]:
                    mycon=faithde[str(pfaith)]['icon']
                    faithpic[i.zfill(maxlen)]=mycon
                    myfaith=(faithde[str(pfaith)]['name'])
                    myfaith='Faith: '+myfaith
                else:
                    mycon=faithde[str(pfaith)]['icon']
                    faithpic[i.zfill(maxlen)]=mycon
                    faithname=faithde[fr'{pfaith}']['template']
                    myfaith='Faith: '+((re.findall(fr'{faithname}\b:.*"(.*)"',allines))[0])

                basename=faithre[str(faithde[fr'{pfaith}']['religion'])]['template']           
                mybase='Religion: '+((re.findall(fr'{basename}\b:.*"(.*)"',allines))[0])
                faith='\n'+myfaith+'\n'+mybase
                if myfaith not in allfaith:
                    allfaith.append(myfaith)
                else:
                    pass


            else:
                faith=''
    # LIVE CULTURE
            if 'culture' in live[i]:
                pcult=live[i]['culture']
                cultem=cult[str(pcult)]['culture_template']
                culture=(re.findall(fr'\b{cultem}\b:.*"(.*)"',loccult))[0]
                culture='\n'+'Culture: '+culture
            else:
                culture=''


    # LIVE COMBINE
            notes='Game ID: '+i+titlenote+accented+birthnote+satli+faith+culture+gendernote
            combine=i,i,iterhouse3,itername,sex,birth,death,itertitle,notes
            allist.append(combine)
            print(f'{setlist.index(i)+1}/{len(setlist)} CHARACTERS PROCESSED')
    #-------------------------------------------DEAD-------------------------------------------------------
        elif i in dead:
    # DEAD NAME
            itername=dead[i]['first_name']
            if re.search(fr'(?<=\s){itername}\b',locnames) is not None:
                itername=re.findall(fr'(?<=\s){itername}\b:.*"(.*)"',locnames)
                itername=itername[0]
            accented='\n'+'Name: '+itername
            itername= unidecode.unidecode(itername)
            itername=itername.title()
    # DEAD DYNASTY
            if 'dynasty_house' in dead[i]:
                iterhouse1=dead[i]['dynasty_house']                    
                if 'key' in dyn[str(iterhouse1)]:
                    iterhouse2=dyn[str(iterhouse1)]['key']
                    iterhouse3=re.findall('(?<=_)[^_]+$',iterhouse2)
                    iterhouse3=iterhouse3[0]
                    iterhouse3=iterhouse3.title()
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
                elif 'name' in dyn[str(iterhouse1)]:
                    iterhouse2=dyn[str(iterhouse1)]['name']
                    iterhouse3=re.findall(fr'\b{iterhouse2}\b:.*"(.*)"',dynloc)
                    iterhouse3=iterhouse3[0]
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)  
                    iterhouse3=iterhouse3.title()
                elif 'localized_name' in dyn[str(iterhouse1)]:
                    iterhouse3=dyn[str(iterhouse1)]['localized_name']
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
#DEAD COA           
                
                if 'coat_of_arms_id' in dyn[f'{iterhouse1}']:
                    coa_id=dyn[f'{iterhouse1}']['coat_of_arms_id']
                    dyncoapic[i.zfill(maxlen)]=str(coa_id)
                    dynpres=dyn[f'{iterhouse1}']['dynasty']
#DEAD DYN PRES                         
                    if str(coa_id) not in dynprespic:
                        dynacc=coafind[f'{dynpres}']['prestige']['accumulated']
                        dynprespic[str(coa_id)]=dynacc                              
             
                else:
                    nestdyn=dyn[f'{iterhouse1}']['dynasty']
                    if 'coat_of_arms_id' in coafind[f'{nestdyn}']:
                        coa_id=coafind[f'{nestdyn}']['coat_of_arms_id']                            
                        dyncoapic[i.zfill(maxlen)]=str(coa_id)
                        
                        if str(coa_id) not in dynprespic:
                            dynacc=coafind[f'{nestdyn}']['prestige']['accumulated']
                            dynprespic[str(coa_id)]=dynacc   
            else:
                iterhouse3=''
    # DEAD GENDER
            if 'sexuality' in dead[i]:
                sexo=dead[i]['sexuality']
                sexo=re.sub('as','Asexual',sexo)
                sexo=re.sub('bi','Bisexual',sexo)
                sexo=re.sub('ho','Homosexual',sexo)
            else:
                sexo='Heterosexual'
            if 'female' in dead[i]:
                sex='Female'
            else:
                sex='Male'
            gendernote='\n'+'Sex: '+sex+'\n'+'Sexual Orientation: '+sexo
    # DEAD TITLE
            if 'domain' in dead[i]['dead_data']:
                itertitle=dead[i]['dead_data']['domain'][0]
                iterrank=title['landed_titles'][str(itertitle)]['key']
                
#DEAD TITLE COA
                titlecoa=title['landed_titles'][str(itertitle)]['coat_of_arms_id']
                titlecoapic[i.zfill(maxlen)]=str(titlecoa)  
                iterrank=re.sub('(.)_.*',r'\1',iterrank)
                if str(coa_id) not in titlerankpic:
                    titlerankpic[str(titlecoa)]=iterrank
                itertitle=title['landed_titles'][str(itertitle)]['name']
                if 'b' in iterrank and sex!='Female':
                    iterrank="Baron of "
                elif 'b' in iterrank and sex=='Female':
                    iterrank="Baroness of "
                elif 'c' in iterrank and sex!='Female':
                    iterrank="Count of "
                elif 'c' in iterrank and sex=='Female':
                    iterrank="Countess of "
                elif 'd' in iterrank and sex!='Female':
                    iterrank="Duke of "
                elif 'd' in iterrank and sex=='Female':
                    iterrank="Duchess of "
                elif 'k' in iterrank and sex!='Female':
                    iterrank="King of "
                elif 'k' in iterrank and sex=='Female':
                    iterrank="Queen of "
                elif 'e' in iterrank and sex!='Female':
                    iterrank="Emperor of "
                elif 'e' in iterrank and sex=='Female':
                    iterrank="Empress of "
                elif 'x' in iterrank:
                    iterrank="Leader of the " 
                else: 
                    iterrank="Titled"
                itertitle=iterrank+itertitle
                titlenote='\n'+'Title: '+itertitle
                itertitle= unidecode.unidecode(itertitle)
                itertitle=itertitle.title()
            else:
                itertitle=''
                titlenote=''
    # DEAD BIRTH
            birth=dead[i]['birth']
            birth=birth.replace(".", "-")
            birthnote='\n'+'Born: '+birth
    # DEAD DEATH
            death=dead[i]['dead_data']['date']
            death=death.replace(".","-")
            deathnote='\n'+'Died: '+death


    # DEAD Skills AND TRAITS
            traitpic[i.zfill(maxlen)]=[]
            if 'skill' in dead[i]:
                skill=[dead[i]['skill'][j] for j in range(6)]
                skill=[str(skillist[x])+str(skill[x]) for x in range(6)]
                skill='Skills: '+str(skill)
            else:
                skill=[]
            if 'traits' in dead[i]:
                traits=dead[i]['traits']
                traits=set(traits)
                traits=(sorted(traits))
                traits=list(traits)  
                traits=list(map(str,traits))
                traitxml=[traitcode.get(item,item) for item in traits]
                traitpic[i.zfill(maxlen)]=traitxml
                if sex=='Female':
                    traits=[ fdictraits.get(item,item) for item in traits ]
                else:
                    traits=[ mdictraits.get(item,item) for item in traits ]
                traits='Traits: '+str(traits)
            else:
                traits=[]
            if 'recessive_traits' in dead[i]:
                retraits=dead[i]['recessive_traits']
                retraits=set(retraits)
                retraits=(sorted(retraits))
                retraits=list(retraits)
                retraits=list(map(str,retraits))
                traitxml2=[traitcode.get(item,item) for item in retraits]
                traitpic[i.zfill(maxlen)].extend(traitxml2)
                if sex=='Female':
                    retraits=[ fdictraits.get(item,item) for item in retraits ]
                else:
                    retraits=[ mdictraits.get(item,item) for item in retraits ]
                retraits='Inherited Traits: '+str(retraits)
            else:
                retraits=[]
            if '[]' in traits:
                traits=''
            if '[]' in retraits:
                retraits=''
            if bool(traits) is True and bool(retraits) is True:
                d='\n'+traits+'\n'+retraits
            elif bool(traits) is True and bool(retraits) is False:
                d='\n'+traits
            elif bool(traits) is False and bool(retraits) is True:
                d='\n'+retraits
            elif bool(traits) is False and bool(retraits) is False:
                d=''
            if bool(d) is False:
                satli='\n'+skill
            else:
                satli='\n'+skill+d
    # DEAD FAITH

            if 'faith' in dead[i]:
                pfaith=dead[i]['faith']
                if 'name' in faithde[str(pfaith)]:
                    mycon=faithde[str(pfaith)]['icon']
                    faithpic[i.zfill(maxlen)]=mycon
                    myfaith=(faithde[str(pfaith)]['name'])
                    myfaith='Faith: '+myfaith
                else:
                    mycon=faithde[str(pfaith)]['icon']
                    faithpic[i.zfill(maxlen)]=mycon
                    faithname=faithde[fr'{pfaith}']['template']
                    myfaith='Faith: '+((re.findall(fr'{faithname}\b:.*"(.*)"',allines))[0])

                basename=faithre[str(faithde[fr'{pfaith}']['religion'])]['template']
                mybase='Religion: '+((re.findall(fr'{basename}\b:.*"(.*)"',allines))[0])
                faith='\n'+myfaith+'\n'+mybase
                if myfaith not in allfaith:
                    allfaith.append(myfaith)
                else:
                    pass

            else:
                faith=''
    # DEAD CULTURE
            if 'culture' in dead[i]:
                pcult=dead[i]['culture']
                cultem=cult[str(pcult)]['culture_template']
                culture=(re.findall(fr'\b{cultem}\b:.*"(.*)"',loccult))[0]
                culture='\n'+'Culture: '+culture
            else:
                culture=''
    #DEAD CAUSE OF DEATH
            if 'reason' in dead[i]['dead_data']:
                reason=dead[i]['dead_data']['reason']
                reason=re.sub('wounded_1','Wounded',reason)
                reason=re.sub('wounded_2','Severely Injured',reason)
                reason=re.sub('wounded_3','Brutally Mauled',reason)
                reason=re.sub('death(.*)',r'\1',reason)
                reason=reason.title()
                reason=re.sub('(?<=\w)_',' ',reason)
                reason=re.sub('_','',reason)
                reason=re.sub(' Passive','',reason)
                reason='\n'+'Cause of Death: '+reason
            else:
                reason=''
    # DEAD COMBINE
            notes='Game ID: '+i+titlenote+accented+birthnote+deathnote+reason+satli+faith+culture+gendernote
            combine=i,i,iterhouse3,itername,sex,birth,death,itertitle,notes
            allist.append(combine)
            print(f'{setlist.index(i)+1}/{len(setlist)} CHARACTERS PROCESSED')
    #-------------------------------------------OTHER-------------------------------------------------------
        elif i in other:
    # OTHER NAME
            itername=other[i]['first_name']
            if re.search(fr'(?<=\s){itername}\b',locnames) is not None:
                itername=re.findall(fr'(?<=\s){itername}\b:.*"(.*)"',locnames)
                itername=itername[0]
            accented='\n'+'Name: '+itername
            itername= unidecode.unidecode(itername)
            itername=itername.title()
    # OTHER DYNASTY
            if 'dynasty_house' in other[i]:
                iterhouse1=other[i]['dynasty_house']
                if 'key' in dyn[str(iterhouse1)]:
                    iterhouse2=dyn[str(iterhouse1)]['key']
                    iterhouse3=re.findall('(?<=_)[^_]+$',iterhouse2)
                    iterhouse3=iterhouse3[0]
                    iterhouse3=iterhouse3.title()
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
                elif 'name' in dyn[str(iterhouse1)]:
                    iterhouse2=dyn[str(iterhouse1)]['name']
                    iterhouse3=re.findall(fr'\b{iterhouse2}\b:.*"(.*)"',dynloc)
                    iterhouse3=iterhouse3[0]
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
                elif 'localized_name' in dyn[str(iterhouse1)]:
                    iterhouse3=dyn[str(iterhouse1)]['localized_name']
                    accented=accented+' '+iterhouse3
                    iterhouse3= unidecode.unidecode(iterhouse3)
                    iterhouse3=iterhouse3.title()
#OTHER COA           
                
                if 'coat_of_arms_id' in dyn[f'{iterhouse1}']:
                    coa_id=dyn[f'{iterhouse1}']['coat_of_arms_id']
                    dyncoapic[i.zfill(maxlen)]=str(coa_id)
                    dynpres=dyn[f'{iterhouse1}']['dynasty']
#OTHER DYN PRES                         
                    if str(coa_id) not in dynprespic:
                        dynacc=coafind[f'{dynpres}']['prestige']['accumulated']
                        dynprespic[str(coa_id)]=dynacc                              
             
                else:
                    nestdyn=dyn[f'{iterhouse1}']['dynasty']
                    if 'coat_of_arms_id' in coafind[f'{nestdyn}']:
                        coa_id=coafind[f'{nestdyn}']['coat_of_arms_id']                            
                        dyncoapic[i.zfill(maxlen)]=str(coa_id)
                        
                        if str(coa_id) not in dynprespic:
                            dynacc=coafind[f'{nestdyn}']['prestige']['accumulated']
                            dynprespic[str(coa_id)]=dynacc   
            else:
                iterhouse3=''
    # OTHER GENDER
            if 'sexuality' in other[i]:
                sexo=other[i]['sexuality']
                sexo=re.sub('as','Asexual',sexo)
                sexo=re.sub('bi','Bisexual',sexo)
                sexo=re.sub('ho','Homosexual',sexo)
            else:
                sexo='Heterosexual'
            if 'female' in other[i]:
                sex='Female'
            else:
                sex='Male'
            gendernote='\n'+'Sex: '+sex+'\n'+'Sexual Orientation: '+sexo
    # OTHER TITLE
            if 'domain' in other[i]['dead_data']:
                itertitle=other[i]['dead_data']['domain'][0]
                iterrank=title['landed_titles'][str(itertitle)]['key']
                
#OTHER TITLE COA
                titlecoa=title['landed_titles'][str(itertitle)]['coat_of_arms_id']
                titlecoapic[i.zfill(maxlen)]=str(titlecoa) 
                iterrank=re.sub('(.)_.*',r'\1',iterrank)
                if str(coa_id) not in titlerankpic:
                    titlerankpic[str(titlecoa)]=iterrank
                itertitle=title['landed_titles'][str(itertitle)]['name']
                if 'b' in iterrank and sex!='Female':
                    iterrank="Baron of "
                elif 'b' in iterrank and sex=='Female':
                    iterrank="Baroness of "
                elif 'c' in iterrank and sex!='Female':
                    iterrank="Count of "
                elif 'c' in iterrank and sex=='Female':
                    iterrank="Countess of "
                elif 'd' in iterrank and sex!='Female':
                    iterrank="Duke of "
                elif 'd' in iterrank and sex=='Female':
                    iterrank="Duchess of "
                elif 'k' in iterrank and sex!='Female':
                    iterrank="King of "
                elif 'k' in iterrank and sex=='Female':
                    iterrank="Queen of "
                elif 'e' in iterrank and sex!='Female':
                    iterrank="Emperor of "
                elif 'e' in iterrank and sex=='Female':
                    iterrank="Empress of "
                elif 'x' in iterrank:
                    iterrank="Leader of the " 
                else: 
                    iterrank="Titled"
                itertitle=iterrank+itertitle
                titlenote='\n'+'Title: '+itertitle
                itertitle= unidecode.unidecode(itertitle)
                itertitle=itertitle.title()
            else:
                itertitle=''
                titlenote=''
    # OTHER BIRTH
            birth=other[i]['birth']
            birth=birth.replace(".", "-")
            birthnote='\n'+'Born: '+birth
    # OTHER DEATH
            death=other[i]['dead_data']['date']
            death=death.replace(".","-")
            deathnote='\n'+'Died: '+death

    # OTHER Skills AND TRAITS
            traitpic[i.zfill(maxlen)]=[]
            if 'skill' in other[i]:
                skill=[other[i]['skill'][j] for j in range(6)]
                skill=[str(skillist[x])+str(skill[x]) for x in range(6)]
                skill='Skills: '+str(skill)
            else:
                skill=[]
            if 'traits' in other[i]:
                traits=other[i]['traits']
                traits=set(traits)
                traits=(sorted(traits))
                traits=list(traits)
                traits=list(map(str,traits))
                traitxml=[traitcode.get(item,item) for item in traits]
                traitpic[i.zfill(maxlen)]=traitxml
                if sex=='Female':
                    traits=[ fdictraits.get(item,item) for item in traits ]
                else:
                    traits=[ mdictraits.get(item,item) for item in traits ]
                traits='Traits: '+str(traits)

            else:
                traits=[]
            if 'recessive_traits' in other[i]:
                retraits=other[i]['recessive_traits']
                retraits=set(retraits)
                retraits=(sorted(retraits))
                retraits=list(retraits)
                retraits=list(map(str,retraits))
                traitxml2=[traitcode.get(item,item) for item in retraits]
                traitpic[i.zfill(maxlen)].extend(traitxml2)
                if sex=='Female':
                    retraits=[ fdictraits.get(item,item) for item in retraits ]
                else:
                    retraits=[ mdictraits.get(item,item) for item in retraits ]
                retraits='Inherited Traits: '+str(retraits)

            else:
                retraits=[]
            if '[]' in traits:
                traits=''
            if '[]' in retraits:
                retraits=''
            if bool(traits) is True and bool(retraits) is True:
                d='\n'+traits+'\n'+retraits
            elif bool(traits) is True and bool(retraits) is False:
                d='\n'+traits
            elif bool(traits) is False and bool(retraits) is True:
                d='\n'+retraits
            elif bool(traits) is False and bool(retraits) is False:
                d=''
            if bool(d) is False:
                satli='\n'+skill
            else:
                satli='\n'+skill+d

    # OTHER FAITH

            if 'faith' in other[i]:
                pfaith=other[i]['faith']
                if 'name' in faithde[str(pfaith)]:
                    mycon=faithde[str(pfaith)]['icon']
                    faithpic[i.zfill(maxlen)]=mycon
                    myfaith=(faithde[str(pfaith)]['name'])
                    myfaith='Faith: '+myfaith
                else:
                    mycon=faithde[str(pfaith)]['icon']
                    faithpic[i.zfill(maxlen)]=mycon
                    faithname=faithde[fr'{pfaith}']['template']
                    myfaith='Faith: '+((re.findall(fr'{faithname}\b:.*"(.*)"',allines))[0])

                basename=faithre[str(faithde[fr'{pfaith}']['religion'])]['template']
                mybase='Religion: '+((re.findall(fr'{basename}\b:.*"(.*)"',allines))[0])
                faith='\n'+myfaith+'\n'+mybase
                if myfaith not in allfaith:
                    allfaith.append(myfaith)
                else:
                    pass
            else:
                faith=''

    # OTHER CULTURE
            if 'culture' in other[i]:
                pcult=other[i]['culture']
                cultem=cult[str(pcult)]['culture_template']
                culture=(re.findall(fr'\b{cultem}\b:.*"(.*)"',loccult))[0]
                culture='\n'+'Culture: '+culture
            else:
                culture=''
    #OTHER CAUSE OF DEATH
            if 'reason' in other[i]['dead_data']:
                reason=other[i]['dead_data']['reason']
                reason=re.sub('wounded_1','Wounded',reason)
                reason=re.sub('wounded_2','Severely Injured',reason)
                reason=re.sub('wounded_3','Brutally Mauled',reason)
                reason=re.sub('death(.*)',r'\1',reason)
                reason=reason.title()
                reason=re.sub('(?<=\w)_',' ',reason)
                reason=re.sub('_','',reason)
                reason=re.sub(' Passive','',reason)
                reason='\n'+'Cause of Death: '+reason
            else:
                reason=''
    # OTHER COMBINE
            notes='Game ID: '+i+titlenote+accented+birthnote+deathnote+reason+satli+faith+culture+gendernote
            combine=i,i,iterhouse3,itername,sex,birth,death,itertitle,notes
            allist.append(combine)
            print(f'{setlist.index(i)+1}/{len(setlist)} CHARACTERS PROCESSED')
    traitpic={k: v for k, v in traitpic.items() if v}
    with open(r'.\pickle\pic.pickle','wb') as f:
        pickle.dump(traitpic,f)
        pickle.dump(faithpic,f)
        pickle.dump(dyncoapic,f)
        pickle.dump(titlecoapic,f)
        pickle.dump(dynprespic,f)
        pickle.dump(titlerankpic,f)    
    print('Pickled image-character relationship for step 3')
    print('Finished Exporting ')
    return allist


# In[ ]:


def maketable():
    #Adding to table
    print('Finishing Touches...')
    person=pd.DataFrame(columns=['grampsid','person','surname','given','gender','birth date','death date','title','note'],data=allist)
    person=person.replace("\'","",regex=True)
    person=person.replace("\[","",regex=True)
    person=person.replace("\]","",regex=True)
    person['grampsid'] = person['grampsid'].apply(lambda x: x.zfill(maxlen))
    d4={'grampsid':'','person':'','surname':'','given':'','gender':'','birth date':'','death date':'','title':'','note':''}
    person=person.append(d4,ignore_index=True)
    d5={'marriage':'','husband':'','wife':''}
    marry=marrydata.append(d5,ignore_index=True)
    person.to_csv(f"{dynastyname}_tree.csv",encoding="utf-8-sig",index=False)
    marry.to_csv(f"{dynastyname}_tree.csv", header=True, mode = 'a',index=False)
    famdata.to_csv(f"{dynastyname}_tree.csv", header=True, mode = 'a',index=False)
    end = time.time()
    return end
    print('\nDone!')


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


# In[ ]:


def tojson():
#Identifying save type
    while True:
        print('Input whether the file is a normal (n) or ironman (i) save:')
        savetype=input()
        if savetype=='i':
            print('Enter the name of your .ck3 ironman save file (eg. savename.ck3):')
            ck3i=input()
            if os.path.isfile(ck3i) is True:
                ck3n=''
                ck3json=os.path.splitext(ck3i)[0]+'.json'
                break
            else:
                print('Invalid file. Please try again.')
                continue
        elif savetype=='n':
            print('Enter the name of your .ck3 normal save file (eg. savename.ck3):')
            ck3n=input()
            if os.path.isfile(ck3n) is True:
                ck3i=''
                ck3json=os.path.splitext(ck3n)[0]+'.json'
                break
            else:
                print('Invalid file. Please try again.')
                continue
            break
        else:
            continue

    start = time.time()
#automatically unzip ck3 normal save.
    if bool(ck3n) is True:
        try:
            with zipfile.ZipFile(ck3n, 'r') as zip_ref:
                zip_ref.extractall()
                gamestateog=zip_ref.namelist()
                gamestatenew=gamestateog[0]
                preextracted=False
        except zipfile.BadZipfile:
            print ("File is already unzipped")
            gamestatenew=ck3n
            preextracted=True
            pass
        except:
            print("An unexpected error has occurred")
            input()
            raise 
    else:
        ironman=ck3i

#Convert to JSON using ck3json program
    try:
        if bool(ck3n) is True:
            print('File is being converted to JSON...')
            p1=(subprocess.run(fr'ck3json "{gamestatenew}"',shell=True,capture_output=True))
            raw=p1.stdout.decode()

        else:
            print('File is being converted to JSON...')
            p1=(subprocess.run(fr'ck3json "{ironman}" ck3bin',shell=True,capture_output=True))
            raw=p1.stdout.decode()

        if p1.returncode==0 and bool(ck3n) is True:
            if preextracted is False:
                os.remove(gamestatenew)
            else:
                pass
        elif p1.returncode==0 and bool(ck3i) is True:
            pass
        elif p1.returncode!=0 and bool(ck3n) is True :
            print(p1.stderr)
            print('\nFailed to convert file to JSON. The converter may not be compatible with your save version or your save has invalid characters. Please refer to the README file for further instructions')
            if preextracted is False:
                os.remove(gamestatenew)
            raise Exception('An error has occurred')   
        elif p1.returncode!=0 and bool(ck3i) is True:
            print(p1.stderr)
            print('\nFailed to convert file to JSON. The converter may not be compatible with your save version or your save has invalid characters. Please refer to README file for further instructions.')
            raise Exception('An error has occurred')   
    except Exception as e:
        print('An error has occurred')
#sub all special characters
    raw=re.sub(r'[\x00-\x1F]+',' ', raw)
    with open(ck3json,'+w',encoding='utf-8') as f:
        json.dump((json.loads(raw,object_pairs_hook=parse_object_pairs)),f)
    end = time.time()
    timer(start,end)


# In[ ]:



def with_icons():
#get traits/faith-idnum relationship
    with open(r'.\pickle\pic.pickle','rb') as f:
        traitpic=pickle.load(f)
        faithpic=pickle.load(f)
        dyncoapic=pickle.load(f)
        titlecoapic=pickle.load(f)
        dynprespic=pickle.load(f)
        titlerankpic=pickle.load(f)
    with open(r'.\pickle\dir.pickle','rb') as f:
        jsondir=pickle.load(f)
        gamedir=pickle.load(f)

 #Prompt to get csv and gramps path       
    while True:
        if os.path.isfile(r'.\pickle\grampsdir.pickle') is True:
            print('Using previously entered gramps directory')
            with open(r'.\pickle\grampsdir.pickle','rb') as f:
                gramps=pickle.load(f)
                gramps=gramps+'\gramps'
        elif os.path.isdir(r'.\pickle\grampsdir.pickle') is False:
            print('Enter your gramps directory (eg. C:\Program Files\GrampsAIO64-5.1.3):')
            gramps=input()
            if os.path.isdir(gramps) is True:
                with open(r'.\pickle\grampsdir.pickle','wb') as f:
                    pickle.dump(gramps,f)
                print('Saved gramps directory as pickle binary for subsequent use')
                gramps=gramps+'\gramps'
            else:
                print('Invalid directory')
                continue
        print('Enter your CSV file:')
        outcsv=input()

        if os.path.isfile(outcsv) is True:
            outgramps=re.sub('(.*).csv',r'\1.gramps',outcsv)
            housepng=re.sub('(.*).csv',r'\1',outcsv)
            break
        else:
            print('Invalid directory')
            continue
#export to workable xml
    p1=(subprocess.run(fr'"{gramps}" -C Anytree -i "{outcsv}" -e "{outgramps}"',shell=True,capture_output=True,input=b'yes')) 
    error=re.sub('\n.*Gtk-WARNING.*\n','',p1.stderr.decode())
    print(error)
    with gzip.open(outgramps, 'rb') as f:
        gfile= f.read()
        root = ET.ElementTree(ET.fromstring(gfile))
    with open(outgramps, 'wb') as f:
        root.write(f, encoding='utf-8', xml_declaration=True)
#convert dds icons to png and save to main dir 
    while True:
        if os.path.isdir('faith_icon') and os.path.isdir('traits_icon')  is True and os.path.isdir('coa_icon'):
            print('Using previously converted icons.')
            break
        else:
            print('No converted icon files found in current directory.')
            if os.path.isfile('.\pickle\dir.pickle') is True:
                yourinput=gamedir
                print('Using previous entered game directory to generate icons in the exporter directory.')
                break
            print(r'Enter your ck3 game directory to generate those files (eg. C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game):')
            yourinput=input()
        if os.path.isdir(yourinput) is True and os.path.isdir(fr'{yourinput}\\common') is True:
            break
        else:
            continue
#end while loop begin conversion to pnng and move to main folder
    if os.path.isdir('faith_icon') is False and os.path.isdir('traits_icon') is False and os.path.isdir('coa_template') is False:
        os.makedirs('faith_icon',exist_ok=True)
        os.makedirs('traits_icon',exist_ok=True)
        os.makedirs('coa_icon',exist_ok=True)
        os.makedirs('coa_icon/rank',exist_ok=True)
        os.makedirs('coa_icon/colored_emblems',exist_ok=True)
        os.makedirs('coa_icon/patterns',exist_ok=True)
        os.makedirs('coa_icon/exported_coa',exist_ok=True)
        
        path=fr'{yourinput}\gfx\interface\icons\faith'
        path2=fr'{yourinput}\gfx\interface\icons\traits'
        path3=fr'{yourinput}\gfx\interface\coat_of_arms'
        path4=fr'{yourinput}\gfx\coat_of_arms\colored_emblems'
        path5=fr'{yourinput}\gfx\coat_of_arms\patterns'
        pathpng=path+'\*png'
        pathpng2=path2+'\*png'
        pathpng3=path3+'\*png'
        pathpng4=path4+'\*png'
        pathpng5=path5+'\*png'
        p1=(subprocess.run(fr'DDStronk "{path}" && move "{pathpng}" faith_icon',shell=True,capture_output=True,input=b'yes')) 
        p1=(subprocess.run(fr'DDStronk "{path2}" && move "{pathpng2}" traits_icon',shell=True,capture_output=True,input=b'yes'))
        p1=(subprocess.run(fr'DDStronk "{path3}" && move "{pathpng3}" coa_icon/rank',shell=True,capture_output=True,input=b'yes'))
        p1=(subprocess.run(fr'DDStronk "{path4}" && move "{pathpng4}" coa_icon/colored_emblems',shell=True,capture_output=True,input=b'yes'))
        p1=(subprocess.run(fr'DDStronk "{path5}" && move "{pathpng5}" coa_icon/patterns',shell=True,capture_output=True,input=b'yes'))
        print('Converted icons saved to main directory')
    else:
        pass
    start = time.time()

#Producing Coa files
  

    

    outputfilename = '{}_{}'.format(housepng,dt.datetime.now().strftime('%Y%m%d%H%M%S') )
    os.makedirs(f'coa_icon/exported_coa/{outputfilename}',exist_ok=True)
    color.maincoaex(f'coa_icon/exported_coa/{outputfilename}')
    print('Exported title and dynasty icons saved to coa_icon folder')
    
#Parse XML and add obj element
    iconlist=os.listdir('faith_icon')
    traitlist=os.listdir('traits_icon')
    sexlist=os.listdir('avatar')
    coalist=os.listdir(f'coa_icon/exported_coa/{outputfilename}')
    iconrel=['faith_icon/'+i for i in iconlist]
    traitrel=['traits_icon/'+i for i in traitlist]
    sexrel=['avatar/'+i for i in sexlist]
    coarel=[f'coa_icon/exported_coa/{outputfilename}/'+i for i in coalist]
    
    iconlist.extend(traitlist)
    iconlist.extend(coalist)
    iconlist.extend(sexlist)
    
    iconrel.extend(traitrel)
    iconrel.extend(coarel)
    iconrel.extend(sexrel)
    
    
    iconlist=[re.sub('(.*).png',r'\1',i) for i in iconlist]
    
    tree = ET.parse(outgramps)
    root = tree.getroot()
    space=(re.findall('\{.*\}',root.tag))[0]
    space2=root.tag.split('}')[0].strip('{')
    ET.register_namespace('',space2)
    string= ET.tostring(root)
    guy=root[2]
    
    nameform=ET.Element(f'{space}name-formats')
    formnum=ET.SubElement(nameform,f'{space}format',number="-1",name="Title Given Surname",fmt_str="title given surname",active="1")
    root.insert(1,nameform)
    
    mediapath= ET.Element(f'{space}mediapath')
    maindir=os. getcwd()
    mediapath.text=maindir
    root[0].append(mediapath)
    objectspath=ET.Element(f'{space}objects')
    objectspath.tail='\n'
    root.insert(4,objectspath)
    objects=root[4]
#add a obj tag for every icon into xml
    count=0
    for i in range(len(iconrel)):
            count+=1
            objectpath=ET.Element(f'{space}object',handle=housepng+str(count),id='O000'+str(count))
            objectpath.tail='\n'
            filepath=ET.SubElement(objectpath,f'{space}file',src=iconrel[i],mime='image/png',description=iconlist[i])
            filepath.tail='\n'
            objects.append(objectpath)
    femalehandle=objects[len(objects)-2].attrib['handle']
    malehandle=objects[len(objects)-1].attrib['handle']
    
#get the handle of the obj of dynasty icons and add ref to person
    dynnew={}
    for idnum,dyncoa in dyncoapic.items():
        for i in range(len(objects)):
            if objects[i][0].attrib['description']==f'{dyncoa}':
                myhandle=objects[i].attrib['handle']
                dynnew[idnum]=myhandle               
    for idnum,imghandle in dynnew.items():
        for i in range(len(guy)):
            if guy[i].attrib['id']==idnum:
                obj = ET.Element(f'{space}objref',hlink=imghandle)
                obj.tail='\n'
                guy[i].append(obj)
#get the handle of the obj of dynasty icons and add ref to person
    titlenew={}
    for idnum,titlecoa in titlecoapic.items():
        for i in range(len(objects)):
            if objects[i][0].attrib['description']==f'{titlecoa}':
                myhandle=objects[i].attrib['handle']
                titlenew[idnum]=myhandle               
    for idnum,imghandle in titlenew.items():
        for i in range(len(guy)):
            if guy[i].attrib['id']==idnum:
                obj = ET.Element(f'{space}objref',hlink=imghandle)
                obj.tail='\n'
                guy[i].append(obj)
#add male/female avatar
    for i in range(len(guy)):
        if guy[i][0].text=='M':
            male= ET.Element(f'{space}objref',hlink=malehandle)
            male.tail='\n'
            guy[i].append(male)
        if guy[i][0].text=='F':
            female= ET.Element(f'{space}objref',hlink=femalehandle)
            female.tail='\n'
            guy[i].append(female)
#get the handle of the obj of faith icons and add ref to person
    faithnew={}
    for idnum,faithname in faithpic.items():
        for i in range(len(objects)):
            if objects[i][0].attrib['description']==f'{faithname}':
                myhandle=objects[i].attrib['handle']
                faithnew[idnum]=myhandle               
    for idnum,imghandle in faithnew.items():
        for i in range(len(guy)):
            if guy[i].attrib['id']==idnum:
                obj = ET.Element(f'{space}objref',hlink=imghandle)
                obj.tail='\n'
                guy[i].append(obj)
#get the handle of the obj of traits icons and add ref to person    
    detraitnew={}
    for idnum,traits in traitpic.items():
        detraitnew[idnum]=[]
        for trait in traits:
            for i in range(len(objects)):
                if objects[i][0].attrib['description']==f'{trait}':
                    myhandle=objects[i].attrib['handle']
                    detraitnew[idnum].append(myhandle)
                else:
                    pass
    for idnum,imghandles in detraitnew.items():
        for imghandle in imghandles:
            for i in range(len(guy)):
                if guy[i].attrib['id']==idnum:
                    obj = ET.Element(f'{space}objref',hlink=imghandle)
                    obj.tail='\n'
                    guy[i].append(obj)
                else:
                    pass
    with open(outgramps, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f'Import into Gramps as {housepng}? (Existing trees with the same name in Gramps will be replaced!) y/n')
    change=input()
    if change!='y':
        print('Enter your new family tree name:')
        newname=input()
        housepng=newname
        p1=(subprocess.run(fr'"{gramps}" -C "{housepng}" -i "{outgramps}"',shell=True,capture_output=True))
        error=re.sub('\n.*Gtk-WARNING.*\n','',p1.stderr.decode())
        print(error)
    if change=='y':
        print('Using default name')
        p1=(subprocess.run(fr'"{gramps}" -C "{housepng}" -i "{outgramps}"',shell=True,capture_output=True))
        error=re.sub('\n.*Gtk-WARNING.*\n','',p1.stderr.decode())
        print(error)
    end = time.time()
    timer(start,end)


# In[ ]:


# EXPORT TO GRAMPS WITHOUT TITLE AND DYNASTY ICONS
def with_icons_2():
#get traits/faith-idnum relationship
    with open(r'.\pickle\pic.pickle','rb') as f:
        traitpic=pickle.load(f)
        faithpic=pickle.load(f)
        dyncoapic=pickle.load(f)
        titlecoapic=pickle.load(f)
        dynprespic=pickle.load(f)
        titlerankpic=pickle.load(f)
    with open(r'.\pickle\dir.pickle','rb') as f:
        jsondir=pickle.load(f)
        gamedir=pickle.load(f)

 #Prompt to get csv and gramps path       
    while True:
        if os.path.isfile(r'.\pickle\grampsdir.pickle') is True:
            print('Using previously entered gramps directory')
            with open(r'.\pickle\grampsdir.pickle','rb') as f:
                gramps=pickle.load(f)
                gramps=gramps+'\gramps'
        elif os.path.isdir(r'.\pickle\grampsdir.pickle') is False:
            print('Enter your gramps directory (eg. C:\Program Files\GrampsAIO64-5.1.3):')
            gramps=input()
            if os.path.isdir(gramps) is True:
                with open(r'.\pickle\grampsdir.pickle','wb') as f:
                    pickle.dump(gramps,f)
                print('Saved gramps directory as pickle binary for subsequent use')
                gramps=gramps+'\gramps'
            else:
                print('Invalid directory')
                continue
        print('Enter your CSV file:')
        outcsv=input()

        if os.path.isfile(outcsv) is True:
            outgramps=re.sub('(.*).csv',r'\1.gramps',outcsv)
            housepng=re.sub('(.*).csv',r'\1',outcsv)
            break
        else:
            print('Invalid directory')
            continue
#export to workable xml
    p1=(subprocess.run(fr'"{gramps}" -C Anytree -i "{outcsv}" -e "{outgramps}"',shell=True,capture_output=True,input=b'yes')) 
    error=re.sub('\n.*Gtk-WARNING.*\n','',p1.stderr.decode())
    print(error)
    with gzip.open(outgramps, 'rb') as f:
        gfile= f.read()
        root = ET.ElementTree(ET.fromstring(gfile))
    with open(outgramps, 'wb') as f:
        root.write(f, encoding='utf-8', xml_declaration=True)
#convert dds icons to png and save to main dir 
    while True:
        if os.path.isdir('faith_icon') and os.path.isdir('traits_icon')  is True and os.path.isdir('coa_icon'):
            print('Using previously converted icons.')
            break
        else:
            print('No converted icon files found in current directory.')
            if os.path.isfile('.\pickle\dir.pickle') is True:
                yourinput=gamedir
                print('Using previous entered game directory to generate icons in the exporter directory.')
                break
            print(r'Enter your ck3 game directory to generate those files (eg. C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game):')
            yourinput=input()
        if os.path.isdir(yourinput) is True and os.path.isdir(fr'{yourinput}\\common') is True:
            break
        else:
            continue
#end while loop begin conversion to pnng and move to main folder
    if os.path.isdir('faith_icon') is False and os.path.isdir('traits_icon') is False and os.path.isdir('coa_template') is False:
        os.makedirs('faith_icon',exist_ok=True)
        os.makedirs('traits_icon',exist_ok=True)
        os.makedirs('coa_icon',exist_ok=True)
        os.makedirs('coa_icon/rank',exist_ok=True)
        os.makedirs('coa_icon/colored_emblems',exist_ok=True)
        os.makedirs('coa_icon/patterns',exist_ok=True)
        os.makedirs('coa_icon/exported_coa',exist_ok=True)
        
        path=fr'{yourinput}\gfx\interface\icons\faith'
        path2=fr'{yourinput}\gfx\interface\icons\traits'
        path3=fr'{yourinput}\gfx\interface\coat_of_arms'
        path4=fr'{yourinput}\gfx\coat_of_arms\colored_emblems'
        path5=fr'{yourinput}\gfx\coat_of_arms\patterns'
        pathpng=path+'\*png'
        pathpng2=path2+'\*png'
        pathpng3=path3+'\*png'
        pathpng4=path4+'\*png'
        pathpng5=path5+'\*png'
        p1=(subprocess.run(fr'DDStronk "{path}" && move "{pathpng}" faith_icon',shell=True,capture_output=True,input=b'yes')) 
        p1=(subprocess.run(fr'DDStronk "{path2}" && move "{pathpng2}" traits_icon',shell=True,capture_output=True,input=b'yes'))
        p1=(subprocess.run(fr'DDStronk "{path3}" && move "{pathpng3}" coa_icon/rank',shell=True,capture_output=True,input=b'yes'))
        p1=(subprocess.run(fr'DDStronk "{path4}" && move "{pathpng4}" coa_icon/colored_emblems',shell=True,capture_output=True,input=b'yes'))
        p1=(subprocess.run(fr'DDStronk "{path5}" && move "{pathpng5}" coa_icon/patterns',shell=True,capture_output=True,input=b'yes'))
        print('Converted icons saved to main directory')
    else:
        pass
    start = time.time()

    
#Parse XML and add obj element
    iconlist=os.listdir('faith_icon')
    traitlist=os.listdir('traits_icon')
    sexlist=os.listdir('avatar')
    iconrel=['faith_icon/'+i for i in iconlist]
    traitrel=['traits_icon/'+i for i in traitlist]
    sexrel=['avatar/'+i for i in sexlist]
    
    
    iconlist.extend(traitlist)
    iconlist.extend(sexlist)
    
    iconrel.extend(traitrel)
    iconrel.extend(sexrel)
    
    
    iconlist=[re.sub('(.*).png',r'\1',i) for i in iconlist]
    
    tree = ET.parse(outgramps)
    root = tree.getroot()
    space=(re.findall('\{.*\}',root.tag))[0]
    space2=root.tag.split('}')[0].strip('{')
    ET.register_namespace('',space2)
    string= ET.tostring(root)
    guy=root[2]
    
    nameform=ET.Element(f'{space}name-formats')
    formnum=ET.SubElement(nameform,f'{space}format',number="-1",name="Title Given Surname",fmt_str="title given surname",active="1")
    root.insert(1,nameform)
    
    mediapath= ET.Element(f'{space}mediapath')
    maindir=os. getcwd()
    mediapath.text=maindir
    root[0].append(mediapath)
    objectspath=ET.Element(f'{space}objects')
    objectspath.tail='\n'
    root.insert(4,objectspath)
    objects=root[4]
#add a obj tag for every icon into xml
    count=0
    for i in range(len(iconrel)):
            count+=1
            objectpath=ET.Element(f'{space}object',handle=housepng+str(count),id='O000'+str(count))
            objectpath.tail='\n'
            filepath=ET.SubElement(objectpath,f'{space}file',src=iconrel[i],mime='image/png',description=iconlist[i])
            filepath.tail='\n'
            objects.append(objectpath)
    femalehandle=objects[len(objects)-2].attrib['handle']
    malehandle=objects[len(objects)-1].attrib['handle']
    

#add male/female avatar
    for i in range(len(guy)):
        if guy[i][0].text=='M':
            male= ET.Element(f'{space}objref',hlink=malehandle)
            male.tail='\n'
            guy[i].append(male)
        if guy[i][0].text=='F':
            female= ET.Element(f'{space}objref',hlink=femalehandle)
            female.tail='\n'
            guy[i].append(female)
#get the handle of the obj of faith icons and add ref to person
    faithnew={}
    for idnum,faithname in faithpic.items():
        for i in range(len(objects)):
            if objects[i][0].attrib['description']==f'{faithname}':
                myhandle=objects[i].attrib['handle']
                faithnew[idnum]=myhandle               
    for idnum,imghandle in faithnew.items():
        for i in range(len(guy)):
            if guy[i].attrib['id']==idnum:
                obj = ET.Element(f'{space}objref',hlink=imghandle)
                obj.tail='\n'
                guy[i].append(obj)
#get the handle of the obj of traits icons and add ref to person    
    detraitnew={}
    for idnum,traits in traitpic.items():
        detraitnew[idnum]=[]
        for trait in traits:
            for i in range(len(objects)):
                if objects[i][0].attrib['description']==f'{trait}':
                    myhandle=objects[i].attrib['handle']
                    detraitnew[idnum].append(myhandle)
                else:
                    pass
    for idnum,imghandles in detraitnew.items():
        for imghandle in imghandles:
            for i in range(len(guy)):
                if guy[i].attrib['id']==idnum:
                    obj = ET.Element(f'{space}objref',hlink=imghandle)
                    obj.tail='\n'
                    guy[i].append(obj)
                else:
                    pass
    with open(outgramps, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)
    print(f'Import into Gramps as {housepng}? (Existing trees with the same name in Gramps will be replaced!) y/n')
    change=input()
    if change!='y':
        print('Enter your new family tree name:')
        newname=input()
        housepng=newname
        p1=(subprocess.run(fr'"{gramps}" -C "{housepng}" -i "{outgramps}"',shell=True,capture_output=True))
        error=re.sub('\n.*Gtk-WARNING.*\n','',p1.stderr.decode())
        print(error)
    if change=='y':
        print('Using default name')
        p1=(subprocess.run(fr'"{gramps}" -C "{housepng}" -i "{outgramps}"',shell=True,capture_output=True))
        error=re.sub('\n.*Gtk-WARNING.*\n','',p1.stderr.decode())
        print(error)
    end = time.time()
    timer(start,end)


# In[ ]:


while True:
    print("""Main Menu
Select Operations:

[1] Convert .ck3 Save To JSON 
[2] Export Family Tree To CSV
[3] Automatically Import CSV Tree From Step 2 Into Gramps With Icons (Requires step 2 pickle files. Gramps program MUST be closed.)
[4] Import CSV Tree to Gramps Without Dynasty and Title Icons (Faster loading times)
[5] Help
[6] Exit Program""")
    choice=input()
    if choice=='5':
        print("""[1] - Converting your .ck3 save to JSON format is required to export your Family Tree. Both normal and ironman saves are supported.
    Conversion is done by using scorpdx's ck3json Rust program. Go to https://github.com/scorpdx/ck3json for more information about its functionality. 

[2] - Export Family Tree to CSV which can be imported into Gramps. You will get the option to start your tree from any character and with or without cadet families. 
For example,choosing your dynasty founder will generate all characters in your dynasty, while choosing someone else on the tree will only generate 
their descendants and not their extended family.

[3] - Automatically import your save into Gramps with corresponding icons. Besides the CSV file, the generated pickle files from step 2 is required to link characters
to the icon files. The icons in your game directory will be converted to png format and placed in the directory of this program. 
This operation will convert your csv file into gramps-xml, edit the xml to link the icons to each of your characters, and import your save into Gramps.

[4] - Same as [3] except Dynasty and Title icons are excluded. This mode will use the gender icons in the avatar as thumbnails for each character. Performance may be better
and should be selected if [3] lags too much.

    """)
        print('Press enter to go back to the main menu')
        goback=input()
    if choice=='6':
        break
    if choice=='1':
        try:
            tojson()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            logging.error(e, exc_info=True)
    
        print('Press enter to go back to the main menu')
        done=input()
    if choice=='2':
        try:
            data,locnames,dynloc,loccult,allines,mdictraits,fdictraits,traitcode=loading_files()
            dynastyname,idnum,cadet=getinfo()
            faithde,faithre,cult,live,dead,other,dyn,title,houseid,skillist,start,coafind=variables()
            setlist,setlist2,maxlen=getid()
            marrydata,famdata=getfamily()
            allist=getperson()
            end=maketable()
            timer(start,end)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            logging.error(e, exc_info=True)
            
        print('Press enter to go back to the main menu')
        done=input()
    if choice=='3':
        try:
            if 'color' not in sys.modules:
                import color
            else:
                importlib.reload(color)
            with_icons()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            logging.error(e, exc_info=True)
    if choice=='4':
        try:
             with_icons_2()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            logging.error(e, exc_info=True)

            
        print('Press enter to go back to the main menu')
        done=input()
    else:
        continue

