import psycopg2
import json
globalcon=None
def connection():
    try:
        conn= psycopg2.connect(
            )
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def whatshow(number):
    if number==1:
        return 'Promised Neverland'
    elif number==2:
        return 'Vikings'
    elif number==3:
        return "Seven Deadly Sins"
    elif number==4:
        return "Witcher"
    elif number==5:
        return "Blacklist"

def init():
    global globalcon
    globalcon=connection()

def getActors():
    query = "SELECT * from \"Actors\""

    # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    k=1
    text={}
    for record in cur:
        text[record[0]]={'FirstName':record[1],'LastName':record[2],"Age":record[3]}
        k+=1
    return text
def getActorInfo(ID: int):
    query = "SELECT * from \"Actors\" WHERE \"ID\"={0}".format(ID)

    # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    text = {}
    for record in cur:
        text={'FirstName':record[1],'LastName':record[2],"Age":record[3]}

    return text

def getShows():
    query = "SELECT * from \"Shows\""

    # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    text = {}
    k=1
    for record in cur:
        text[k]={"Aired:":record[1],"Episodes":record[2],"Title":record[3]}
        k+=1
    return text
def getShowsNames():
    query = "SELECT \"ID\",\"Name\" from \"Shows\""

    # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    text = {}
    k=1
    for record in cur:
        text[record[0]]={"Title":record[1]}
        k+=1
    return text

def getShow(Title):
    query = "SELECT * from \"Shows\" WHERE \"Name\"=\'{0}\'".format(Title)

    # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    text = {}

    for record in cur:
        text = {"Aired:": record[1], "Episodes": record[2], "Title": record[3]}

    return text

def getShow2(ID):
    query = "SELECT * from \"Shows\" WHERE \"ID\"=\'{0}\'".format(ID)

    # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    text = {}

    for record in cur:
        text = {"Aired:": record[1], "Episodes": record[2], "Title": record[3]}

    return text

def getshowinfo(number):
    #title=whatshow(int(number))
   # print(title)
    info=getShow2(number)
    print(info)
    actors=getActorsFromShow(number)
    Actors_name={}
    k=1

    for i in actors:
        temp=getActorInfo(i)
        name=temp['FirstName']+temp['LastName']
        Actors_name[k]=name
        k+=1
    print(info)
    info["Actors"]=Actors_name

    return info




def getActorsFromShow(Show: int):

    query = "SELECT * from \"Repartition\" where \"ShowID\"={0}".format(Show)

     # display the PostgreSQL database server version
    cur = globalcon.cursor()
    cur.execute(query)
    text = []
    for record in cur:
        text.append(record[1])
    return text
init()

def getActorsInfoFromShow(show : int):
    actors=getActorsFromShow(show)
    temp={}
    k=1
    for i in actors:
        temp[i]=getActorInfo(i)
        k+=1
    return temp

def insertIntoShows(Info : json):

    query= "Insert into \"Shows\" VALUES({0},{1},{2},\'{3}\')".format(Info["ID"],Info["Aired"],Info["Episodes"],Info["Title"])
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)
def insertIntoActors(Info : json):
    query = "Insert into \"Actors\" VALUES({0},\'{1}\',\'{2}\',{3})".format(Info["ID"], Info["FirstName"], Info["LastName"],Info["Age"])
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)

def updateActorInfo(Info : json):
    actorinfo=getActorInfo(Info['ID'])
    if Info["FirstName"]=='':
        Info['FirstName']=actorinfo['FirstName']
    if Info['LastName']=='':
        Info['LastName']==actorinfo['LastName']
    if Info['Age']=='':
        Info['Age']==actorinfo['Age']

    print(Info)
    query = "Update \"Actors\" SET \"FirstName\"=\'{1}\',\"LastName\"=\'{2}\',\"age\"=\'{3}\' where \"ID\"={0}".format(Info["ID"], Info["FirstName"],
                                                                            Info["LastName"], Info["Age"])
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)

def updateShowInfo(Info : json):
    showinfo=getshowinfo(Info['ID'])
    if Info['Aired']=='':
        Info['Aired']=showinfo['Aired']
    if Info['Episodes']=='':
        Info['Episodes']=showinfo['Episodes']
    if Info['Title']=='':
        Info['Title']=showinfo['Title']
    query = "Update \"Shows\" SET \"Aired\"={0},\"Episodes\"={1},\"Name\"=\'{2}\' where \"ID\"={3}".format(Info['Aired'],Info["Episodes"],Info['Title'],Info['ID'])
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)


def deleteShow(Info : json):
    test=getShow2(Info['ID'])
    print(test)
    if test=={}:
        raise Exception
    query= "Delete from \"Shows\" where \"ID\"={0}".format(Info['ID'])
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)

def deleteActor(Info : json):
    test = getActorInfo(Info['ID'])
    print(test)
    if test == {}:
        raise Exception
    query = "Delete from \"Actors\" where \"ID\"={0}".format(Info['ID'])
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)
def deleteShowCollection():
    print('DELETESHOWCOLLECTION')
    query = "Delete from \"Shows\" where 1=1"
    cur = globalcon.cursor()
    cur.execute(query)
    globalcon.commit()
    print(cur)

def addActorstoShow(Info : json,showID):
    for i in Info:
        query = "Insert into \"Repartition\" VALUES({0},{1})".format(showID,Info[i])
        cur = globalcon.cursor()
        cur.execute(query)
    globalcon.commit()

