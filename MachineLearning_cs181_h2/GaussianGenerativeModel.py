from scipy.stats import multivariate_normal
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c

# Please implement the fit and predict methods of this class. You can add additional private methods
# by beginning them with two underscores. It may look like the __dummyPrivateMethod below.
# You can feel free to change any of the class attributes, as long as you do not change any of
# the given function headers (they must take and return the same arguments), and as long as you
# don't change anything in the .visualize() method.
class GaussianGenerativeModel:
    def __init__(self, isSharedCovariance=False):
        self.isSharedCovariance = isSharedCovariance

    # estimate parameters
    def fit(self, X, Y):
        self.X = X
        f = len(X)
        self.Y = Y
        n = len(Y)
        #compute class priors
        self.priors = np.bincount(Y) / float(n)
        c = len(self.priors)
        #compute mle mean and variances
        self.mu = []
        self.sigma = []
        for k in range(c):
            class_subset = X[Y == k]
            self.mu.append(np.mean(class_subset, axis=0))
            if not self.isSharedCovariance:
                #note that np.cov divides by n-1 (unbiased estimate) rather than n (MLE derived in problem 3)
                self.sigma.append(np.cov(class_subset.T))
        if self.isSharedCovariance:
            self.sigma = c * [np.cov(X.T)] #make c copies of shared covariance to make later code cleaner
        print "isSharedCovariance", self.isSharedCovariance
        print "Mu"
        print self.mu
        print "Sigma"
        print self.sigma
        print "Training Loss", np.sum(self.__loss_matrix(X)[np.arange(n), Y])
        print
        return

    #get the matrix of negative log likelihood for data points
    def __loss_matrix(self, X):
        n = len(X)
        c = len(self.priors)
        L = np.empty((n, c))
        for k in range(c):
            L[:, k] = - multivariate_normal.logpdf(X, self.mu[k], self.sigma[k]) - np.log(self.priors[k])
        return L

    # predict new data points
    def predict(self, X_to_predict):
        return np.argmin(self.__loss_matrix(X_to_predict), axis=1)

    # Do not modify this method!
    def visualize(self, output_file, width=3, show_charts=False):
        X = self.X

        # Create a grid of points
        x_min, x_max = min(X[:, 0] - width), max(X[:, 0] + width)
        y_min, y_max = min(X[:, 1] - width), max(X[:, 1] + width)
        xx,yy = np.meshgrid(np.arange(x_min, x_max, .005), np.arange(y_min,
            y_max, .005))

        # Flatten the grid so the values match spec for self.predict
        xx_flat = xx.flatten()
        yy_flat = yy.flatten()
        X_topredict = np.vstack((xx_flat,yy_flat)).T

        # Get the class predictions
        Y_hat = self.predict(X_topredict)
        Y_hat = Y_hat.reshape((xx.shape[0], xx.shape[1]))

        cMap = c.ListedColormap(['r','b','g'])

        # Visualize them.
        plt.figure()
        plt.pcolormesh(xx,yy,Y_hat, cmap=cMap)
        plt.scatter(X[:, 0], X[:, 1], c=self.Y, cmap=cMap)
        plt.savefig(output_file)
        if show_charts:
            plt.show()
