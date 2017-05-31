import psycopg2 as database
import csv
import re as regularExpression

"""#####Bereinigung#####"""

file = open('american-election-tweets.csv')
DataDictionary = csv.DictReader(file, delimiter=';')

# Read in all the Data from .csv
handle,author,time,favourite,retweet,hashtagsPerTweet,text = [],[],[],[],[],[],[]
hashtagSet = set()
for row in DataDictionary:
    handle.append(row['handle'])
    time.append(row['time'].replace('T', ' '))
    if row['original_author'] == "":
        author.append(row['handle'])
    else:
        author.append(row['original_author'])
    favourite.append(row['favorite_count'])
    retweet.append(row['retweet_count'])
    text.append(row['text'])
file.close()
    
# Extract Hashtags from Text
for singleTweetText in text:
    hashtagsInOneTweet = regularExpression.findall("#[a-zA-Z0-9_]+", singleTweetText)
    for i in range(len(hashtagsInOneTweet)):
        hashtagsInOneTweet[i] = hashtagsInOneTweet[i].lower()
        hashtagSet.add(hashtagsInOneTweet[i])
    hashtagsPerTweet.append(hashtagsInOneTweet)
hashtagsPerTweet[4969] = [hashtagsPerTweet[4969][0]] # Trump uses the same Hashtag in a Tweet twice or thrice 
hashtagsPerTweet[5444] = [hashtagsPerTweet[5444][0]] # and this is the easiest way to account for it manually

"""#####Import#####"""

# Conntect to the Database and get Query Command
server = database.connect("host=localhost dbname=Election user=postgres")
query = server.cursor().execute
#for debugging
query("DELETE FROM Enthaelt")
query("DELETE FROM Tweet")
query("DELETE FROM Hashtag")
# Insert Data into the Database
for hashtag in hashtagSet:
    query("INSERT INTO Hashtag VALUES ('%s')" % (hashtag))

for i in range(len(handle)):
    command = "INSERT INTO Tweet VALUES (%s,'%s',%s,%i,E'%s','%s','%s')" % (
    favourite[i],author[i],retweet[i],i,unicode(text[i].replace( "'" , r"\'"), errors='replace'),time[i],handle[i])
    query(command)
    for hashtag in hashtagsPerTweet[i]:
        query("INSERT INTO Enthaelt VALUES (%i,'%s')" % (i,hashtag))

# Make Changes permanent & exit
server.commit()
server.close()
