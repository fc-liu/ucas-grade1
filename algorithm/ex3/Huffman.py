import struct

"""
present struct for tree node
"""


class Node:
    val = 0

    def __init__(self, char, value):
        self.left_node = None
        self.right_node = None
        self.val = value
        self.char = char


"""
class implement Huffman encode
"""


class Huffman_encode:
    def __init__(self):
        self.__freq_word = []
        self.tree = Node(None, 0)
        self.encode_dic = {}
        self.append_key = "appends"
        self.end_flag = "end\n"

    """
    method to encode the input_file and write to output_file
    """

    def encode(self, input_file, output_file_path):
        self.__freq_word = self.char_freq(input_file)
        print(self.__freq_word)
        hfm_tree = Huffman_tree()
        self.tree = hfm_tree.build_tree_from_freq(self.__freq_word)
        self.encode_dic = hfm_tree.code_from_tree(self.tree)
        print(self.encode_dic)
        total_len_bin = 0

        #
        for c in self.encode_dic:
            total_len_bin += self.__freq_word[c] * len(self.encode_dic[c])

        add_bits = 8 - total_len_bin % 8

        # write encode information to the file head
        output_file = open(output_file_path, "w")
        for c in self.encode_dic:
            code_str = c + ":" + self.encode_dic[c] + "\n"
            output_file.write(code_str)
        output_file.write((self.append_key + ":" + str(add_bits) + "\n"))
        output_file.write(self.end_flag)
        output_file.close()

        try:
            write = ""
            in_file = open(input_file, 'r')
            chunk = in_file.readline()
            while chunk:
                for char in chunk:
                    # char = struct.unpack('c', bytes(chunk))[0]
                    # print(char)
                    code = self.encode_dic[char]
                    write = write + code
                    buffer_size = 256
                    if len(write) > buffer_size:
                        self.write_file(write[:buffer_size], output_file_path)
                        write = write[buffer_size:]
                chunk = in_file.readline()
            self.write_file(write, output_file_path)
        finally:
            in_file.close()
        return

    def write_file(self, str_code, output_file_path):
        try:
            out_file = open(output_file_path, 'ab')
            l = len(str_code)
            if l % 8 != 0:
                n = 8 - l % 8
                str_add = "0" * n
                str_code = str_code + str_add
            while len(str_code) >= 8:
                str_write = str_code[0:8]
                str_code = str_code[8:]
                code_write = int(str_write, 2)
                out_file.write(struct.pack('B', code_write))
        finally:
            out_file.close()

    def char_freq(self, input_file):
        encode_file = open(input_file, 'r')
        try:
            chunk = encode_file.readline()
            while chunk:
                for char in chunk:
                    if char in self.encode_dic:
                        self.encode_dic[char] = self.encode_dic[char] + 1
                    else:
                        self.encode_dic[char] = 1
                chunk = encode_file.readline()
        finally:
            encode_file.close()
        print(self.encode_dic)
        return self.encode_dic


"""
class implement Huffman tree
"""


class Huffman_tree:
    nodes = []

    def __init__(self):
        self.root = None
        self.nodes = None

    """
    build a huffman tree from char frequency
    """

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

    """
    build a huffman tree from Huffman code

    """

    def build_tree_from_code(self, code_dic):
        root = Node(None, 0)
        for code_key in code_dic:
            temp = root
            code = code_dic[code_key]
            for c in code:
                if c == '0':
                    if temp.left_node is None:
                        temp.left_node = Node(None, 0)
                    temp = temp.left_node
                else:
                    if temp.right_node is None:
                        temp.right_node = Node(None, 0)
                    temp = temp.right_node
            temp.char = code_key
        print("build tree from code finish!!!!!")
        return root

    """
    get Huffman code from Huffman tree
    """

    def code_from_tree(self, root):
        dic = {}
        if root.char is not None:
            return {root.char: ""}
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


"""
class implement Huffman decode
"""


class Huffman_decode:
    def __init__(self):
        self.dic = {}
        self.append_key = "appends"
        self.end_flag = "end"
        self.root = None

    """
    chief method to decode a compressed file
    """

    def decode(self, input_file_path, output_file_path):
        print("start decode!!!!!")
        encode_file = open(input_file_path, 'rb')
        self.dic = self.get_encode_dic(encode_file)
        appends_count = self.dic[self.append_key]
        del self.dic[self.append_key]
        ori_text = ""

        hfm_tree = Huffman_tree()
        self.root = hfm_tree.build_tree_from_code(self.dic)
        chunk = encode_file.read(1)
        temp_node = self.root

        # scan the compressed part file
        while chunk:
            integer = struct.unpack('B', bytes(chunk))[0]
            bin_str = self.__int2binStr(integer)
            chunk = encode_file.read(1)

            # meet the last byte of the compressed file, should omit the added bits
            if chunk is None:
                bin_str = bin_str[:8 - appends_count]

            c = ''

            # get the real char through searching the Huffman tree
            for sc in bin_str:
                if temp_node.char:
                    c = temp_node.char
                    temp_node = self.root
                    # print(str(c))
                    ori_text += c
                if sc == '0':
                    temp_node = temp_node.left_node
                else:
                    temp_node = temp_node.right_node

        decode_file = open(output_file_path, 'w')
        decode_file.write(ori_text)

    """
    get Huffman code from compressed file head
    """

    def get_encode_dic(self, file):
        encode_dic = {}
        str_line = file.readline()
        str_line = str_line.decode('ascii')[:-1]
        while str_line != self.end_flag:
            # print(str_line)
            par = str_line.split(':')

            # special case for character : ":"
            if len(par) == 3:
                par[0] = ':'
                par[1] = par[2]

            # special case for character : "\n"
            if len(par) < 2:
                str_line = file.readline().decode('ascii')[:-1]
                par = str_line.split(":")
                par[0] = "\r\n"
            # print(par[1])
            if par[0] not in encode_dic:
                encode_dic[par[0]] = par[1]
            str_line = file.readline().decode('ascii')[:-1]
        print("finish get encode dic!!!")
        return encode_dic

    """
    tramsform an integer to the responsding binary string
    """

    def __int2binStr(self, number):
        s = bin(number).replace('0b', '')
        s = "0" * (8 - len(s)) + s
        return s


"""
main method
"""
if __name__ == '__main__':
    input_1_file = "Aesop_Fables.txt"
    encode_1_file = "encode_Ae.txt"
    decode_1_file = "decode_As.txt"
    input_2_file = "graph.txt"
    encode_2_file = "encode_g.txt"
    decode_2_file = "decode_g.txt"

    hfm_encode = Huffman_encode()
    hfm_decode = Huffman_decode()
    hfm_encode.encode(input_1_file, encode_1_file)
    hfm_decode.decode(encode_1_file, decode_1_file)

    hfm_encode = Huffman_encode()
    hfm_decode = Huffman_decode()
    hfm_encode.encode(input_2_file, encode_2_file)
    hfm_decode.decode(encode_2_file, decode_2_file)
