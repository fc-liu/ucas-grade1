class IOHelper:
    def __init__(self, file):
        try:
            self.file = open(file)
        except Exception as e:
            print(e)

    def get_next_data(self):
        line = self.file.readline()
        while line and line[0] == "#":
            line = self.file.readline()
        line = self.file.readline()
        if not line:
            return None
        line1 = line.strip(" \n")
        # print(line1)
        line2 = self.file.readline().strip(" \n")
        list1 = str.split(line1, " ")
        list2 = str.split(line2, " ")
        ret = [[], []]
        for item in list1:
            ret[0].append(int(item))
        for item in list2:
            ret[1].append(int(item))
        return ret

    def close(self, ):
        self.file.close()


class P1Helper:
    def __init__(self, file):
        try:
            self.file = open(file)
        except Exception as e:
            print(e)

    def get_next_jobs(self):
        line = self.file.readline()
        jobs = []
        while line[0] == "#":
            line = self.file.readline()
        job = []
        line = self.file.readline()
        while line[0] != " ":
            ids = str.split(line, " ")
            job.append(ids[0], ids[1])
            jobs.append(job)

        return jobs


if __name__ == '__main__':
    io = IOHelper("problem2.data")
    data = io.get_next_data()
    print(data)
    data = io.get_next_data()
    print(data)
    data = io.get_next_data()
    print(data)
