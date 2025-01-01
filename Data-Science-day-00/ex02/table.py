
import os
import pandas as pd

def get_pd_object(file: str)-> pd.DataFrame:
    """This function is for open a csv file with pandas

    Args:
        file (str): the path of the file

    Returns:
        pd.Object: pandas object
    """
    df = pd.read_csv(file)
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
    # for file in files[:1]:
    #     df = get_pd_object(__dir + file)
    #     print(f"{'=' * 20}")
    #     print(df.head(1))
    #     print(f"{'=' * 20}")
    return files

def get_query(cols: pd.Index, tabel_name: str)-> str:
    """This function use to create your query string

    Args:
        cols (pd.DataFrame): panads data frame
        table_name (str): the table name

    Returns:
        str: query
    """
    return 'test'



def create_tables(__dir: str = "./",files: list | None = None)-> None:
    """This function create table in a postgress databse bas on csv file

    Args:
        files (list): list of files to turn as table in postgres database
    """
    if not files :
        return
    for file in files[:1] :
        pf = get_pd_object(__dir + file)
        for i in pf.columns:
            print(i)


def main():
    try:
        path  = './customer/'
        files = get_files(path)
        print(files)
        create_tables(path, files)
    except(err):
        print(f"Error exception {err}")




if __name__ == "__main__":
    main()