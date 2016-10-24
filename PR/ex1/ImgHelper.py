import struct
import numpy


# import matplotlib.pyplot as plt
# import matplotlib.cm as cm


class Img:
    def __init__(self, img_path, lb_path):
        self.__img_file_path = img_path  # "train-images.idx3-ubyte"
        self.__lb_file_path = lb_path  # "train-labels.idx1-ubyte"
        self.amount = 0
        self.rows = 0
        self.cols = 0
        self.__offset = 0
        self.__img_file = open(self.__img_file_path, 'rb')
        self.__label_file = open(self.__lb_file_path, 'rb')
        self.__init_img()
        self.__init_label()
        # self.pixels = self.rows * self.cols
        self.current_img = 0

    def next_img(self):
        # print("current_img")
        # print(self.current_img)
        if self.current_img < self.amount:
            img_offset = 16 + self.current_img * self.rows * self.cols
            label_offset = 8 + self.current_img
            self.__img_file.seek(img_offset)
            self.__label_file.seek(label_offset)
            dim = self.rows * self.cols
            img = numpy.zeros(dim)
            for i in range(0, dim):
                chunk = self.__img_file.read(1)
                if chunk:
                    pixel = struct.unpack('>B', bytes(chunk))[0]
                    img[i] = pixel
            label = self.__label_file.read(1)
            # print(label)
            if label:
                label = struct.unpack('>B', bytes(label))[0]
            self.current_img += 1
            return [img, label]
        else:
            self.close()
            return None

    def close(self):
        self.__img_file.close()
        self.__label_file.close()

    def __init_img(self):
        try:
            # while True:
            self.__img_file.seek(4)
            chunk = self.__img_file.read(4)
            self.amount = struct.unpack('>I', bytes(chunk))[0]
            chunk = self.__img_file.read(4)
            self.rows = struct.unpack('>I', bytes(chunk))[0]
            chunk = self.__img_file.read(4)
            self.cols = struct.unpack('>I', bytes(chunk))[0]
            # if not chunk:
            #     break
            # print("amount : ")
            # print(self.amount)
            # print("rows : ")
            # print(self.rows)
            # print("cols : ")
            # print(self.cols)
        except Exception as err:
            print(err)

    def __init_label(self):
        try:
            # while True:
            self.__label_file.seek(8)
        except Exception as err:
            print(err)


if __name__ == '__main__':
    a = Img("train-images.idx3-ubyte", "train-labels.idx1-ubyte")
    # a = Img("t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte")
    p = a.next_img()
    # plt.imshow(p[0], cmap=cm.gray)
    # print(p[0])
    # print(p[1])
    # print(numpy.size(p[0]))
