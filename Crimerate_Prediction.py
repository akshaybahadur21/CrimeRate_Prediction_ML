
from matplotlib import pyplot
from pandas import DataFrame
from pandas import Series
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
from math import sqrt
 
# create a differenced series
def difference(dataset, interval=1):
	diff = list()
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff.append(value)
	return diff
 
# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]
 
# load data
series = Series.from_csv('C:\\Users\\akshaybahadur21\\Documents\\GitHub\\CrimeRate_Prediction_MachineLearning\\Daily_Incidents_of_Crime_Dummy.csv')
# prepare data
X = series.values
# print X
X = X.astype('float32')
train_size = int(len(X) * 0.50)
train, test = X[0:train_size], X[train_size:]
# walk-forward validation
history = [x for x in train]
predictions = list()
bias=0.409864
for i in range(len(test)):
	# difference data
	months_in_year = 30
	diff = difference(history, months_in_year)
	# predict
	model = ARIMA(diff, order=(1,0,0))
	model_fit = model.fit(trend='nc', disp=0)
	yhat = model_fit.forecast()[0]
	yhat = bias + inverse_difference(history, yhat, months_in_year)
	# yhat = inverse_difference(history, yhat, months_in_year)
	predictions.append(yhat)
	# observation
	obs = test[i]
	history.append(obs)
	print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
# report performance
# residuals = [test[i]-predictions[i] for i in range(len(test))]
# residuals = DataFrame(residuals)
# print(residuals.describe())
mse = mean_squared_error(test, predictions)
rmse = sqrt(mse)
print('RMSE: %.3f' % rmse)
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()