"""
Autorzy: Patrycja Bednarska i Maciej Dzieciuch

Wymagania:
    python 3.8
    pip install numpy

Start programu:
    python recommend_movie_engine.py
"""
import json

import numpy as np


# Compute the Euclidean distance score between user1 and user2
def euclidean_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    # If there are no common movies between the users,
    # then the score is 0
    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


# Compute the Pearson correlation score between user1 and user2
def pearson_score(dataset, user1, user2):
    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    # Movies rated by both user1 and user2
    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)

    # If there are no common movies between user1 and user2, then the score is 0
    if num_ratings == 0:
        return 0

    # Calculate the sum of ratings of all the common movies
    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    # Calculate the sum of squares of ratings of all the common movies
    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    # Calculate the sum of products of the ratings of the common movies
    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    # Calculate the Pearson correlation score
    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


def choose_person():
    counter = 0
    user_list = []
    print('\nChoose person for which you want to recommend movie: ')
    for item in data:
        print('\t' + str(counter) + '. ' + item)
        user_list.append(item)
        counter += 1

    return user_list[int(input())]


def choose_algorithm():
    algorithm_type = ['Pearson', 'Euclidean']
    algorithm_list = []
    print('Choose algorithm: ')

    counter = 0

    for item in algorithm_type:
        print('\t' + str(counter) + '. ' + item)
        algorithm_list.append(item)
        counter += 1

    return algorithm_list[int(input())]


def movie_result(user_dict):
    movie_object = {}

    for key, value in user_dict.items():
        if key not in data[user].keys():
            movie_object[key] = value

    movie_dict = dict(sorted(movie_object.items(), key=lambda element: element[1], reverse=True))

    best_movies = dict(list(movie_dict.items())[:7])
    bad_movies = dict(list(movie_dict.items())[-7:])

    counter = 1
    movie_list = []

    print('\nThe best movies for you:')
    for movie in best_movies:
        print('\t' + str(counter) + '. ' + movie + ' ' + str(best_movies[movie]))
        counter += 1
        movie_list.append(movie)

    counter = 1

    print('\nWe don\'t recommend:')
    for movie in bad_movies:
        print('\t' + str(counter) + '. ' + movie + ' ' + str(bad_movies[movie]))
        counter += 1
        movie_list.append(movie)

    return movie_list


if __name__ == '__main__':

    ratings_file = 'ratings.json'

    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    user = choose_person()
    algorithm_type = choose_algorithm()
    score_array = []

    for element in data:
        if element != user:
            if algorithm_type == 'Pearson':
                score_array.append({'score': pearson_score(data, user, element), 'user': element})
            else:
                score_array.append({'score': euclidean_score(data, user, element), 'user': element})

    max_score = max(score_array, key=lambda x: x['score'])

    user_movies = data[max_score['user']]

    movie_result(user_movies)
