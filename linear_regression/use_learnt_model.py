from helper.metoffice_training_data import make_all_poly_terms


def predict(temp, wind_speed, prerecip_prob, relative_humidity, wind_gust, poly_order, scale_terms):
    data_set = [temp, wind_speed, prerecip_prob, relative_humidity, wind_gust]
    make_all_poly_terms(data_set, [])