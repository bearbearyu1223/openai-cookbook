import os
import wget
import zipfile
import pandas as pd 
import logging
from ast import literal_eval
from tqdm import tqdm
# from tqdm.auto import tqdm  # for notebooks

logging.basicConfig(level=logging.DEBUG)

cwd = os.getcwd()
sep = os.path.sep
download_path = cwd
data_path = os.path.join(cwd, "data")

def download_and_read_data(
        data_path: str, 
        download_path: str, 
        file_name: str = 'vector_database_wikipedia_articles_embedded', 
        data_url: str =  'https://cdn.openai.com/API/examples/data/vector_database_wikipedia_articles_embedded.zip'
)->pd.DataFrame:
    csv_file_path = os.path.join(data_path, file_name + '.csv')
    zip_file_path = os.path.join(download_path, file_name + '.zip')

    if os.path.isfile(csv_file_path):
        logging.info(f"File {csv_file_path} has been downloaded")
    else:
        if os.path.isfile(zip_file_path):
            logging.info("Zip downloaded but not unzipped, unzipping now...")
        else:
            logging.info("File not found, downloading now...")
            # Download the data
            wget.download(data_url, out=download_path)

        # Unzip the data
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(data_path)

        # Remove the zip file
        os.remove(zip_file_path)
        logging.info(f"File downloaded to {data_path}")

    str2list = lambda x: [float(x) for x in list(x[1:-1].split(', '))]
    tqdm.pandas()
    data = pd.read_csv(csv_file_path)
    data['id'] = data['id'].astype(str)
    data['vector_id'] = data['vector_id'].astype(str)
    data['title_vector'] = data.title_vector.progress_apply(str2list)
    data['content_vector'] = data.content_vector.progress_apply(str2list)
    
    
    return data
        

if __name__ == '__main__': 
    data = download_and_read_data(data_path=data_path, download_path=download_path)
    # print(data.head())
    print(data.dtypes)
    print(type(data['title_vector'][0][0]))
    print(type(data['content_vector'][0][0]))
