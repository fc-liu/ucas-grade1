import csv


def get_datalist(file):
    reader = csv.reader(open(file, "r"))
    data = []
    for item in reader:
        temp = []
        for cell in item:
            temp.append(float(cell))
        data.append(temp)
    return data


if __name__ == '__main__':
    file = "data.csv"
    data = get_datalist(file)
    print(data)
