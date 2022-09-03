# -*- coding:Windows-1252 -*-
import urllib
import chardet
import urllib2
import re
import os

def getPage(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('Windows-1252')#.encode('utf-8')
    except urllib2.URLError, e:
        if hasattr(e,"reason"):
            print 'Connection Failed',e.reason
            return None

def modify(s):
    s=s.replace("</i>","")
    s=s.replace(u'�',"A")
    s=s.replace(u'�',"a")
    s=s.replace(u'�',"a")
    s=s.replace(u'�',"a")
    s=s.replace(u'�',"a")
    s=s.replace(u'�',"a")
    s=s.replace(u'�',"a")
    s=s.replace(u'�',"E")
    s=s.replace(u'�',"E")
    s=s.replace(u'�',"e")
    s=s.replace(u'�',"e")
    s=s.replace(u'�',"e")
    s=s.replace(u'�',"I")
    s=s.replace(u'�',"i")
    s=s.replace(u'�',"i")
    s=s.replace(u'�',"O")
    s=s.replace(u'�',"O")
    s=s.replace(u'�',"o")
    s=s.replace(u'�',"o")
    s=s.replace(u'�',"o")
    s=s.replace(u'�',"o")
    s=s.replace(u'�',"o")
    s=s.replace(u'�',"U")
    s=s.replace(u'�',"u")
    s=s.replace(u'�',"u")
    s=s.replace(u'�',"y")
    s=s.replace(u'�',"N")
    s=s.replace(u'�',"n")
    s=s.replace(u'�',"d")
    s=s.replace(u'�',"S")
    s=s.replace(u'�',"s")
    s=s.replace(u'�',"Z")
    s=s.replace(u'�',"z")
    s=s.replace(u'�',"C")
    s=s.replace(u'�',"c")
    s=s.replace(u'�',"ss")
    s=s.replace(u'�',"ae")
    s=s.replace(u'�',"'")
    s=s.replace(u'&nbsp;'," ")
    s=s.replace(u'&amp;',"&")
    s=s.replace(u'&#259;',"a")
    s=s.replace(u'&#261;',"a")
    s=s.replace(u'&#262;',"C")
    s=s.replace(u'&#268;',"C")
    s=s.replace(u'&#269;',"c")
    s=s.replace(u'&#263;',"c")
    s=s.replace(u'&#281;',"e")
    s=s.replace(u'&#283;',"e")
    s=s.replace(u'&#287;',"g")
    s=s.replace(u'&#304;',"I")
    s=s.replace(u'&#305;',"i")
    s=s.replace(u'&#317;',"L")
    s=s.replace(u'&#321;',"L")
    s=s.replace(u'&#322;',"l")
    s=s.replace(u'&#324;',"n")
    s=s.replace(u'&#326;',"n")
    s=s.replace(u'&#328;',"n")
    s=s.replace(u'&#337;',"o")
    s=s.replace(u'&#345;',"r")
    s=s.replace(u'&#350;',"S")
    s=s.replace(u'&#351;',"s")
    s=s.replace(u'&#355;',"t")
    s=s.replace(u'&#367;',"u")
    s=s.replace(u'&#537;',"s")
    s=s.strip()
    return s

baseURL='http://www.footballsquads.co.uk/'
main='squads.htm'
page=getPage(baseURL+main)

Top4League=("LaLiga","Serie A","Bundesliga","Premier League")

count=0

for leagueName in Top4League:
    league=re.search(r'<a href="(.+)">'+leagueName+'</a></td>',page).group(1)
    leagueURL=baseURL+league
    print "--------------",leagueName,"--------------"
    leaguePage=getPage(leagueURL) # Find the link for Top 4 League

    if not os.path.exists(leagueName):
        os.makedirs(leagueName)

    p = re.compile(r'<h5><a href="(.+)">(.+)</a></h5>')

    #leagueFile = open(leagueName+"/clubs.txt", "w")
    for m in p.finditer(leaguePage): # Find the link for each club in the league
        clubName=modify(m.group(2)).replace(" ","")
        #leagueFile.write(clubName+"\n")
        clubFile = open(leagueName+"/"+clubName+".txt", "w")
        mLeague=league[:league.rindex("/")+1]
        clubURL=baseURL+mLeague+m.group(1)
        count+=1
        print "[%s] (%d/78)" % (clubName,count)
        print "Downloading from:",clubURL
        clubPage=getPage(clubURL)

        end=str(clubPage.encode('utf-8')).index("Players no longer at this club")
        clubPage=clubPage[:end]

        s=r'(\d+)</TD>\s*<td.*>(.+)</td>\s*<td.*>.+</td>\s*<td.*>(.+)</td>'
        # re for each player information
        p2= re.compile(s)
        nameDict={}
        playerList=[]
        
        for m2 in p2.finditer(clubPage): # Get the information for each player
            fullName=modify(m2.group(2)).encode('utf-8') # Modify their name to avoid special characters
            number=int(m2.group(1).encode('utf-8'))
            position=m2.group(3).replace("</i>","").encode('utf-8')           
            
            if len(fullName)>0:
                playerList.append([number,fullName,position])

                    
        for player in playerList:
            clubFile.write(str(player[0])+' '+player[1]+' '+player[2]+"\n")
        clubFile.close()
    #leagueFile.close()
