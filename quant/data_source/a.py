#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author = 'wyx'
@time = 2019-04-02 15:53
@annotation = ''
"""
import os

import pandas as pd
from keras import Sequential
from keras.layers import Dense
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

BUNDLE_DIR = os.path.join(os.path.dirname(__file__), "bundle")
HDF5_COMP_LEVEL = 4
HDF5_COMP_LIB = 'blosc'
# pair = 'binance_bcc_btc'
pair = 'okfuture_btc_usd_this_week'


def save_h5(key, value):
    h5_file_path = os.path.join(BUNDLE_DIR, pair + ".h5")
    with pd.HDFStore(h5_file_path, complevel=HDF5_COMP_LEVEL, complib=HDF5_COMP_LIB) as h5:
        h5.put(key, value)


def get_h5(key):
    h5_file_path = os.path.join(BUNDLE_DIR, pair + ".h5")
    return pd.read_hdf(h5_file_path, key)


def clf_data_set(one_hot=False):
    X, y = get_h5('new_x'), get_h5('new_y')
    f = y.groupby(['change_type']).agg({'change_type':'count'})
    y = y['change_type'].values.reshape(-1, 1)
    if one_hot:
        enc = OneHotEncoder()
        y[y == -1] = 2
        a = enc.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    return X_train, X_test, y_train, y_test


def reg_data_set():
    X, y = get_h5('new_x'), get_h5('new_y')
    y = y['change'].values.reshape(-1, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    print(X_train.shape)
    print(X_test.shape)
    print(y_train.shape)
    print(y_test.shape)
    return X_train, X_test, y_train, y_test


def linreg():
    X_train, X_test, y_train, y_test = reg_data_set()
    reg = RandomForestRegressor()
    reg.fit(X_train, y_train)
    print(reg.score(X_test, y_test))


# linreg()


def linclf():
    X_train, X_test, y_train, y_test = clf_data_set()
    clf = RandomForestClassifier(n_estimators=20,min_samples_leaf=8,min_samples_split=10,n_jobs=-1)
    clf.fit(X_train, y_train)
    # y_pred = cross_val_predict(reg, X_train, y_train, cv=5)
    # y_pred = clf.predict(X_test)
    print(clf.score(X_test, y_test))


# linclf()


def kclf():
    CLASSES = 3
    HIDDEN = 100
    DIM = 193
    X_train, X_test, y_train, y_test = clf_data_set(one_hot=True)

    # y_train[y_train == -1] = 2
    # y_test[y_test == -1] = 2
    # y_train = y_train.reshape(1,-1)
    # y_test = y_test.reshape(1,-1)
    model = Sequential()
    model.add(Dense(256, input_shape=(DIM,), activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(CLASSES, activation='softmax'))
    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['categorical_accuracy'])
    model.fit(X_train, y_train,
              batch_size=200, epochs=200,
              verbose=1, validation_split=0.2, shuffle=False)
    score = model.evaluate(X_test, y_test)
    print(model.metrics_names)
    print("\nTest score:", score[0])
    print('Test accuracy:', score[1])


kclf()
