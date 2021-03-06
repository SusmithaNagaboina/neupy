import theano
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn import model_selection, metrics, datasets
from neupy import algorithms, layers, environment
from neupy.exceptions import StopTraining


environment.reproducible()
theano.config.floatX = 'float32'

mnist = datasets.fetch_mldata('MNIST original')

target_scaler = OneHotEncoder()
target = mnist.target.reshape((-1, 1))
target = target_scaler.fit_transform(target).todense()

data = mnist.data / 255.
data = data - data.mean(axis=0)

x_train, x_test, y_train, y_test = model_selection.train_test_split(
    data.astype(np.float32),
    target.astype(np.float32),
    test_size=(1 / 7.)
)

network = algorithms.Momentum(
    [
        layers.Input(784),
        layers.Relu(500),
        layers.Relu(300),
        layers.Softmax(10),
    ],

    # Using categorical cross-entropy as a loss function.
    # It's suitable for classification with 3 and more classes.
    error='categorical_crossentropy',

    # Learning rate
    step=0.01,

    # Shows information about algorithm and
    # training progress in terminal
    verbose=True,

    # Randomly shuffles training dataset before every epoch
    shuffle_data=True,

    momentum=0.99,
    # Activates Nesterov momentum
    nesterov=True,
)
network.architecture()
network.train(x_train, y_train, x_test, y_test, epochs=20)

y_predicted = network.predict(x_test).argmax(axis=1)
y_test = np.asarray(y_test.argmax(axis=1)).reshape(len(y_test))

print(metrics.classification_report(y_test, y_predicted))
score = metrics.accuracy_score(y_test, y_predicted)
print("Validation accuracy: {:.2%}".format(score))
