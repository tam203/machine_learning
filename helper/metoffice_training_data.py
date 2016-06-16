import os
import urllib2
import json

import cPickle

import math

TMP_DIR = os.path.join(os.path.dirname(__file__), '..', 'tmp')
X_PICKLE = os.path.join(TMP_DIR, 'datapoint_x.pickled')
Y_PICKLE = os.path.join(TMP_DIR, 'datapoint_y.pickled')
XREF_PICKLE = os.path.join(TMP_DIR, 'datapoint_xref.pickled')
PICKLE_FILES = [X_PICKLE, Y_PICKLE, XREF_PICKLE]
KEY = os.environ['DATAPOINT_KEY']
GET_ALL_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/all?res=3hourly&key=" + KEY
USE_PICKLED = True # To save pulling down from WOW and processing all the time we can use the pickle files we create if present.
USE_ONE_IN_X_SITES = 5 # Up this number to reduce the amount of data your dealing with.
ORDER = 2




if os.environ.has_key('HTTP_PROXY'):
    proxy = urllib2.ProxyHandler({'http': os.environ['HTTP_PROXY']})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)

X = []
X_REF_SHORT = ['U', 'T', 'S', 'P', 'H', 'G']
X_REF_DESC = """U = Uv Index,
    T = Temperature,
    W = Wind Speed,
    P = Precipitation Probability (AKA Pp),
    H = Relative Humidity,
    G = Wind Gust"""

Y = [] # F: This gives the Feels Like Temperature


# In order to predict a function like y = x*x we create new features which are
# polynomial versions of the original features
# This function does that up to a polynomial order.
# It also returns a "ref" array which tells you what the new polynomials are.
def make_all_poly_terms(x, x_ref, order=1, x2=None, x2_ref=None):
    x2, x2_ref = (x, x_ref) if x2 is None else (x2, x2_ref)

    if order <= 1:
        return x2, x2_ref

    new_poly_terms, new_poly_terms_ref = [], []
    for xi, refi in zip(x, x_ref):
        for xj, refj in zip(x2, x2_ref):
            new_poly_terms.append(xi * xj)
            new_poly_terms_ref.append("%s*%s" % (refi, refj))

    return make_all_poly_terms(x, x_ref, order=order - 1, x2=new_poly_terms, x2_ref=new_poly_terms_ref)


if USE_PICKLED and all((os.path.exists(f) for f in PICKLE_FILES)):
    print("Using pickled data, skipping Datapoint and processing...")
    with open(X_PICKLE, 'r') as fp:
        X = cPickle.load(fp)

    with open(Y_PICKLE, 'r') as fp:
        Y = cPickle.load(fp)

    with open(XREF_PICKLE, 'r') as fp:
        X_REF_SHORT = cPickle.load(fp)
else:
    # Get all 3 hour forcasts for all sites
    req = urllib2.Request(url=GET_ALL_URL)
    res = urllib2.urlopen(req)
    data = json.load(res)

    # Grab all the numeric weather parameters to make our feature vector x and put in to the collection X
    # Grab the feels like temp and stick it in our collection Y, this is what we are aiming to guess.
    for i, loc in enumerate(data['SiteRep']['DV']['Location']):
        if (i % USE_ONE_IN_X_SITES) != 0: # Limit our self's to 1 in x sites
            continue
        for period in loc['Period']:
            for rep in period['Rep']:
                X.append([
                    float(rep['U']),
                    float(rep['T']),
                    float(rep['S']),
                    float(rep['Pp']),
                    float(rep['H']),
                    float(rep['G'])
                ])
                Y.append(float(rep['F']))


    # Make some poly nomial ters i.e T*T or T*H up to the order ORDER.
    for i,x in enumerate(X):
        x, ref = make_all_poly_terms(x, x_ref=X_REF_SHORT, order=ORDER)
        if i == 0:
            mins = [x[k] for k in range(len(x))]
            maxs = [x[k] for k in range(len(x))]
        # While we are looping over the data anyway, get the max's and min's of each feature (such as T or T*H)
        for j in xrange(len(x)):
            maxs[j] = x[j] if x[j] > maxs[j] else maxs[j]
            mins[j] = x[j] if x[j] < mins[j] else mins[j]
        X[i] = x
    X_REF_SHORT = ref # Up date the reference with our new polynomial features.

    # Feature scale. This makes all features between 0 and 1 with a mean of 0.5. Doing this
    # Prevents one feature from dominating the cost and so being unduly represented.
    for i,x in enumerate(X):
        X[i] = [(x[j] - mins[j])/(maxs[j] - mins[j]) for j in xrange(len(x))]

    # Again update the refs with our scaling terms
    X_REF_SHORT = ["((%s) - %s)/(%s - %s)" % (X_REF_SHORT[j], mins[j], maxs[j], mins[j]) for j in xrange(len(X_REF_SHORT))]


# pickle the data for faster access in the future.
with open(X_PICKLE, 'w') as fp:
    cPickle.dump(X, fp)

with open(Y_PICKLE, 'w') as fp:
    cPickle.dump(Y, fp)

with open(XREF_PICKLE, 'w') as fp:
    cPickle.dump(X_REF_SHORT, fp)

# Split data in to training and validation sets. (Aprox 2/3 to 1/3)
num_train_examples = int(math.floor(2 * len(X) / 3))
TRAIN_DATA = (X[:num_train_examples], Y[:num_train_examples])
VALIDATE_DATA = (X[num_train_examples:], Y[num_train_examples:])

print("There are %s training examples with %s features of order %s (%s validation examples)" % (
    len(TRAIN_DATA[0]),
    len(X[0]),
    ORDER,
    len(VALIDATE_DATA[0])))
