import struct


class Node:
    val = 0

    def __init__(self, char, value):
        self.left_node = None
        self.right_node = None
        self.val = value
        self.char = char


class Huffman_encode:
    def __init__(self):
        self.__freq_word = []
        self.tree = Node(None, 0)
        self.encode_dic = {}

    def encode(self, input_file, output_file_path):
        self.__freq_word = self.char_freq(input_file)
        hfm_tree = Huffman_tree()
        self.tree = hfm_tree.build_tree_from_freq(self.__freq_word)
        self.encode_dic = hfm_tree.code_from_tree(self.tree)
        total_len_bin = 0

        for c in self.encode_dic:
            total_len_bin += self.__freq_word[c] * len(self.encode_dic[c])

        add_bits = 8 - total_len_bin % 8

        # write encode information to the file head
        output_file = open(output_file_path, "c")
        for c in self.encode_dic:
            code_str = c + ":" + self.encode_dic[c] + "\n"
            output_file.write(code_str)
        output_file.write("appends:" + str(add_bits))
        output_file.close()

        try:
            write = ""
            in_file = open(input_file, 'rb')
            chunk = in_file.read(1)
            while chunk:
                char = struct.unpack('c', bytes(chunk))[0]
                # print(char)
                code = self.encode_dic[char]
                write = write + code

                chunk = in_file.read(1)
        finally:
            in_file.close()
        return

    def write_file(self, str_code, output_file_path):
        try:
            out_file = open(output_file_path, 'wa')
            l = len(str_code)
            if l % 8 != 0:
                n = 8 - l % 8
                str_add = "0" * n
                str_code = str_code + str_add
            while len(str_code) > 8:
                str_write = str_code[0:8]
                str_code = str_code[8:]
                code_write = bytes(int(str_write, 2))
                out_file.write(code_write)
        finally:
            out_file.close()

    def char_freq(self, input_file):
        encode_file = open(input_file, 'rb')
        try:
            chunk = encode_file.read(1)
            while chunk:
                char = struct.unpack('c', bytes(chunk))[0]
                # print(char)
                if char in self.encode_dic:
                    self.encode_dic[char] = self.encode_dic[char] + 1
                else:
                    self.encode_dic[char] = 1
                chunk = encode_file.read(1)
        finally:
            encode_file.close()
        return self.encode_dic


class Huffman_tree:
    nodes = []

    def __init__(self):
        self.root = None
        self.nodes = None

    def build_tree_from_freq(self, char_freq):
        node_list = []
        for c in char_freq:
            node_temp = Node(c, char_freq[c])
            node_list.append(node_temp)
        self.nodes = node_list
        while (self.nodes.__len__() > 1):
            self.nodes = self.__sort()
            min1 = self.nodes[0]
            min2 = self.nodes[1]
            temp = Node(None, min1.val + min2.val)
            temp.left_node = min1
            temp.right_node = min2
            del self.nodes[0]
            del self.nodes[0]
            self.nodes.append(temp)
        return self.nodes[0]

    def build_tree_from_code(self, code_dic):
        return

    def code_from_tree(self, root):
        dic = {}
        if root.char is not None:
            return {str(root.char): ""}
        else:
            dic_left = self.code_from_tree(root.left_node)
            for c in dic_left:
                dic_left[c] = "0" + dic_left[c]

            dic_right = self.code_from_tree(root.right_node)
            for c in dic_right:
                dic_right[c] = "1" + dic_right[c]
            dic = dict(dic_left, **dic_right)
        return dic

    def __sort(self):
        return sorted(self.nodes, key=lambda Node: Node.val)


class Huffman_decode:
    def __init__(self, encode_dic):
        self.dic = encode_dic


if __name__ == '__main__':
    # n1 = Node(10)
    # n2 = Node(12)
    # n3 = Node(1)
    # n4 = Node(2)
    # n5 = Node(3432)
    # n6 = Node(25)
    # n7 = Node(6)
    # n8 = Node(42)
    #
    # nl = [n1, n2, n3, n4, n5, n6, n7, n8]
    # hfm = Huffman_tree()
    # file_path = "Aesop_Fables.txt"
    # hfm_encode = Huffman_encode()
    # freq = hfm_encode.char_freq(file_path)
    # nn = sorted(freq.items(), key=lambda d: d[1], reverse=True)
    # # for n in nn:
    # #     print(n.val)
    # root = hfm.build_tree_from_freq(freq)
    # print(nn)
    #
    # code = hfm.code_from_tree(root)
    # print(code)

    # print("finish")
    # print("hahah")

    file_test = "test.txt"
    file = open(file_test, 'a+')
    str1 = "01010101"
    str2 = "10010011"
    code = str(chr(int(str1, 2)))
    print(code)
    file.write(code)
    code = str(chr(int(str2, 2)))
    print(code)
    file.write(code)
    file.close()

    input = open(file_test, 'rb')
    chunk = input.read(1)
    char = struct.unpack('c', bytes(chunk))[0]
    s = str(char)
    print(s)

    chunk = input.read(1)
    char = struct.unpack('c', bytes(chunk))[0]
    s = str(char)
    print(s)
