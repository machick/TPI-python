import numpy
import pandas as pd
import requests
import tensorflow as keras
from keras import Sequential
from keras.layers import LSTM, Dense, Flatten, TimeDistributed, Conv1D, MaxPooling1D
from keras.models import load_model
from datetime import datetime, timedelta
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# data preparation
def download_usd():
    url = 'http://infra.datos.gob.ar/catalog/sspm/dataset/168/distribution/168.1/download/datos-tipo-cambio-usd-futuro-dolar-frecuencia-diaria.csv'
    r = requests.get(url)
    with open('dolar.csv', 'wb') as f:
        f.write(r.content)


def split_sequence(sequence, n_steps):
    """
    split a univariate sequence into samples
    """
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return numpy.array(X), numpy.array(y)

# download most recent data from datos.gob.ar

def updateCsv():
    url = 'https://api.bluelytics.com.ar/v2/evolution.csv'
    r = requests.get(url)
    with open('dolar.csv', 'wb') as f:
        f.write(r.content)
    return {"message": "Datos dolar actualizados"}

def getDolarBlueHistory():
    print("INICIO getDolarBlueHistory")
    data = pd.read_csv("./dolar.csv").iloc[::-1]
    _filter = data["type"].isin(["Blue"])
    print("FIN getDolarBlueHistory")            
    return data[_filter]

def getSaludo():
    download_usd()
    return {"dolar": "Hola soy el dolar"}

def getDolarTraining():
    data = getDolarBlueHistory()
    print("INICIO getDolarTraining")
    data['value_sell'] = data['value_sell'].fillna(data['value_sell'].median())
    historic_data = data.value_sell.values[:-20]
    print("historic_data")
    print(historic_data)
    # choose a number of time steps
    n_steps = 4

    # split into samples
    X, y = split_sequence(historic_data, n_steps)

    n_features = 1
    n_seq = 2
    n_steps = 2
    n_epochs = 500
    X = X.reshape((X.shape[0], n_seq, n_steps, n_features))

    # model definition
    model = Sequential()
    model.add(TimeDistributed(Conv1D(filters=64,
                                    kernel_size=1,
                                    activation='relu'), input_shape=(None, n_steps, n_features)))
    model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
    model.add(TimeDistributed(Flatten()))
    model.add(LSTM(50, activation='relu'))  # we do no normalization, so use relu
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # model training
    model.fit(X, y, epochs=n_epochs, verbose=0)
    model.save('dolar_model')
    print("FIN getDolarTraining")
    return str("Entrenamiento Finalizado")

def getDolar():
    print("INICIO getDolar")
    n_features = 1
    n_seq = 2
    n_steps = 2

    model = load_model('dolar_model')
    # predict dolar 🐬
    predicted_values = []
    data = getDolarBlueHistory()
    last_predicted = data['value_sell'].fillna(data['value_sell'].median())
    last_predicted = data.value_sell.values[-4:]
    print('last_predicted')
    print(last_predicted)
    n_values_to_predict = 5

    class Precio:
        def __init__(self, fecha, precio):
            self.fecha = fecha
            self.precio = precio

    for x in range(n_values_to_predict):
        x_input = last_predicted.reshape((1, n_seq, n_steps, n_features))
        y = model.predict(x_input, verbose=0)
        y_predicted =float(y.flatten()[0])
        next_date = datetime.now() + timedelta(x)
        date_ = next_date.strftime("%Y-%m-%d")
        precio = Precio(date_,y_predicted)
        predicted_values.append(precio)
        # calculate next batch of samples for prediction,
        # including the last prediction we just did.
        last_predicted = last_predicted[1:]
        last_predicted = numpy.append(last_predicted, [y])

    print(last_predicted)
    jsonStr = json.dumps([obj.__dict__ for obj in predicted_values])
    print("FIN getDolar")
    return jsonStr
    
   # return str([obj.__dict__ for obj in predicted_values])
    #str(predicted_values)

    #pyplot.title("Historico")
    #pyplot.plot(data.tipo_cambio_bna_vendedor)
    #pyplot.xlabel('Indice Tiempo')
    #pyplot.ylabel('Indice Dolar')
    #pyplot.show()
    #
    #pyplot.title("Prediccion " + str(n_values_to_predict) + " Días")
    #pyplot.plot(predicted_values)
    #pyplot.show()