'''
find p values in PDF and DOCX files and plot histogram

uses python-docx
https://python-docx.readthedocs.io/en/latest/user/install.html
and textract http://textract.readthedocs.io/en/stable/installation.html

'''

#file and folder libraries
import socket
import os 
import glob

import re #regular expressions
import numpy as np #number functions
import pylab as plt #plotting
import pandas as pd #dataframes

#these all probably require installation
import textract #text from .doc and .pdf
from docx import Document # text from .docx


def getText(filename):
    '''text extraction function'''
    doc = Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


print("getting list of files")

#if 'tom' in socket.gethostname():
#    os.chdir('/home/tom/Dropbox/university/expts/pcurve')
#    os.chdir('/home/tom/Dropbox/university/expts/pcurve/p-value-scraper')
#else:
#    print("assuming running in host directory")

filenames=glob.glob('**/*.*',recursive=True)


print("scraping files")

scanned_reports=0
df=pd.DataFrame(columns=['id','folder','p_value'])

for filename in filenames:
    try:
        #filename=filenames[1]
        foldername='-'.join(filename.split('/')[:-1]) #which subfolder is the file in
        fulltext=[]
        
        if (filename[-4:]=='docx') or (filename[-4:]=='DOCX'):
            #assume is Word Docx
    
            fulltext=getText(filename)
            
        elif (filename[-3:]=='doc') or (filename[-3:]=='pdf'):
            #pdf or doc
            fulltext = str(textract.process(filename))
            
        else:
            print(" - - - not a DOC or DOCX or PDF " + filename)
            #do nothing
            
        
        if fulltext:
            #identify locations in text which match repoting of p values
            p_locs=[m.start() for m in re.finditer('p =', fulltext)] + [m.start() for m in re.finditer('p=', fulltext)]
                        
            #for each identified location...
            for s in p_locs:
                            
                snippet=fulltext[s:s+10] #take a snippet of the text
        
                #find the p value reported
                pvalue=float(re.findall('[-+]?\d*\.\d+|\d+', snippet )[0]) # thanks https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
    
                #store p value in df
                df.loc[len(df)]=[scanned_reports,foldername,pvalue]
                           
            scanned_reports+=1
            print("total successfully scanned docs = " + str(scanned_reports))
            
            

            
    except:
        print(" - - - caught error " + filename)
        
print("saving data")

df.to_csv('scraped_pvalues.csv')

print("make histograms")

pvalues=df['p_value'].values

plt.clf()

mask=(pvalues<1) & (pvalues>0)

plt.hist(pvalues[mask],bins=50)
plt.title(str(len(pvalues))+ " p values, from " + str(scanned_reports) + " reports")
plt.savefig('pcurve_all',bbox_inches='tight')

plt.clf()
mask=(pvalues<0.05) & (pvalues>0)
plt.hist(pvalues[mask],bins=15)
plt.title(str(len(pvalues))+ " p values, from " + str(scanned_reports) + " reports")
plt.savefig('pcurve_0p05',bbox_inches='tight')


plt.clf()
mask=(pvalues<0.1) & (pvalues>0)
plt.hist(pvalues[mask],bins=30)
plt.title(str(len(pvalues))+ " p values, from " + str(scanned_reports) + " reports")
plt.savefig('pcurve_0p1',bbox_inches='tight')

plt.clf()
plt.hist(df.groupby('id')['p_value'].count(),bins=25,color='r')
plt.xlabel('p values in report')
plt.ylabel('frequency')
plt.savefig('pcount_dist.png',bbox_inches='tight')

#todo - add something to capture "p <"?