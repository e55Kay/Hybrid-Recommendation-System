# Load Dataframe
import pandas as pd
import pickle
import math
import numpy as np
from heapq import nlargest

movies = pd.read_csv("movies.csv")
movies = movies[["id", "original_title"]]

def get_recommendation(root, G):
    commons_dict = {}
    for e in G.neighbors(root):
        for e2 in G.neighbors(e):
            if e2 == root:
                continue
            if G.nodes[e2]['label'] == "Movie":
                commons = commons_dict.get(e2)
                if commons==None:
                    commons_dict.update({e2 : [e]})
                else:
                    commons.append(e)
                    commons_dict.update({e2 : commons})
    movies = []
    weight = []
    
    #Adamic Adar measure implementation
    
    for key, values in commons_dict.items():
        w=0.0
        for e in values:
            w = w+1/math.log(G.degree(e))
        movies.append(key) 
        weight.append(w)
    
    result = pd.Series(data=np.array(weight),index=movies)
    result.sort_values(inplace=True,ascending=False)        
    return result

def movies_recommendation(movie_list, G):
    
    results = {}

    for j in movie_list:
        result = get_recommendation(j, G)
        
        #print(result)
        i = result.shape[0] - len(movie_list)
        
        for movie in result.iteritems():
            
            if (i == 0):
                break
                
            if (movie[0] in movie_list):
                continue
            
            if movie[0] not in results:
                results[movie[0]] = i
            else:
                results[movie[0]] += i
                
            i -= 1
                
    res = nlargest(len(results), results, key = results.get)
    return res
    

def nw_ranks(movie_list):
    file = open('NetworkPickle.pkl', 'rb')     
    G = pickle.load(file)
    file.close()
    
    res = movies_recommendation(movie_list, G)
    
    net_rank = [x for x in range(1,len(res)+1)]
    net_data = {"title":res, "Network_rank":net_rank}
    net_result = pd.DataFrame(net_data)
    
    global movies
    movies  = movies.merge(net_result, left_on = "original_title", right_on = "title")
    
def get_rating(movie_id, user_id, algo):
    pred = algo.predict(user_id, movie_id)
    return pred.est

def cf_ranks(movie_list, user):
    file = open('RatingsPickle.pkl', 'rb')     
    algo = pickle.load(file)
    file.close()
    global movies
    df = movies
    
    df['user_ratings'] = df['id'].apply(get_rating, user_id = user, algo = algo)
    
    rank = []
    m = 5.1
    cr = 0
    for i in df['user_ratings'].values:
        if i < m:
            cr += 1
            m = i
            
        rank.append(cr)

    df["cf_rank"] = rank
    #df = df[["id","cf_rank"]]
    df.drop(["title", "user_ratings"], axis = 1, inplace = True)
    
    
    #movies  = movies.merge(df, on = 'id')

def rank_merging(x):
    return x['Network_rank'] * 0.5 + x['cf_rank'] * 0.5

def final_ranks():
    global movies
    #print(movies.columns)
    movies["Final_rank"] = movies.apply(rank_merging, axis = 1)
    movies.sort_values(by = ['Final_rank'], ascending = True, inplace = True)

def get_top_recommendations(n, movie_list, user):
    nw_ranks(movie_list)
    cf_ranks(movie_list, user)
    final_ranks()
    
    print(movies.iloc[:n, [0,2,3,4]])
    
    return movies['original_title'].values[:n]

'''def get_nw_recommendations(n):
    return movies.sort_values(by = ['Network_rank'], ascending = True)['original_title'].values[:n]

def get_cf_recommendations(n):
    return movies.sort_values(by = ['cf_rank'], ascending = True)['original_title']o.values[:n]'''