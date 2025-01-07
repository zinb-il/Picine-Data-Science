
import os
import sys
import psycopg2
import pandas as pd
from tqdm import tqdm
from time import sleep                                                                                                                                                                             
from dotenv import load_dotenv
sys.path.append('../ex02')
from table import get_files, create_tables


def main():
    try:
        path  = './customer/'
        files = get_files(path)
        create_tables(path, files)
    except Exception as err:
        print(f"Error exception {err}")




if __name__ == "__main__":
    main()
