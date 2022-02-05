import requests  
from BeautifulSoup import BeautifulSoup
import pyPdf
from pyPdf import PdfFileReader
import os
from urlparse import urlparse
import mechanize

url="https://yandex.com/search/?text=site%3Amayotte.gouv.fr+ext%3Apdf&lr=10502&p=0"

userAgent = [('User-agent','Mozilla/5.0 (X11; U; ''Linux 2.4.2-2 i586; en-US; m18) Gecko/20010131 Netscape6/6.01')]
link=[]
f="target.html"

def start(linker):
    for i in range(0,2):
        r=linker.replace("p=0","p="+str(i))
        cd=get_code(r)        
        magic_extractor(cd)
        print("\n\n")
    print("[+] All links Has Been Added")
    #print(link)
    start_dw(link)

def get_code(lien):
    return str(requests.get(lien).content)
    
def test_read_file():
    with open(f,"r") as z:
        return z.read()

def downloader(file):
    name=file.split("/")[-1]
    binary_data=testUserAgent(file,userAgent)
    if "%20" in name:
        name=name.replace('%20',"-")
    with open(name,"wb") as data:
        data.write(binary_data)
    print("\n[+] Successfully Download "+name)

def magic_extractor(data):
    bs=BeautifulSoup(data)
    all_a=bs.findAll("a")
    for a in all_a:
        href=a.get("href")
        try:
            if href not in link and "yandex" not in href and "search" not in href:
                link.append(href)
                print(href)
        except TypeError:
            continue

def testUserAgent(url, userAgent):
    browser = mechanize.Browser()
    browser.addheaders = userAgent
    page = browser.open(url)
    source_code = page.read()
    return source_code
            
def start_dw():
    #for lk in list:
        #print(lk)
        #downloader(lk)
    lst=list_file()
    for f in lst:
        extractor_exif("pdf/"+f)
        
def list_file():
    return os.listdir("pdf/")
            
def extractor_exif(fileName):
    pdfFile = PdfFileReader(file(fileName, 'rb'))
    docInfo = pdfFile.getDocumentInfo()
    print '[*] PDF MetaData For: ' + str(fileName)
    for metaItem in docInfo:
        print '[+] ' + str(metaItem) + ':' + str(docInfo[metaItem]) +"\n\n"
   

start_dw()
#extractor_exif("03-Bouclier-qualite%CC%81-prix-juillet-2019-de-SOMACO.pdf")
