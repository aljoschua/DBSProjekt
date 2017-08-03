from distance import d
import psycopg2 as database
from random import randint as random
import json
from math import sqrt

# Load & trim Data
server = database.connect("host=localhost dbname=Election user=postgres")
queryTool = server.cursor()
queryTool.execute("Select * from Hashtag")
results = queryTool.fetchall()
hashtags = []
for instance in results:
    hashtags.append(instance[0])
queryTool.execute("Select * from Enthaelt")
results = queryTool.fetchall()
enthaelt = {}
for instance in results:
    if instance[0] in enthaelt:
        enthaelt[instance[0]].append(instance[1])
    else:
        enthaelt[instance[0]] = [instance[1]]
queryTool.execute("Select * from Tweet")
results = queryTool.fetchall()
tweets = []
for instance in results:
    tweet = {'id' : instance[3], 'date': str(instance[5])[5:10] }
    tweets.append(tweet)
server.close()

# k-means algorithm
def calculateClustercenter(cluster): # given a list of hashtags, finds the hashtag,
#to which all the others have minimal distance
    matrix = {}
    for a in cluster:
        matrix[a] = []
        for b in cluster:
            matrix[a].append(d(a, b))
    return reduce(lambda a,b: a if sum(a[1]) < sum(b[1]) else b, matrix.items())[0]
"""
 reduce means foldl in python;
 x if y else z
 is equivalent to:
 if y:
    x
 else:
    z
"""
sigma = 1.2 # Assign Values for the constants
k = 7
clustercenters = {} #keys are cluster centers, values are arrays of whole clusters
for i in range(k): # Generate Random Clustercenters
    potentialCenter = random(0, len(hashtags)-1)
    if potentialCenter not in clustercenters:
        clustercenters[hashtags[potentialCenter]] = [] #
while True:
    for hashtag in hashtags: # Assign Datapoints to their nearest Clustercenters
        foldl_func = lambda x, y: x if d(hashtag, x) < d(hashtag, y) else y
        nearestCenter = reduce(foldl_func, clustercenters.keys())
        clustercenters[nearestCenter].append(hashtag)
    stop = True
    for key, value in clustercenters.items():
        min = calculateClustercenter(value) # update Clustercenters
        if min != key:
            clustercenters[min] = value
            del clustercenters[key]
        if d(key, min) > sigma: # nicer
            stop = False
    if stop:
        break
    # delete clusters
    for i in clustercenters.keys():
        clustercenters[i] = []
assert(len(clustercenters.keys()) == k)
for z, v in clustercenters.items():
    assert(z in v)
    assert(len(v) == len(set(v)))
    for h, i in clustercenters.items():
        if h != z:
            assert(h not in v)
            assert(z not in i)
# Calculate Coordinates for Clustercenters
def euclidD( a, b):
    c = (a[0]-b[0])**2
    d = (a[1]-b[1])**2
    return sqrt(c+d)
# Dimensions of the whole Graph
x = 1800
y = 1000

i = 1
while k > i**2:
    i += 1
centerpoints = []
for a in range(k):
    for u in range(1,i*2, 2):
        for t in range(1, i*2, 2):
            centerpoints.append( ((u*x)/(i*2), (t*y)/(i*2)))
centerpoints  = list(set(centerpoints))
counter = 0
hashtagstocenterpoints = {}
for center in clustercenters.keys():
    hashtagstocenterpoints[center] = centerpoints[counter]
    counter += 1

# Make JSON for sigma JS
a = 0
sigma = {"nodes" : [], "edges" : []}
for k,v in enthaelt.items():
    for i in v:
        node = {'id' : i, 'label' : i, 'size' : 1}
        if node['id'] not in map(lambda x: x['id'], sigma['nodes']):
            if i in clustercenters.keys():
                        point = hashtagstocenterpoints[i]
                        node['x'] = point[0]
                        node['y'] = point[1]
                        node['color'] = "#000"
                        node['size'] = 10
            else:
                for e, f in clustercenters.items():
                    if i in f:
                        point = hashtagstocenterpoints[e]
                        candidate = (0,0)
                        while euclidD(candidate,point) > 120:
                            candidate = (random(0,x), random(0,y))
                        node['x'] = candidate[0]
                        node['y'] = candidate[1]
                        break
            sigma['nodes'].append(node)
        for j in v:
            if i != j:
                edge = {'source' : i, 'id' : a, 'target' : j, 'color' : "#0ff"}
                a += 1
                extractor = lambda x: [x['source'],x['target']]
                if [edge['source'], edge['target']] not in map( extractor, sigma['edges']):
                    filter(lambda x: x['id'] == edge['source'], sigma['nodes'])[0]['size'] += 1
                    sigma['edges'].append(edge)
#""" uncomment lines 138 and 144 if you dont want edges for clusters( the red ones )
for k, v in clustercenters.items():
    for i in v:
        edge = {'source': k, 'id': a, 'target': i, 'color': "#ec5148" }
        a += 1
        sigma['edges'].append(edge)
#"""
file = open("js/sigma-data.json", "w")
file.write(json.dumps(sigma))
file.close()

#Make JSON for flot JS
hashtagsPerDay = {}
for tweet in tweets:
    if tweet['id'] not in enthaelt:
        continue
    hashtagsInOneTweet = enthaelt[tweet['id']]
    if tweet['date'] in hashtagsPerDay:
        hashtagsPerDay[tweet['date']] += hashtagsInOneTweet
    else:
        hashtagsPerDay[tweet['date']] = hashtagsInOneTweet
file = open("js/blockchart-data.json", "w")
file.write(json.dumps(hashtagsPerDay))
file.close()
