import logging
import pandas as pd
import numpy as np

class Forecaster:

    def __init__(self, input_data, po_corr_data, neg_corr_data, model):
        # Setup logger
        self.logger = logging.getLogger('Forecaster')
        hdlr = logging.FileHandler('logs/forecaster.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)

        self.model = model
        self.input_data = input_data
        self.po_corr_data = po_corr_data
        self.neg_corr_data = neg_corr_data


    def __calculate_insample_error__(self, predicted, actual):
        predicted_change = (predicted[1:] - predicted[:-1]) / predicted[:-1]
        actual_change = (actual[1:] - actual[:-1]) / actual[:-1]
        error_mean = np.mean(predicted_change - actual_change)
        error_std = np.std(predicted_change - actual_change)
        return error_mean, error_std

    def __clean_ft_mx__(self, ft_mx):

        ft_mx = ft_mx.dropna()
        return ft_mx

    def __price_avg_n__(self, moving_days, total_number, symbol, date_index):
        output_dir = 'output/index/'
        df = pd.read_csv(output_dir + symbol + '.csv', index_col=[0])
        df = df.ix[date_index]
        price_list = np.array(df['Adj Close'])
        price_avg = [np.mean(price_list[i : i + moving_days]) for i in range(total_number)]
        return price_avg

    def __create_feature_mx__(self, input_data, po_corr_data, neg_corr_data, forward_step=0):

        # Features
        # Get total length of input data
        n = len(input_data)

        # Construct initial structure
        ft_mx = pd.DataFrame({'price': input_data['Adj Close'].tolist()}, index=range(n))
        ft_mx = ft_mx.append(pd.DataFrame({'price': [np.nan] * 30}, index=range(n + 1, n + 31)))

        # Average five days' volume
        volume_list = np.array(input_data['Volume'])
        if forward_step <= 5:
            volumes_avg_5 = [np.mean(volume_list[i:i + 5]) for i in xrange(n)]
            ft_mx.loc[5:5 + n, 'volume_avg_5'] = volumes_avg_5
        # Average 30 days' volume
        volumes_avg_30 = [np.mean(volume_list[i:i + 30]) for i in xrange(n)]
        ft_mx.loc[30:30 + n, 'volume_avg_30'] = volumes_avg_30

        # Average five days' price
        price_list = np.array(input_data['Adj Close'])
        if forward_step <= 5:
            price_avg_5 = [np.mean(price_list[i:i + 5]) for i in xrange(n)]
            ft_mx.loc[5:5 + n, 'price_avg_5'] = price_avg_5
        price_avg_30 = [np.mean(price_list[i:i + 30]) for i in xrange(n)]
        ft_mx.loc[30:30 + n, 'price_avg_30'] = price_avg_30

        # Index Features
        if forward_step <= 5:
            dji_price_avg_5 = self.__price_avg_n__(5, n, 'DJI', input_data.index)
            ft_mx.loc[5:5 + n, 'dji_price_avg_5'] = dji_price_avg_5
        dji_price_avg_30 = self.__price_avg_n__(30, n, 'DJI', input_data.index)
        ft_mx.loc[30:30 + n, 'dji_price_avg_5'] = dji_price_avg_30

        if forward_step <= 5:
            ixic_price_avg_5 = self.__price_avg_n__(5, n, 'IXIC', input_data.index)
            ft_mx.loc[5:5 + n, 'ixic_price_avg_5'] = ixic_price_avg_5
        ixic_price_avg_30 = self.__price_avg_n__(30, n, 'IXIC', input_data.index)
        ft_mx.loc[30:30 + n, 'ixic_price_avg_5'] = ixic_price_avg_30

        if forward_step <= 5:
            sp_price_avg_5 = self.__price_avg_n__(5, n, 'SP', input_data.index)
            ft_mx.loc[5:5 + n, 'sp_price_avg_5'] = sp_price_avg_5
        sp_price_avg_30 = self.__price_avg_n__(30, n, 'SP', input_data.index)
        ft_mx.loc[30:30 + n, 'sp_price_avg_30'] = sp_price_avg_30

        # check weather it is forecast or training
        if forward_step == 0:
            return ft_mx[:n]
        else:
            return ft_mx[n : n + forward_step]

    def train(self):
        import ipdb; ipdb.set_trace()
        train_result = {}
        ft_mx = self.__create_feature_mx__(self.input_data, self.po_corr_data, self.neg_corr_data)
        ft_mx = self.__clean_ft_mx__(ft_mx)
        x = ft_mx.drop('price', 1)
        y = ft_mx['price']
        trained_model = self.model.fit(x, y)
        predicted = trained_model.predict(x)
        error_mean, error_std = self.__calculate_insample_error__(np.array(predicted), np.array(y.tolist()))
        train_result['trained_model'] = trained_model
        train_result['error'] = (error_mean, error_std)
        train_result['last_price'] = ft_mx['price'].tolist()[-1]
        return train_result

    def forecast(self, forward_step):
        train_result = self.train()
        trained_model = train_result['trained_model']
        forecast_ft_mx = self.__create_feature_mx__(self.input_data, self.po_corr_data,
                                                    self.neg_corr_data, forward_step)
        #Delete price data
        del forecast_ft_mx['price']
        forecast_ft_mx = self.__clean_ft_mx__(forecast_ft_mx)
        forecast_price = trained_model.predict(forecast_ft_mx)
        forecast_result = {}
        forecast_result['price'] = forecast_price
        forecast_result['return'] = (forecast_price[-1] - train_result['last_price']) / train_result['last_price']
        forecast_result['error'] = train_result['error']
        return forecast_result

if __name__ == '__main__':
    from forecast_server.engine.ForecastModels import SVRModel
    ml_model = SVRModel()
    df = pd.read_csv('output/stock_raw_data/AA.csv')[-730:]
    df_po = pd.read_csv('output/stock_raw_data/AAN.csv')[-730:]
    df_neg = pd.read_csv('output/stock_raw_data/AAP.csv')[-730:]
    fcster = Forecaster(df, df_po, df_neg, ml_model)
    forecast_result = fcster.forecast(5)


