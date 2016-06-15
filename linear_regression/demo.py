from __future__ import division

import os
import random

import math

from helper import chartting


# Create some data. This is a black box to the machine learning algorithm below.
# This function will model out input data. It's a y =mx+c but with a bit of random
y_lambda = lambda x:  3 + 0.3 * x + random.randint(math.floor(-0.2*x),math.floor(0.2*x))
# Create some data
X = range(10,110)
Y = [y_lambda(x) for x in X]

# Ok let's pretend that out data is "enemy level" on the x and "enemy hit" points on the y.
# Let's take a look:
chartting.open_chart(
        chartting.make_chart(
                [chartting.scatter2d(X,Y)], xlabel="Enemy level", ylabel="Enemy hitpoints", title="Hit points V Level"))
# TODO: Uncomment below
#raw_input("Waiting for you to finish looking at your chart. Hit enter when you are good to go!")


# So our task becomes given we know an enemy's level can we guess their hit points?

# So we are going to make the hypothesis that our data is in the form:
# y = mx +c     // AKA: enemy_hit_points = CONSTANT_1 * enemy_level + CONSTANT_2
# I'm going to rewrite that as:
# y = Theta[0] + Theta[1] * x
# I.e. Theta[0] = c and Theta[1] = m so Theta = [c,m]


# So given an array of x's (enemy levels) we can predict the corresponding y's (hit points)
def hypothesis(X, Theta):
    return [(Theta[0] + Theta[1] * x) for x in X]

# The issue is that we don't know what the two constants are (Theta[0] and Theta[1]).
# We could guess, let's try that.
Theta = [
    random.randrange(0,5) + random.random(),  # A random guess between 0 and 6
    random.random() * 6, # A random guess between 0 and 6
]

# Now let's plot our predictions against our guesses using the above values for the constants.
chartting.open_chart(
        chartting.make_chart([
            chartting.scatter2d(X,Y, name="Actuals"),
            chartting.line2d(X, hypothesis(X, Theta), name="Our guess. Theta=%s"%(Theta,))],
            title="Guessing at the constants",
            xlabel="Enemy level",
            ylabel="Enemy hitpoints"))
# TODO: Uncomment below
#raw_input("Enjoy that one for a bit and hit enter when you've recovered you blown mind.")


# Ok that doesn't look quite right...
# Next step figure out how not right it is. Let's create a `cost` function that will:
# Given your guess for Theta[0] and Theta[1] work out the predicted value for all y's give x's,
# compare to the actual values and tell you how wrong you are (the cost for a given Theta selection).
# Cost will be the average of all:
# (actual_value - predicted_value)^2
def cost(X, Y, Theta):
    return sum([(y - h) ** 2 for h, y in zip(hypothesis(X, Theta), Y)]) / len(X)


# Ok let's have some guesses and evaluate the cost.
guess1 = [20,0]
guess2 = [0,0.1]
guess3 = [3,0.5]




#for i,guess in enumerate([guess1, guess2, guess3]):
#    print("For guess %s Theta=%s The cost is %.2e" %(i+1, guess, cost(X, Y, guess)))

chartting.open_chart(
        chartting.make_chart([
            chartting.scatter2d(X,Y, name="actuals"),
            chartting.line2d(X, hypothesis(X, guess1), name="Guess Theta=%s, Cost %.2e" %(guess1, cost(X, Y, guess1))),
            chartting.line2d(X, hypothesis(X, guess2), name="Guess Theta=%s, Cost %.2e"%(guess2, cost(X, Y, guess2))),
            chartting.line2d(X, hypothesis(X, guess3), name="Guess Theta=%s, Cost %.2e" %(guess3, cost(X, Y, guess3)))],
            title="Some guesses and their cost", xlabel="Enemy level", ylabel="Enemy hitpoints"))

# TODO: Uncomment below
#raw_input("You know the drill. Enter to go on.")


# Ok so better guesses have a lower `cost` so to find the best guess we try find the parameters of Theta that
# minimise the cost

# If we understand our cost function we can figure out how to minimise it
# So lets take a look by plotting as a 3d surface. x = Theta[0], y = Theta[1] and z = cost(X,Y,Theta)
# Where X and Y our our fixed set of data (effectively constants)
chartting.open_chart(
    chartting.make_chart([
        chartting.surface_data(
            [0.1 * i for i in range(0, 40)], # plot Theta[0] between 0 and 4 in 0.1 increments
            [0.01 * i for i in range(0, 100)], # plot Theta[1] between 0 and 1 in 0.01 increments
            lambda theta0, theta1: cost(X, Y, [theta0, theta1]) # z is our cost given Theta[0] and Theta[1]
        )], title="The cost function", xlabel="Theta[0]", ylabel="Theta[1]", zlabel="cost"))



# TODO: Uncomment below
#raw_input("You know the drill. Enter to go on.")


# So to find the minimum we need to find that dip at the very bottom of the curved surface.
# There are different ways of doing this but we are going to use gradient decent. This works
# on the fact that at the minimum the gradient is zero. To implement we chose a random start
# (random Theta[0] and Theta[1] find the gradient of the cost function at that point and then
# move `down` the surface in the direction of the gradient a distance proportional to the
# steepness of the gradient. We then calculate the gradient of the cost function at this new spot
# and repeat till the gradient is near zero (or we get bord).

# Let's see this in action.

# This function will calculate the approx gradient for a function f(x) at x with respect to x.
# Aka How slopey is the function at this point.
def gardient_aprox(func, x, delta=0.00001):
    return (func(x + (delta/2)) - func(x - (delta/2)))/delta

# Learning rate, this is how quickly we want to "descend the slope" to quick and we over shoot and never find the minimum,
# to little it takes for ages...
LEARNING_RATE = 1e-04

# Our starting guess at Theta, we have to start somewhere
Theta = [2, 1]

# As we go we are going to keep a track of all our guesses and their cost
history = []
history.append([Theta[0],Theta[1],cost(X,Y,Theta)])


print "with y = %.2f + %.2fx cost = %.2e (Alpha=%.2e)" % (Theta[0], Theta[1], cost(X, Y, Theta), LEARNING_RATE)

# Let's run gradent decent 20 times
for i in range(2000):
    gradient_with_respect_to_theta = [
        gardient_aprox((lambda theta0: cost(X, Y, [theta0, Theta[1]])), Theta[0]), # The gradient with respect to Theta[0]
        gardient_aprox((lambda theta1: cost(X, Y, [Theta[0], theta1])), Theta[1]) # The gradient with respect to Theta[1]
    ]


    # Change our guess at Theta by an amount proportional to the gr
    Theta[0] = Theta[0] - LEARNING_RATE * gradient_with_respect_to_theta[0]
    Theta[1] = Theta[1] - LEARNING_RATE * gradient_with_respect_to_theta[1]

    # Append our current guess
    history.append([Theta[0],Theta[1],cost(X,Y,Theta)])

    # Print the results so we can watch
    if (i % 10) is 0:
        print "Iteration %i: y = %.2f + %.2fx cost = %.2e (learning rate = %.2e)" % (i, Theta[0], Theta[1], cost(X, Y, Theta), LEARNING_RATE)

    # Now repeat that all again

print "Our final guess is after %i iiterations\n\ty = %.2f + %.2fx" % (i+1, Theta[0], Theta[1])

chartting.open_chart(
        chartting.make_chart([
            chartting.scatter2d(X,Y, name="Actuals"),
            chartting.line2d(X, hypothesis(X, Theta), name="Our best guess")],
                title="Our best fit", xlabel="Enemy level", ylabel="Enemy hitpoints"))



# Let's visualise how we got to that guess:


chartting.open_chart(
    chartting.make_chart(
            [
                chartting.surface_data(
                    [0.1 * i for i in range(0, 40)], # plot Theta[0] between 0 and 4 in 0.1 increments
                    [0.01 * i for i in range(0, 100)], # plot Theta[1] between 0 and 1 in 0.01 increments
                    lambda theta0, theta1: cost(X, Y, [theta0, theta1]),
                    opacity=0.9),
                chartting.line3d(*zip(*history), name="`Path` taken by gradient descent")
            ],
            title="Gradient decent visualised",xlabel="Theta[0]", ylabel="Theta[1]", zlabel="cost"
    )
)