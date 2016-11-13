import csv
from sklearn import linear_model
import time
from datetime import datetime
from matplotlib import pyplot as plt
import numpy


def csvread(file):
    reader = csv.reader(open(file, "r"))
    k = 0;

    for item in reader:
        print(item)
        k += 1
        if k > 100:
            return reader


def csvwrite(file, data):
    writer = csv.writer(open(file, "a"))

    for i in data:
        writer.writerow(i)


def read_key(file):
    reader = csv.reader(open(file, "r"))
    key = {}
    for item in reader:
        prov = item[1]
        type = item[3]
        if prov in key:
            val = key[prov]
            if type not in val:
                val.append(type)
        else:
            key[prov] = [type]
    return key


def extract_farm_data(file, key):
    reader = csv.reader(open(file, "r"))
    data = []
    for item in reader:
        prov = item[1]
        type = item[3]
        if prov in key:
            val = key[prov]
            if type in val:
                data.append(item)

    return data


def csv_count(file):
    reader = csv.reader(open(file, "r"))
    k = 0
    for item in reader:
        k += 1

    return k


def get_linear_regr(x_list, y_list):
    regr = linear_model.LinearRegression()
    regr.fit(x_list, y_list)

    return regr


def train(train_file, predic_file, res_file):
    train_reader = csv.reader(open(train_file, 'r'))
    predic_reader = csv.reader(open(predic_file, 'r'))
    res_writer = csv.writer(open(res_file, 'a'))

    very_begin = str2datetime("2015-10-01")

    train_data_dic = {}
    lin_regr_dic = {}
    # get train date set model
    for item in train_reader:
        # print(item)
        prov = item[1]
        type = item[3]
        t_str = item[12]
        t = str2datetime(t_str)
        t_dif = day_diff(t, very_begin)
        price = float(item[9])
        if prov in train_data_dic:
            type_dic = train_data_dic[prov]
            if type in type_dic:
                train_data_dic[prov][type][t_dif] = price
            else:
                train_data_dic[prov][type] = {t_dif: price}

        else:
            train_data_dic[prov] = {type: {t_dif: price}}
            # print(train_data_dic[prov])

    # get linear regression
    for prov in train_data_dic:
        for type_dic in train_data_dic[prov]:
            x_list = list(train_data_dic[prov][type_dic].keys())
            x = []
            for i in x_list:
                x.append([i])
            y = list(train_data_dic[prov][type_dic].values())
            # print("x : " + str(x))
            # print("y : " + str(y))
            regr = get_linear_regr(x, y)
            par = regr.get_params()
            print(par)
            if prov in lin_regr_dic:
                lin_regr_dic[prov][type_dic] = regr

            else:
                lin_regr_dic[prov] = {type_dic: regr}

    for item in predic_reader:
        prov = item[1]
        type = item[3]
        t_str = item[9]
        t = str2datetime(t_str)
        t_dif = day_diff(t, very_begin)
        # print(write_row)
        regr = lin_regr_dic[prov][type]
        predict_price = round(regr.predict(t_dif)[0], 3)
        if predict_price < 0:
            predict_price = abs(predict_price)
        print(predict_price)
        write_row = [item[1], item[3], item[9], predict_price]
        res_writer.writerow(write_row)


def str2datetime(s_time):
    format_str = "%Y-%m-%d"
    t = time.strptime(s_time, format_str)
    return datetime(t[0], t[1], t[2])


def day_diff(day1, day2):
    return (day1 - day2).days


def plot_figure(x_list, y_list, a):
    plt.figure(figsize=(8, 5), dpi=80)
    axes = plt.subplot(111)
    type1_x = []
    type1_y = []

    x = numpy.linspace(-10.0, 10.0)
    y = -(a[2] + x * a[0]) / a[1]
    plt.plot(x, y, 'r.-')

    for i in x_list:
        i = i[0]

    type1 = axes.scatter(x_list, y_list, s=20, c='red')
    plt.xlabel('x1')
    plt.ylabel('x2')
    axes.legend((type1, type2, type3, type4), ("w1", "w2", "w3", "w4"), loc=2)

    plt.show()


if __name__ == '__main__':
    file_dir = "/home/lfc/Desktop/"
    farm = file_dir + "farming.csv"
    prod = file_dir + "product_market.csv"
    keys = file_dir + "key.csv"
    extract_file = file_dir + "extract.csv"
    predict_file = file_dir + "predict.csv"
    # csvread(farm)
    # reader = csvread(prod)
    # key = read_key(prod)
    # key = read_key(prod)
    # print(key)
    # extract_data = extract_farm_data(farm, key)
    # csvwrite(extract_file, extract_data)

    # k = csv_count(farm)
    # print(k)
    train(extract_file, prod, predict_file)

    # csvwrite(out, reader)
