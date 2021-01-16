import os
import kaggle


def grab_baseball_databank():
    os.environ['KAGGLE_USERNAME'] = 'kotarohyama'
    os.environ['KAGGLE_KEY'] = 'bf094dfef5ceb846801b8ed0baebc9f7'

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files('open-source-sports/baseball-databank', path='data', unzip=True)

    print("Data retrieved from open-source-sports/baseball-databank on Kaggle.")


if __name__ == '__main__':
    grab_baseball_databank()
