# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 03:42:10 2022

@author: shubh
"""

import CF_Prediction as model
import pickle
import Recommendations as rc
import time

#model.load_model()

'''file = open('RatingsPickle.pkl', 'rb')     
algo = pickle.load(file)
file.close()

pred = algo.predict(671, 153)
print(pred.est)'''

l = ['Avatar', 'Tangled', 'King Kong', 'Spectre' ]

start_time = time.time()
r = rc.get_top_recommendations(10, l, 671)

end_time = time.time()

print("\nFinal Recommendations =>\n")
for i in r:
    print(i)

print("\ntime taken: ", end_time - start_time, " seconds")

'''n = rc.get_nw_recommendations(10)
c = rc.get_cf_recommendations(10)

print("\nTop Ranked Netword Recommendation List =>\n")

for i in n:
    print(i)


print("\nTop Rated Movies Prediction List =>\n")
for i in c:
    print(i)'''

#algo = model.load_model()

#print(model.ratings[model.ratings["userId"] == 672])
#model.test()

#rating = [672,163,5]

#model.add_ratings(rating)

#model.test()