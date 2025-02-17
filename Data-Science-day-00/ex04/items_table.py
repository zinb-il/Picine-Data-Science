import os
import sys
import psycopg2
import pandas as pd
from tqdm import tqdm
from time import sleep
from dotenv import load_dotenv

sys.path.append('../ex02')
from table import get_files, get_pd_object


def get_create_query(cols: list, table_name: str) -> str | None:
    """This function use to create your query string

    Args:
        cols (list): list of columns
        table_name (str): the table name

    Returns:
        str: query
    """
    if not cols or not table_name:
        return None
    return f"""DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
        "{cols[0]}" INTEGER,
        "{cols[1]}" NUMERIC,
        "{cols[2]}" TEXT,
        "{cols[3]}" VARCHAR(255)
    );"""


def insert_values(pf: pd.DataFrame, table_name: str,
                  cursor: psycopg2.extensions.cursor) -> None:
    """this function insert values inside a csv file into a table

    Args:
        pf (pd.DataFrame): panads data frame
        table_name (str): the table name
        cursor (psycopg2.extensions.cursor): cursor object

    Returns:
        str: query
    """
    columns = ", ".join([f'"{col}"' for col in pf.columns])
    for index, row in tqdm(pf.iterrows(), total=pf.shape[0]):
        cursor.execute(f"INSERT INTO {table_name} ({columns}) \
            VALUES (%s, %s, %s, %s);", (row.iloc[0],
                                        row.iloc[1],
                                        row.iloc[2],
                                        row.iloc[3]))
        sleep(0.01)


def create_tables(__dir: str = "./", files: list | None = None) -> None:
    """This function create table in a pewostgress databse bas on csv file

    Args:
        files (list): list of files to turn as table in postgres database
    """
    if not files and not len(files):
        return
    try:
        dotenv_path = '../ex00/src/.env'
        load_dotenv(dotenv_path)
        conn = psycopg2.connect(
            host="localhost",
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        cursor = conn.cursor()
        for file in files:
            table_name = file.split('.')[0]
            pf = get_pd_object(__dir + file)
            query = get_create_query(list(pf.columns), table_name)
            if query:
                cursor.execute(query)
                print(f"Votre requête d'insertion dan la table {table_name} \
est en cours de traitement")
                insert_values(pf, table_name, cursor)
                conn.commit()
    except Exception as err:
        print(f"Error exception {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def main():
    try:
        path = './item/'
        files = get_files(path)
        create_tables(path, files)
    except Exception as err:
        print(f"Error exception {err}")


if __name__ == "__main__":
    main()
