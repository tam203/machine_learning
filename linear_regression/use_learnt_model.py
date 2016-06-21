import cPickle

from helper import datapoint, data_helpers
from helper.datapoint import PARAM_INDEXES


def predict(x, Theta):
    return Theta[0] + sum((Theta[i + 1] * x[i] for i in xrange(len(x))))

def prepare_data_for_model(x, order, norm_terms):
    x = data_helpers.make_all_poly_terms(x, order)
    return data_helpers.normalise([x], norm_terms)[0][0]

def data_Set_to_str(x):
    msg = []
    for key, index in PARAM_INDEXES.items():
        msg.append("%s @ %4.1f" % (key, x[index]))
    return ', '.join(msg)

if __name__ == "__main__":
    model_file = r"C:\theo-work-area\machine_learning\helper\..\tmp\a0.1_r0_i10_b200_p2_d3000.Theta_min_max.pickle"
    with open(model_file) as fp:
        Theta, norm_terms, poly_order = cPickle.load(fp)

    X, Y = datapoint.feels_like_temp_training_set()

    for x,y in zip(X, Y)[:30]:
        print "for %s I predict %4.1f correct answer %4.1f" % (
                data_Set_to_str(x),
                predict(prepare_data_for_model(x, poly_order, norm_terms), Theta),
                y)


