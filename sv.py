import re
import urllib2
import json
import sys
#from bs4 import BeautifulSoup
#from html.parser import HTMLParser



pldir = 'D:\\Program Files (x86)\\KinoGid\\Browser++\\bin\\Debug\\PlayList\\'
prefix = ''
#pldir = ''
WEB = 0


TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def download(l):
	f = open('temp.html','w')
	res = urllib2.urlopen('http://seasonvar.ru/serial-'+l)
	f.write(res.read())
	f.close()
	#print 'showOpened'


#http://seasonvar.ru/playls2/12be1ccd89bec57e049a1dd237ba63f3/trans/9409/list.xml?rand=0.211448150919073729

def openSeasons(l):#load ass seasons if exists, and load all episodes
	plind = 1  
	#print 'openingSeasons'
	
	res = open('temp.html', 'r').read()
#todo filter trash seasons
#"/serial-7810--Simpsony-0025-sezon.html
	#tabs-result   to  </span>
	i = res.index('tabs-result')
	#res = res.substring
	#res = res[i:100]
	#i = res.index('</span>')
	
	#print remove_tags(res)
	#r'<[^>]+>'
	#res2  = re.compile('tabs-result(.*?)', re.DOTALL |  re.IGNORECASE).findall(res)[0]
	res = res.split('tabs-result')
	if res[1]:
		res = res[1]
	res = res.split('</span>')
	if res[0]:
		res = res[0]
	else:
		print 'fail'
		sys.exit()
	
	#re.findall(r'tabs-result(.*?)',res)
	
	
	for p in re.findall('/serial(.*?).html',res):
		#print 'from:'+p
		t = re.findall('[0-9]+',p)[0]
		if t:
			#print 'to:'+t
			loadPlaylisti(t,str(plind))
			plind = plind + 1
			
	#sys.exit()
	#for i in range(1,50):
#		p = re.findall('/serial(.*?)-'+str(i)+'-',res)
		#if p:
			#print p[0]+" season"+str(i)
			
			#sys.exit()
			#loadPlaylist(l,str(plind))
			#plind = plind+1
		#else:
		#	break
	#print episodes
	
	#loadPlaylist(l,str(0))#was plind
	
	
	

def loadDB():
	f = open('db.sv','w')
	res = urllib2.urlopen('http://seasonvar.ru')
	t = ''
	for p in re.findall(r'/serial-(.*?)</',res.read()):
		t = t + p.replace('"','') + '\n'
	f.write(t)
	f.close()

def log(f,c):
	if not WEB:#todo
		#newpath = r'C:\Program Files\arbitrary' 
		#if not os.path.exists(newpath):
			#os.makedirs(newpath)
		f = open(f,'w')
		f.write(c)
		f.close()
	
def searchFor(p):#find item in DB, load all seasons, load all episodes
	global prefix
	#print 'searchFOr'
	l = ''
	okey = 0
	with open('db.sv') as f:
		for line in f:
			if p.lower() in line.lower():
				r = re.search('(.*?.html)',line)
				
				#findall('(.*?).html',line)[0]
				if r:
					l = r.group(0)			
					#print ")"+l
					prefix = re.search(r'(.*).html',l).group(1)
					rem = re.search(r'[0-9]+-',prefix).group(0)
					if rem:
						prefix = prefix.replace(rem,'')
					rem = re.search('-(.*)',prefix).group(0)
					if rem:
						prefix = prefix.replace(rem,'')
					#print prefix
					#sys.exit()
					
					prefix = prefix +"."
					#print ']'+prefix+' | '+l
					#sys.exit()
					download(l)
					openSeasons(l)
					return

					

def loadPlaylist(l,name):
	global prefix
	global pldir
	ind = re.search('[0-9]+',l).group(0)
	res = urllib2.urlopen('http://seasonvar.ru/playls2/12be1ccd89bec57e049a1dd237ba63f3/trans/' + ind +'/list.xml?rand=0.211448150919073729')
	fetchList(pldir+prefix+name+'.m3u',res.read())

def loadPlaylisti(ind,name):
	global prefix
	global pldir
	global WEB
	#print 'save '+pldir+prefix+name
	if WEB:
		print '<h2>'+prefix+name+'</h2>'
	res = urllib2.urlopen('http://seasonvar.ru/playls2/12be1ccd89bec57e049a1dd237ba63f3/trans/' + ind +'/list.xml?rand=0.211448150919073729')
	fetchList(pldir+prefix+name+'.m3u',res.read())

	
def loadShowPlaylists(l):
	res = urllib2.urlopen(l).read()
	
	return 0

					
def loadSeason():
	return 0

def fetchList(name,data):
	global WEB
	res = '#EXTM3U\n'
	#with data as json_file:  
	#d = json.loads(j)
	data = json.loads(data)
	for p in data['playlist']:
		res += '#EXTINF:\n'+p['file']+"\n\n"
		if WEB:
			print '<a href="'+p['file']+'">'+p['file']+'</a>'
	#print res
	log(name,res.encode('utf-8').strip())
	
	#http://seasonvar.ru/playls2/12be1ccd89bec57e049a1dd237ba63f3/trans/11533/list.xml?rand=0.709797164692378073

#t = ':-1067--Simpsoni-007-sezon'
#print re.findall('',t)
#sys.exit()
	
if sys.argv[1]:
	searchFor(sys.argv[1])
	#print p.split(' >')[1]

#openShow('http://seasonvar.ru/serial-13995-Salem-3-season.html')
#openSeasons()
#loadDB()
#fetchList()
#56