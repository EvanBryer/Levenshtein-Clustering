import argparse
parser = argparse.ArgumentParser(description='Perform Levenshtein clustering with a spell check ranking.')
req = parser.add_argument_group('Required arguments')
parser.add_argument("-p", "--path", help="path to file of new line delimited strings.", required=True)
parser.add_argument("-r", "--radius", help="Allowed degree of Levenshtein Distance for clustering. Default is 2.0", type=float, default=2.0)
parser.add_argument("-o", "--out", help="Output file containing clustered data. Default is ./out.txt", default="./out.txt")
req = parser.parse_args()
import io
import hunspell
import re
from datetime import datetime
from leven import levenshtein

startTime = datetime.now()


out = open(req.out,"w+")
#Select languages
hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
hobj.add_dic('/usr/share/hunspell/fr.dic')
hobj.add_dic('/usr/share/hunspell/de.dic')
hobj.add_dic('/usr/share/hunspell/la.dic')
#Select radius for clusters
radius = req.radius
used = []
#Path to files
f1 = open(req.path).readlines()

#Find the distance between the two compressed strings
def dist(str1, str2):
	str1 = str1.lower()
	str2 = str2.lower()
	return levenshtein(str1,str2)

def toFile():
	for i in f1:
		out.write(i)
	print(datetime.now()-startTime)

#Spell check
def checkSpell(clust, ind, inds):
	count = {}
	pos = 0
	for title in clust:
		title = re.sub("-"," ",title)
		c = 0
		for word in title.split():
			word = re.sub(r'\W+', '', word)
			if hobj.spell(word):
				c = c+1
		count[c] = pos
		pos = pos+1
		#print(title, c)
	if(len(count)) > 1:
		#print(count)
		max = -1
		for item in count:
			if int(item) > max:
				max = int(item)
		for i in inds:
			f1[i] = clust[count[max]]
	else:
		for i in inds:
			f1[i] = clust[0]

#Spell check
def check(clust, ind, inds):
	count = {}
	pos = 0
	for title in clust:
		title = re.sub("-"," ",title).lower()
		if title not in count:
			count[title] = 0
		count[title]+=1

	if(len(count)) > 1:
		#print(count)
		max = -1
		maxInd = -1
		for n,v in count.items():
			if int(v) > max:
				max = v
				maxInd = n
		for i in inds:
			f1[i] = clust[count[n]]
	else:
		for i in inds:
			f1[i] = clust[0]

#Go through all strings to find clusters
val = 0
for s1 in f1:
	cluster = [s1]
	inds = [val]
	val = val + 1
	if val in used:
		continue
	for i in range(val, len(f1)):
		s2 = f1[i]
		if(abs(len(s1)-len(s2)) < 5):
			d = dist(s1,s2)
			if d <= radius:
				cluster.append(s2)
				inds.append(f1.index(s2))
	#print(cluster)
	check(cluster, val, inds)
	#if len(cluster) > 1:
	#	print(cluster)
	for v in inds:
		used.append(v)
toFile()

