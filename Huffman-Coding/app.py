import streamlit as st
import heapq
import os
import io

class HuffmanCoding:
    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if other is None:
                return False
            if not isinstance(other, HuffmanCoding.HeapNode):
                return False
            return self.freq == other.freq

    def make_frequency_dict(self, text):
        frequency = {}
        for character in text:
            if character not in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self, file_content):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

        frequency = self.make_frequency_dict(file_content)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(file_content)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        byte_array = self.get_byte_array(padded_encoded_text)

        with io.BytesIO() as compressed_file:
            compressed_file.write(byte_array)
            return compressed_file.getvalue()

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, file_content):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

        bit_string = ""
        for byte in file_content:
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits

        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)
        return decompressed_text


def main():
    st.title("Huffman Coding Compression and Decompression")

    operation = st.radio("Select operation:", ["Compress", "Decompress"])

    if operation == "Compress":
        uploaded_file = st.file_uploader("Choose a text file to compress", type=["txt"])

        if uploaded_file is not None:
            st.write("File uploaded successfully!")

            compression_button = st.button("Compress File")

            if compression_button:
                huffman_coding = HuffmanCoding()
                compressed_file_content = huffman_coding.compress(uploaded_file.read())

                # Display the download button for the in-memory compressed file
                download_button = st.download_button(
                    label="Save Compressed File",
                    data=compressed_file_content,
                    key="download_button",
                    file_name=f"{os.path.splitext(os.path.basename(uploaded_file.name))[0]}_compressed.bin"
                )

    elif operation == "Decompress":
        uploaded_file = st.file_uploader("Choose a binary file to decompress", type=["bin"])

        if uploaded_file is not None:
            st.write("File uploaded successfully!")

            decompression_button = st.button("Decompress File")

            if decompression_button:
                huffman_coding = HuffmanCoding()
                decompressed_text = huffman_coding.decompress(uploaded_file.read())

                # Display the download button for the in-memory decompressed file
                download_button = st.download_button(
                    label="Save Decompressed File",
                    data=decompressed_text,
                    key="download_button",
                    file_name=f"{os.path.splitext(os.path.basename(uploaded_file.name))[0]}_decompressed.txt"
                )

if __name__ == "__main__":
    main()
