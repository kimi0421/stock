from sklearn.svm import SVR

class SVRModel:

    def __init__(self, parameters=None):
        if parameters is not None:
            self.C = parameters['C']
            self.epsilon = parameters['epsilon']
        else:
            self.C = 5
            self.epsilon = 0.5
        self.clf = SVR(C=self.C, epsilon=self.epsilon)


    def fit(self, x, y):
        self.clf.fit(x, y)
        return self.clf
