import pandas as pd
from surprise import Dataset, Reader, KNNWithMeans
import pickle

ratings = pd.read_csv('ratings_small.csv')
ratings.drop(["timestamp"], axis = 1, inplace = True)

def add_ratings(rating):
	ratings.loc[len(ratings.index)] = rating

def load_model():
    reader = Reader()
    print("Loading Model....")
    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

    sim_options = {
	    "name": "cosine",
	    "user_based": False,
	}
    algo = KNNWithMeans(sim_options=sim_options)

    trainingSet = data.build_full_trainset()

    algo.fit(trainingSet)
    
    #pickling
    file = open('RatingsPickle.pkl', 'wb')

	# source, destination
    pickle.dump(algo, file)                     
    file.close()
    print("CF Algorithm Pickled")

    #return algo

'''def predict_rating(model,userId, movieId):
	pred = model.predict(userId, movieId)
	return pred.est'''

'''def test():
    print(ratings[ratings["userId"] == 672])'''

