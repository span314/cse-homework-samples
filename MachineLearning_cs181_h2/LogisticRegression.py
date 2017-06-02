import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as c
from scipy.misc import logsumexp

# Please implement the fit and predict methods of this class. You can add additional private methods
# by beginning them with two underscores. It may look like the __dummyPrivateMethod below.
# You can feel free to change any of the class attributes, as long as you do not change any of
# the given function headers (they must take and return the same arguments), and as long as you
# don't change anything in the .visualize() method.
class LogisticRegression:
    def __init__(self, eta, lambda_parameter):
        self.eta = eta
        self.lambda_parameter = lambda_parameter
        self.num_classes = 3

    # Fit logistic regression
    def fit(self, X, C):
        #append bias
        self.X = self.__append_bias(X)
        self.C = C
        #one-hot encode y
        n, m = self.X.shape #number of data points and features
        self.Y = np.zeros((n, self.num_classes))
        self.Y[np.arange(n), self.C] = 1
        #initialize weights to 1
        self.w = np.ones((m, self.num_classes))
        #initialize losses
        self.losses = [self.__loss()]
        itercount = 0
        #gradient descent
        while itercount < 1000000:
            self.w -= self.eta * self.__gradloss()
            self.losses.append(self.__loss())
            itercount += 1
            if abs(self.losses[itercount] - self.losses[itercount - 1]) < self.eta:
                break #close enough
        else:
            print "Convergence warning: reached max number of iterations in gradient descent"

        print "Eta", self.eta
        print "Lambda", self.lambda_parameter
        print "Iterations", itercount
        print "Loss", self.losses[-1]
        print "Weights (bias in last row)"
        print self.w
        return

    def __append_bias(self, X):
        return np.append(X, np.ones((X.shape[0], 1)), axis=1)

    #loss function, negative log-likelihood
    def __loss(self):
        p = self.__prob(self.X) * self.Y
        pdata = np.sum(p, axis=1) #only one term per row will be non-zero
        return -np.sum(np.log(pdata)) + self.lambda_parameter * np.sum(np.square(self.w))

    #gradient of loss function
    def __gradloss(self):
        return np.dot(self.X.T, self.__prob(self.X) - self.Y) + 2 * self.lambda_parameter * self.w

    #softmax function
    def __softmax(self, z):
        expz = np.exp(z)
        norm = np.sum(expz, axis=1).reshape(z.shape[0], 1)
        return expz / norm

    #class probabilities for X
    def __prob(self, X):
        return self.__softmax(np.dot(X, self.w))

    #predict classes
    def predict(self, X_to_predict):
        X = self.__append_bias(X_to_predict)
        return np.argmax(self.__prob(X), axis=1)

    #plot losses
    def plot_losses(self, output_file):
        plt.figure()
        plt.plot(np.arange(len(self.losses)), self.losses)
        plt.title("Logistic Regression Training: Gradient Descent")
        plt.xlabel("Iterations")
        plt.ylabel("Loss")
        plt.savefig(output_file)

    def visualize(self, output_file, width=2, show_charts=False):
        X = self.X

        # Create a grid of points
        x_min, x_max = min(X[:, 0] - width), max(X[:, 0] + width)
        y_min, y_max = min(X[:, 1] - width), max(X[:, 1] + width)
        xx,yy = np.meshgrid(np.arange(x_min, x_max, .05), np.arange(y_min,
            y_max, .05))

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
        plt.scatter(X[:, 0], X[:, 1], c=self.C, cmap=cMap)
        plt.savefig(output_file)
        if show_charts:
            plt.show()
