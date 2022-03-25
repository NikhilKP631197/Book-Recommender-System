import pickle
from recommenders import ContentBasedRecommender, ItemBasedRecommender, UserBasedRecommender

sim_mat = pickle.load(open("static/Content_Based_Similarities.pkl", "rb"))

cr = ContentBasedRecommender(sim_mat)

sample = [("Politically Correct Bedtime Stories: Modern Tales for Our Life and Times", 8), 
          ("The Poisonwood Bible: A Novel", 9), 
          ("The Pelican Brief", 4),
          ("Harry Potter and the Prisoner of Azkaban (Book 3)", 10),
          ("The Playboy", 3)]

content_recommended = cr.get_recommendations(sample)

print("BASED ON YOUR READINGS, WE RECOMMEND YOU: \n")

for i in range(len(content_recommended)):
    print((i+1), ".) ", content_recommended[i])

print("\n")

itm_mat = pickle.load(open("static/item_similarity_df.pkl", "rb"))

ir = ItemBasedRecommender(itm_mat)

item_recommended = ir.get_recommendations(sample)

print("BASED ON YOUR INTERESTS, WE RECOMMEND YOU: \n")

for i in range(len(item_recommended)):
    print((i+1), ".) ", item_recommended[i])

print("\n")

user_mat = pickle.load(open("static/User_Ratings.pkl", "rb"))

ur = UserBasedRecommender(user_mat)

user_recommended = ur.get_recommendations(sample)

print("OTHER USERS RECOMMEND: \n")

for i in range(len(user_recommended)):
    print((i+1), ".) ",user_recommended[i])

print("\n")
