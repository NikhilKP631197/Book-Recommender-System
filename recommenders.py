import pandas as pd
import numpy as np
import random
from mysql.connector import MySQLConnection
from sklearn.metrics.pairwise import cosine_similarity

db = MySQLConnection(host = 'localhost', 
                     username = 'root', 
                     password = 'mysqlNik631197',
                     database = 'books_database')

cursor = db.cursor(buffered = True)

cursor.execute("SELECT * FROM books")

temp_books = cursor.fetchall()

cols_books = ['ISBN',
        'Book-Title',
        'Book-Author',
        'Year-Of-Publication',
        'Publisher',
        'Image-URL-S',
        'Image-URL-M',
        'Image-URL-L']

books = pd.DataFrame(temp_books, columns = cols_books)

class ContentBasedRecommender:

    def __content_recommend(self, book):
        idx = books[books['Book-Title'] == book].index[0]
        dist = self.sim[idx]
        top = sorted(list(enumerate(dist)), reverse = True, key = lambda x:x[1])[1:6]
        return top
    
    def get_recommendations(self, choices):
        top = []
        for names, _ in choices:
            temp = self.__content_recommend(names)
            top+=temp
        top = list(map(lambda x : list(books.loc[x[0]][['Book-Title']]), top))
        top = random.sample(top, 5)
        top = list(map(lambda x:x[0], top))
        return top

    
    def __init__(self, sim_mat):
        self.sim = sim_mat

class ItemBasedRecommender:

    def __init__(self, sim_mat):
        self.item_sim = sim_mat

    def __get_similar_books(self, book_name, user_rating):
        sim = self.item_sim[book_name] * (user_rating - 5)
        sim = sim.sort_values(ascending = False)
        return sim[1:6]

    def get_recommendations(self, choices):
        sim_books = pd.DataFrame()
        for book, rating in choices:
            sim_books = sim_books.append(self.__get_similar_books(book, rating), ignore_index = True)
        sim_books = sim_books.sum().sort_values(ascending = False)
        fav = list(zip(*choices))[0]
        recommend = []
        count = 0
        for i in dict(sim_books).keys():
            if i not in fav:
                recommend.append(i)
                count += 1
            if count == 5:
                break
        return recommend

class UserBasedRecommender:

    def __init__(self, user_df):
        self.user = user_df

    def __normalize(self, row):
        new_row = (row - row.mean())/(row.max() - row.min())
        return new_row

    def __get_sim_users(self, choices, thresh):
        user_df = self.user.set_index("User_ID").copy()
        user_df.loc['new'] = dict(choices)
        user_df.fillna(0, inplace = True)
        temp = user_df[dict(choices).keys()].copy()
        temp = temp.apply(self.__normalize)
        user_sim = cosine_similarity(temp)
        user_sim = pd.DataFrame(user_sim, columns = temp.index, index = temp.index)
        user_sim.drop('new', inplace = True)
        sim = user_sim['new'].copy()
        sim.sort_values(ascending = False, inplace = True)
        idx = sim[sim>=thresh].index
        return list(idx)

    def get_recommendations(self, choices, threshold = 0.5):
        idx = self.__get_sim_users(choices, threshold)
        user_df = self.user.set_index("User_ID").copy()
        user_df = user_df.loc[idx]
        user_df.drop(dict(choices).keys(), axis = 1, inplace = True)
        for i in user_df:
            if user_df[i].sum() == 0:
                user_df.drop(i, axis = 1, inplace = True)
        score = user_df.sum()/len(user_df)
        recommend = dict(score.sort_values(ascending = False)[:5]).keys()
        return list(recommend)