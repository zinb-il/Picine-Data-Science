
import os
import psycopg2                                                                                                                                                                                  
import pandas as pd
from dotenv import load_dotenv


def get_pd_object(__file: str)-> pd.DataFrame:
    """This function is for open a csv file with pandas

    Args:
        file (str): the path of the file

    Returns:
        pd.Object: pandas object
    """
    df = pd.read_csv(__file)
    return df


def get_files(__dir: str = "./", __ext: str = "csv")->list:
    """this function is for getting all files with a specific extension in a directory

    Args:
        __ext (str): extention of the file
        __dir (str, optional): path of the directory. Defaults to "."

    Returns:
        list: list of the names of the files
    """
    files = []
    for file in os.listdir(__dir):
        if file.endswith(".csv"):
            files.append(file)
    return files


def get_create_query(cols: list, table_name: str)-> str:
    """This function use to create your query string

    Args:
        cols (list): list of columns
        table_name (str): the table name

    Returns:
        str: query
    """
    return  f"""DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
        "{cols[0]}" TIMESTAMP,
        "{cols[1]}" VARCHAR(255),
        "{cols[2]}" INTEGER,
        "{cols[3]}" DECIMAL(10,2),
        "{cols[4]}" BIGINT,
        "{cols[5]}" TEXT
    );"""

def insert_values(pf: pd.DataFrame, table_name: str, cursor: psycopg2.extensions.cursor)-> None:
    """this function insert values inside a csv file into a table

    Args:
        pf (pd.DataFrame): panads data frame
        table_name (str): the table name
        cursor (psycopg2.extensions.cursor): cursor object

    Returns:
        str: query
    """
    for index, row in pf.iterrows():
        columns = ", ".join([f'"{col}"' for col in pf.columns])
        for index, row in pf.iterrows():
            values = ", ".join([f"'{val}'" for val in row])
            cursor.execute (f"INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s, %s, %s);", 
                (row[0], row[1], row[2], row[3], row[4], row[5]))


def create_tables(__dir: str = "./",files: list | None = None)-> None:
    """This function create table in a postgress databse bas on csv file

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
        for file in  files:
            table_name = file.split('.')[0]
            pf = get_pd_object(__dir + file)
            query = get_create_query(list(pf.columns), table_name)
            cursor.execute(query)
            insert_values(pf,table_name, cursor)
            conn.commit()
    except Exception as err:
        print(f"Error exception {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def main():
    try:
        path  = './customer/'
        files = get_files(path)
        create_tables(path, files)
    except Exception as err:
        print(f"Error exception {err}")




if __name__ == "__main__":
    main()