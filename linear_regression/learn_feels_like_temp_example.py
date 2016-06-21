from __future__ import division
import math
import os
import random

import datetime

import cPickle

from helper import chartting, data_helpers
from helper.temp import TMP_DIR


def hypothesis(x, Theta):
    return Theta[0] + sum((Theta[i + 1] * x[i] for i in xrange(len(x))))


def cost(X, Y, Theta, regularization_parameter):
    """
    The Regularization term penalizes higher order terms, this helps prevent over fitting.
    If set to 0 this is the same as not regularizing as per the simple example
    """
    guess = [hypothesis(x, Theta) for x in X]
    fit_cost = sum(((y - h) ** 2 for h, y in zip(guess, Y))) / len(X)
    reg_cost = regularization_parameter * sum((t * t for t in Theta[1:])) / len(x)
    return fit_cost + reg_cost


def partial_derivative(X, Y, Theta, regularization_parameter):
    """
    The Regularization term penalizes higher order terms, this helps prevent over fitting.
    If set to 0 this is the same as not regularizing as per the simple example
    """
    delta = [0 for i in xrange(len(Theta))]
    delta[0] = sum([-(Y[i] - hypothesis(X[i], Theta)) for i in xrange(len(X))])
    for i, x in enumerate(X):
        for j, xj in enumerate(x):
            delta[j + 1] += -xj * (Y[i] - hypothesis(x, Theta)) + regularization_parameter * Theta[j + 1]

    delta = [2 / len(X) * delta[i] for i in xrange(len(delta))]

    return delta


if __name__ == '__main__':

    # The Met Office offer a `feels like temperature` forecast
    # See https://blog.metoffice.gov.uk/2012/02/15/what-is-feels-like-temperature/
    # We as an imaginary competitor we want to steel the algorithm for this.
    # We will use multivariate linear regression to calculate an approximation for us.
    # We will make the assumption that we can calculate feels like temperature based
    # on the other parameters the the Met Office proved in it's 5 day forecast.


    # Some set up params.
    alpha = 0.1  # Learning rate
    reg_param = 0  # regularization_parameter
    iterations = 500  # Number of training iterations
    poly_order = 2 # Using 2 or higher means we will us polynomial terms such as x^2 or x*y allowing more complicated functions to be predicted..
    data_set_size = 10000
    DATA_SET = data_helpers.three_hourly_weather_data_set(poly_term_order=poly_order, max_total=data_set_size)
    X_train, Y_train = DATA_SET['train']
    batching = len(X_train) // 10  # If batching is > 0 and <= len(X_train) we effectively use staccato gradient descent.
    batching = len(X_train) if batching < 1 or batching > len(X_train) else batching

    # Learning:
    Theta = [0 for i in xrange(len(X_train[0]) + 1)]  # Init all Theta to 0

    print "Train over %s examples with in batches of %s running %s iterations. Alpha=%s, Reg = %s" % (
        len(X_train), batching, iterations, alpha, reg_param)

    print "Start training @ %s " % datetime.datetime.now()
    cost_history_over_training = []
    cost_history_over_training.append((0, cost(X_train, Y_train, Theta, reg_param)))
    for i in xrange(iterations):
        if batching < len(X_train):
            X_train, Y_train = data_helpers.shuffle(X_train, Y_train)
        delta_theta = partial_derivative(X_train[:batching], Y_train[:batching], Theta, reg_param)
        Theta = [theta - alpha * delta for theta, delta in zip(Theta, delta_theta)]
        current_cost = cost(X_train, Y_train, Theta, reg_param)
        cost_history_over_training.append((i + 1, current_cost))
        if i % (iterations // 200 + 1) == 0:
            print("Training step %d current cost %.2f" % (i, current_cost))

    print "Final cost is %.2f after %s iterations at learning rate %s" % (current_cost, iterations, alpha)

    # Learning can take time so save our learnt data for use later
    pickled_model_file = os.path.join(TMP_DIR, "a%s_r%s_i%s_b%s_p%s_d%s.Theta_min_max.pickle" % (
        alpha, reg_param, iterations, batching, poly_order, data_set_size))
    with open(pickled_model_file, 'w') as fp:
        print "Saving learnt model (Theta, norm_terms, poly_order) to: %s" % pickled_model_file
        cPickle.dump((Theta, DATA_SET['norm_terms'], poly_order), fp)

    # Validate and test the model
    print "Validate/test:"
    X_test, Y_test = DATA_SET['test']
    Y_test_predict = [hypothesis(x, Theta) for x in X_test]

    print "Five guesses:"
    guess_v_actual = zip(Y_test_predict, Y_test)
    random.shuffle(guess_v_actual)
    for guess, answer in guess_v_actual[:5]:
        print("Predicted %.1f actual %s" % (guess, answer))

    average_error = sum((math.sqrt((a - g) ** 2) for g, a in zip(Y_test_predict, Y_test))) / len(Y_test)
    print "Over all the average error is %.3f" % average_error

    print "Show learning rate"
    chartting.open_chart(
            chartting.make_chart([
                chartting.line2d(*zip(*cost_history_over_training), name="Training")],
                    title="Gradient descent cost v iterations",
                    xlabel="Iterations",
                    ylabel="Cost"))

    # This analysis can help find out how to improve our mode. It take a while to run!.
    if False:  # Disable if your not interested in the learning curve at this moment.
        train_cost = []
        real_cost = []
        num_data = []
        chart_filepath = None


        def trainWithNExamples(n, reg_param, itters=100):
            X_subset = X_train[:n]
            Y_subset = Y_train[:n]
            T = [0 for i in xrange(len(X_train[0]) + 1)]
            for i in xrange(itters):
                delta_theta = partial_derivative(X_subset, Y_subset, T, reg_param)
                T = [theta - alpha * delta for theta, delta in zip(T, delta_theta)]
            return cost(X_subset, Y_subset, T, reg_param), T


        for i in xrange(1, 1001):
            c, T = trainWithNExamples(i, reg_param)
            c_validation = cost(X_test, Y_test, T, reg_param)
            train_cost.append(c)
            real_cost.append(c_validation)
            num_data.append(i)
            print "With %s data cost %s real cost %s" % (i, c, c_validation)
            chart_filepath = chartting.make_chart([
                chartting.line2d(num_data, train_cost, name="Training"),
                chartting.line2d(num_data, real_cost, name="Validation")],
                    title="Learning curve",
                    xlabel="Number of training samples",
                    ylabel="Cost",
                    filepath=chart_filepath)
            print "Open %s and refresh to see progress" % chart_filepath

        chartting.open_chart(chart_filepath)
