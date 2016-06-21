from __future__ import division
import os
import random
import cPickle
import math
from helper import datapoint
from temp import TMP_DIR


def min_max(X):
    return zip(*((min(x), max(x)) for x in zip(*X)))


def make_all_poly_terms(x, order=1, x2=None):
    x2 = x if x2 is None else x2

    if order <= 1:
        return x2

    new_poly_terms = []
    for xi in x:
        for xj in x2:
            new_poly_terms.append(xi * xj)

    return make_all_poly_terms(x,order=order - 1, x2=new_poly_terms)


def normalise(X, norm_tems=None):
    mins, maxs = norm_tems if norm_tems else min_max(X)
    new_X = []
    for x in X:
        new_data = [(x[j] - mins[j]) / (maxs[j] - mins[j]) for j in xrange(len(x))]
        new_X.append(new_data)
    return new_X, (mins, maxs)


def three_hourly_weather_data_set(poly_term_order=2, max_total=0, no_cache=False):
    pickle_file = os.path.join(TMP_DIR, "3hrly_%s_%s.pickle" % (poly_term_order, max_total))
    if os.path.exists(pickle_file) and not no_cache:
        print "Loading from pickle file %s" % pickle_file
        with open(pickle_file) as fp:
            X, Y, norm_terms = cPickle.load(fp)
    else:
        X, Y = shuffle(*datapoint.feels_like_temp_training_set())
        print "Processing data from, data point..."
        if max_total and max_total >= 6 and max_total < len(X):
            X, Y = X[:max_total], Y[:max_total]
        X, norm_terms = polynomial_and_normalise(X, order=poly_term_order)
        print "Pickling for later use.."
        with open(pickle_file, 'w') as fp:
            cPickle.dump((X, Y, norm_terms), fp)


    # Split data in to training, model selection and testting sets. (Aprox 2/3 to 1/3)]
    sixth_of_data = int(math.floor(len(X) / 6))
    train_select_end_index = 4 * sixth_of_data
    model_select_end_index = train_select_end_index + sixth_of_data

    train_data = (X[:train_select_end_index],Y[:train_select_end_index])
    model_select_data = (X[train_select_end_index:model_select_end_index],
                         Y[train_select_end_index:model_select_end_index])
    test_data = (X[model_select_end_index:],Y[model_select_end_index:])

    return {
        'train':train_data,
        'model_select':model_select_data,
        'test':test_data,
        'norm_terms' : norm_terms,
        'order': poly_term_order
    }


def polynomial_and_normalise(X, order=2):
    X = [make_all_poly_terms(x, order=order) for x in X]
    X, norm_terms = normalise(X)
    return X, norm_terms


def shuffle(X, Y):
    holder = zip(X, Y)
    random.shuffle(holder)
    return zip(*holder)

if __name__ == '__main__':
    # Test min_max
    data = [
        [1, 0,      99.2],
        [2, -3,     22.2],
        [6, -22.3,  0],
    ]
    assert min_max(data)[0] == (1, -22.3, 0)
    assert min_max(data)[1] == (6, 0, 99.2)


    # Test shuffel
    X, Y = range(1000), range(1000)
    X, Y = shuffle(X, Y)
    assert all((X[i] == Y[i] for i in xrange(len(X))))
    assert X != range(1000)

