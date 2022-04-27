#Creating Network as graph
#Reading dataset and entering movies and movies details into the graph and then pickling the
#graph for the application to use

import networkx as nx
import pandas as pd
import time
import pickle

# # Load the data

# In[172]:


df = pd.read_csv('movies.csv')

# In[173]:


df.drop(["budget","homepage","original_language","overview","popularity","release_date","revenue","runtime","spoken_languages","status","tagline","vote_average","vote_count"], axis = 1, inplace = True)


# In[174]:


import json


# In[175]:


'''c = 0
for i in df["keywords"].values:
    c += 1'''
def split_keywords(i):
    k = []
    if i == "[]":
        #print(k)
        #continue
        return k
    
    i = i[1:-1]
    keys = i.split(", {")
    
    for j in range(len(keys)):
        if j == 0:
            s = keys[j]
        else:
            s = "{" + keys[j]
            
        d = json.loads(s)
        k.append(d['name'])
     
    #print(c, type(k))
    return(k)
    


# In[176]:


df["Keys"] = df["keywords"].apply(lambda l: [] if pd.isna(l) else split_keywords(l))


# In[177]:


df["Genre"] = df["genres"].apply(lambda l: [] if pd.isna(l) else split_keywords(l))
df["Production"] = df["production_companies"].apply(lambda l: [] if pd.isna(l) else split_keywords(l))
df["Country"] = df["production_countries"].apply(lambda l: [] if pd.isna(l) else split_keywords(l))


# In[178]:


df.drop(["genres","keywords","production_companies","production_countries","title"], axis = 1, inplace = True)



# In[179]:


df2 = pd.read_csv('movie_credits.csv')


# In[180]:


df2["Casts"] = df2["cast"].apply(lambda l: [] if pd.isna(l) else split_keywords(l))


# In[181]:


def get_dp(i):
    k = []
    if i == "[]":
        #print(k)
        #continue
        return k
    
    i = i[1:-1]
    keys = i.split(", {")
    
    for j in range(len(keys)):
        if j == 0:
            s = keys[j]
        else:
            s = "{" + keys[j]
            
        d = json.loads(s)
        
        if(d['job'] == "Director" or d['job'] == "Producer"):
            k.append(d['name'])
     
    #print(c, type(k))
    return(k)


# In[182]:


df2["Heads"] = df2["crew"].apply(lambda l: [] if pd.isna(l) else split_keywords(l))



# In[183]:


df2.drop(["cast","crew"], axis = 1, inplace = True)



# In[184]:


final = pd.merge(df, df2, left_on = "id", right_on = "movie_id")



# In[185]:


final.drop(["movie_id","title"], axis = 1, inplace = True)


# # Loading the graph

# In[189]:


G = nx.Graph(label = "Movie")
start_time = time.time()

for i, rowi in final.iterrows():
    if (i%1000==0):
        print(" Movie no.: {} => {} seconds".format(i,time.time() - start_time))
        
    G.add_node(rowi['original_title'], key = rowi['id'], label = "Movie")

    for element in rowi['Casts']:
        G.add_node(element, label="Person")
        G.add_edge(rowi['original_title'], element, label = "Acted_in")
        
    for element in rowi['Genre']:
        G.add_node(element, label = "Genre")
        G.add_edge(rowi['original_title'], element, label = "Of_Genre")
        
    for element in rowi['Heads']:
        G.add_node(element, label = "Person")
        G.add_edge(rowi['original_title'], element, label = "Director_Producer")
        
    for element in rowi['Country']:
        G.add_node(element, label = "Country")
        G.add_edge(rowi['original_title'], element, label = "Of_Country")
        
    for element in rowi['Production']:
        G.add_node(element, label = "Production")
        G.add_edge(rowi['original_title'], element, label = "Prod_by")
        
    for element in rowi['Keys']:
        G.add_node(element, label = "Keywords")
        G.add_edge(rowi['original_title'], element, label = "Keys")
    
print(" finish => {} seconds".format(time.time() - start_time))

def dumpData():
	dbfile = open('NetworkPickle.pkl', 'wb')

	# source, destination
	pickle.dump(G, dbfile)                     
	dbfile.close()
	print("Network Pickled")
  
def loadData():
	# for reading also binary mode is important
	dbfile = open('NetworkPickle.pkl', 'rb')     
	G = pickle.load(dbfile)
	print(type(G))
	dbfile.close()

dumpData()
loadData()
