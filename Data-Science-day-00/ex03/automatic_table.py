import sys

sys.path.append('../ex02')
from table import get_files, create_tables


def main():
    try:
        path = './customer/'
        files = get_files(path)
        create_tables(path, files)
    except Exception as err:
        print(f"Error exception {err}")


if __name__ == "__main__":
    main()
