import os

def delete_txt_files(data_folder):
    # Iterate over files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_folder, filename)
            # Delete the file
            os.remove(file_path)
            print(f"Deleted: {file_path}")

def main():
    # Specify the path to the data folder
    data_folder = '../data'

    # Delete .txt files in the data folder
    delete_txt_files(data_folder)

if __name__ == "__main__":
    main()