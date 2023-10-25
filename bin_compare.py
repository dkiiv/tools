def compare_binary_files(file1_path, file2_path):
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
        while True:
            byte1 = file1.read(1)
            byte2 = file2.read(1)
            
            if not byte1 and not byte2:
                break
            
            address = file1.tell() - 1  # Address of the difference
            if byte1 != byte2:
                print(f"{hex(address)}: ORIGINAL {bytes.hex(byte1)} | NEW {bytes.hex(byte2)}")

if __name__ == "__main__":
    file1_path = input("Dir path to file 1: ")
    file2_path = input("Dir path to file 2: ")

    try:
        compare_binary_files(file1_path, file2_path)
    except FileNotFoundError:
        print("One or both of the files do not exist.")