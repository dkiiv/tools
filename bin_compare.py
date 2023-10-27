import os

def compare_binary_files(file1_path, file2_path):
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2, open('binCompare.bin', 'wb') as file3:
        while True:
            byte1 = file1.read(1)
            byte2 = file2.read(1)
            
            if not byte1 and not byte2:
                file1.close()
                file2.close()
                file3.close()
                if not exportDiff: os.remove("binCompare.bin")
                break
            
            address = file1.tell() - 1  # Address of the difference
            if byte1 != byte2:
                print(f"{hex(address)}: ORIGINAL {bytes.hex(byte1)} | NEW {bytes.hex(byte2)}")
                if exportDiff: file3.write(byte2)
            else:
                if exportDiff: file3.write(b'\x00')

if __name__ == "__main__":
    file1_path = input("Dir path to file 1: ")
    file2_path = input("Dir path to file 2: ")
    exportDiff = input("""Do you want to export a BIN
file highlighting the changes from file 2? y/n: """)
    if exportDiff == "y":
        exportDiff = True
    else:
        exportDiff = False

    try:
        compare_binary_files(file1_path, file2_path)
    except FileNotFoundError:
        print("One or both of the files do not exist.")