import requests 
from tqdm import tqdm

#download the file from the url
def download_file(url, filename, mode='wb',headers=None):
    try:
        with open(filename, mode) as f:
            if headers is not None:
                # breakpoint()
                response = requests.get(url, stream=True, headers=headers)
            else:
                response = requests.get(url, stream=True)
            for chunk in tqdm(response.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)
                f.flush()
        return True
    except Exception as e:
            print(e)
