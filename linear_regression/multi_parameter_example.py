from __future__ import division
import math
import random

from helper import metoffice_training_data, chartting

X, Y = metoffice_training_data.TRAIN_DATA
X_test, Y_test = metoffice_training_data.VALIDATE_DATA

Theta = [0 for i in xrange(len(X[0]) + 1)]  # Init all Theta to 0

def hypothesis(x, Theta):
    return Theta[0] + sum((Theta[i + 1] * x[i] for i in xrange(len(x))))

def cost(X, Y, Theta):
    guess = [hypothesis(x, Theta) for x in X]
    return sum([(y - h) ** 2 for h, y in zip(guess, Y)]) / len(X)


def partial_derivative(X,Y,Theta):
    delta = [0 for i in xrange(len(Theta))]
    delta[0] = sum([-(Y[i] - hypothesis(X[i], Theta)) for i in xrange(len(X))])
    for i,x in enumerate(X):
        for j,xj in enumerate(x):
            delta[j+1] -= xj * (Y[i] - hypothesis(x, Theta))

    delta = [2/len(X) * delta[i] for i in xrange(len(delta))]

    return delta


history = []
test_set_history = []
history.append((0 , cost(X, Y, Theta)))
test_set_history.append((0 , cost(X_test, Y_test, Theta)))
alpha = 0.1 # Learning rate
iterations = 10 # Number of training iterations

for i in xrange(iterations):
    delta_theta = partial_derivative(X, Y, Theta)
    Theta = [theta - alpha * delta for theta, delta in zip(Theta, delta_theta)]
    current_cost = cost(X, Y, Theta)
    history.append((i+1,current_cost))
    #test_set_history.append((i+1 , cost(X_test, Y_test, Theta)))
    if i % (iterations//200 + 1) == 0:
        print("Training step %d current cost %.2f" %(i,current_cost))

print "Final cost is %.2f after %s iterations at learning rate %s" % (current_cost, iterations, alpha)
print "%.3f" % Theta[0] + ' + '.join(["%.3f*%s" % (theta, ref) for theta, ref in zip(Theta[1:],metoffice_training_data.X_REF_SHORT)])

print "Test"
Y_test_predict = [hypothesis(x,Theta) for x in X_test]

print "Five guesses:"
guess_v_actual = zip(Y_test_predict, Y_test)
random.shuffle(guess_v_actual)
for guess, answer in guess_v_actual[:5]:
    print("Predicted %.1f actual %s" % (guess, answer))

average_error = sum((math.sqrt((a - g)**2) for g,a in zip(Y_test_predict, Y_test)))/ len(Y_test)
print "Over all the average error is %.3f" % average_error

print "Show learning rate"
chartting.open_chart(
        chartting.make_chart([
            chartting.line2d(*zip(*history),name="Training"),
            #chartting.line2d(*zip(*test_set_history), name="Validation")
        ],
         title="Learning rate",
         xlabel="Iterations",
         ylabel="Cost"))