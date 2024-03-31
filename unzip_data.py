import os
import zipfile

def unzip_files(source_dir, dest_dir):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".zip"):
            zip_file_path = os.path.join(source_dir, filename)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(dest_dir)

if __name__ == "__main__":

    raw_data_dir = r"C:\Users\rohit\OneDrive\Desktop\petavue_assignment"
    dest_dir = r"D:\coding_assignment\data"

    # Unzip files
    unzip_files(raw_data_dir, dest_dir)

