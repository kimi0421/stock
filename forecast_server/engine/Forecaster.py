import logging

class Forecaster:

    def __init__(self, input_data, po_corr_data, neg_corr_data):
        # Setup logger
        self.logger = logging.getLogger('Forecaster')
        hdlr = logging.FileHandler('data_crawler/logs/forecaster.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

        self.input_data = input_data
        self.po_corr_data = po_corr_data
        self.neg_corr_data = neg_corr_data


    def __calculate_insample_error__(self):

    def __create_feature_mx__(self):

        # Features
        # Average five days' volume


        # Average five days' price

        # Dow's

        # Nasdaq

        #

        return ft_mx

    def train(self, model):
        return train_result

    def forecast(self, trained_model, forward_step):
        return forecast_result


