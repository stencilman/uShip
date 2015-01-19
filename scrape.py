import requests
from lxml import html
import pdb
import sys


def scrape(line):
    line = line[:-1]   
    itot = 0
    noMore = False
    for pno in range(1, 500):
        print 'REMOVE',line+'/page-'+str(pno)
        page = requests.get(line+'/page-'+str(pno))
        tree = html.fromstring(page.text)
        for i in range(25):  
            print 'REMOVE',itot  
            name = tree.xpath('//*[@id="bcard'+str(itot)+'"]/section[@class="jcar"]/*[@class="jrcl "]/*[@class="compdt"]/p[@class="jcnwrp"]/span/a/text()')
            
            if len(name) == 0:
                noMore = True
                break
            
            ph = tree.xpath('//*[@id="bcard'+str(itot)+'"]/section[@class="jcar"]/*[@class="jrcl "]/*[@class="compdt"]/p[@class="jrcw"]/a/text()')
            ph += tree.xpath('//*[@id="bcard'+str(itot)+'"]/section[@class="jcar"]/*[@class="jrcl "]/*[@class="compdt"]/p[@class="jrcw"]/a/*/text()')
            ph = [p.encode('utf8').replace('\n', '').replace('\r', '').replace('\t','') for p in ph]
            
            name = name[0].encode('utf8').replace('\n', '').replace('\r', '').replace('\t','').replace(',',';')
            jaid = tree.xpath('//*[@id="bcard'+str(itot)+'"]/section[@class="jcar"]/*[@class="jrcl "]/*[@class="compdt"]/p[@class="jaid"]/*')
            if len(jaid) == 0:
                itot += 1
                break
            tags = jaid[1].getchildren()
            ataginfo = tags[0].attrib
            mainurl = ataginfo['onmouseover'].split('\',')[1].split('\'')[1].encode('utf8')
            print 'REMOVE',mainurl
            subpage = requests.get(mainurl)
            subtree = html.fromstring(subpage.text)
            estd  = subtree.xpath('//section[@class="fcont"]')
            finalestd = ''
            if len(estd) > 0:
                for ed in estd:
                    ed = ed.text_content()
                    if 'Year' in ed:
                        finalestd = ed
                        break
                        
            else:
                finalestd = ''
            estd = finalestd
            estd = estd.encode('utf8').replace('\n', '').replace('\r', '').replace('\t','').replace(',',';')
            estd = estd.replace('Year Established','')
            website = ''
            websitecont = subtree.xpath('//*[@class="wsurl"]')
            if len(websitecont) > 0:
                website = subtree.xpath('//*[@class="wsurl"]')[0].getchildren()[-1].text
#             tel = subtree.xpath('//*[@class="tel"]/b/text()')[0].encode('utf8').replace('\n', '').replace('\r', '').replace('\t','').replace(',',';')
            pname = subtree.xpath('//*[@class="item"]/*')[0].text.replace('\r', '').replace('\t','').replace('\n','').replace(',',';')
            fulladd = subtree.xpath('//span[@class="jaddt"]/text()')
            
            if len(fulladd) == 0:
                itot += 1
                break
            
            
            fulladd = fulladd[-1].encode('utf8').replace('\n', '').replace('\r', '').replace('\t','').replace(',',';')
            print pname,',',fulladd,',',
            for p in ph:
                print p,';',
            print ',',estd,',',website,',',mainurl.replace('\r', '').replace('\n','').replace(',',';')
            sys.stdout.flush()
            itot +=1


        if noMore:
            break

with open('justdial.txt') as fn:
    for line in fn:
        scrape(line)

