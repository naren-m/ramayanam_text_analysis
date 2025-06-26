# coding: utf-8

import os

import pandas as pd
import sqlite3

root_dir = os.getcwd() + "/"
sloka_root = os.path.join(root_dir, "Slokas")
database = root_dir + "ramayanam.db"

# Ramayanam metadata
KandaList = []

KandaDetails = {'num': 1, 'name': "BalaKanda", 'sargas': 77}
KandaList.append(KandaDetails)
KandaDetails = {'num': 2, 'name': "AyodhyaKanda", 'sargas': 119}
KandaList.append(KandaDetails)
KandaDetails = {'num': 3, 'name': "AranyaKanda", 'sargas': 75}
KandaList.append(KandaDetails)
KandaDetails = {'num': 4, 'name': "KishkindaKanda", 'sargas': 67}
KandaList.append(KandaDetails)
KandaDetails = {'num': 5, 'name': "SundaraKanda", 'sargas': 68}
KandaList.append(KandaDetails)
KandaDetails = {'num': 6, 'name': "YuddhaKanda", 'sargas': 128}
KandaList.append(KandaDetails)

common_cols = ["kanda_id", "sarga_id", "sloka_id"]


# Collecting files from all kanda folders.
def collect_files_from(sloka_root):
    files = dict()

    for (dp, dn, fn) in os.walk(sloka_root):
        if dp != sloka_root:
            files[dp] = fn

    return files


def get_file_of_type(files_dict, file_type):
    files = list()
    for d, fs in files_dict.items():
        for f in fs:
            if file_type in f:
                files.append(os.path.join(d, f))

    return files


def categorize_all_files(files_dict):
    meaning_files = get_file_of_type(files_dict, "meaning")
    sloka_files = get_file_of_type(files_dict, "sloka")
    translation_files = get_file_of_type(files_dict, "translation")

    return meaning_files, sloka_files, translation_files


# Create Sqlite database
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None


# Generate dataframes from the file contents
def genrate_df_from_files(files, sep, columns, sort_by=None):
    main_df = pd.DataFrame()
    df_list = list()
    for m in files:
        df = pd.read_csv(m, sep=sep, names=columns, engine='python')
        df_list.append(df)

    main_df = pd.concat(df_list)

    if sort_by is not None:
        main_df = main_df.sort_values(sort_by)

    return main_df


def generate_all_dfs(meaning_files, sloka_files, translation_files):
    meaning_cols = common_cols + ["meaning"]
    meaning_df = genrate_df_from_files(meaning_files, sep='::',
                                       columns=meaning_cols,
                                       sort_by=common_cols)

    sloka_cols = common_cols + ["sloka"]
    sloka_df = genrate_df_from_files(sloka_files, sep='::',
                                     columns=sloka_cols,
                                     sort_by=common_cols)

    translation_cols = common_cols + ["translation"]
    translation_df = genrate_df_from_files(translation_files, sep='::',
                                           columns=translation_cols,
                                           sort_by=common_cols)

    return meaning_df, sloka_df, translation_df


def verify_sloka_count(conn, req_sloka_count=0):
    cur = conn.cursor()
    cur.execute("SELECT count(*) FROM slokas")

    rows = cur.fetchall()
    sloka_count = rows[0][0]

    if sloka_count != req_sloka_count:
        print("Something went wrong. Expected",
              req_sloka_count, "got", sloka_count)
    else:
        print("Completed.")


def main():
    files = collect_files_from(sloka_root)
    meaning_files, sloka_files, translation_files = categorize_all_files(files)
    print(database)

    meaning_df, sloka_df, translation_df = generate_all_dfs(
        meaning_files, sloka_files, translation_files)

    # Merging all three dataframes
    meaning_sloka_df = pd.merge_ordered(meaning_df, sloka_df, on=common_cols)
    slokas_df = pd.merge_ordered(
        meaning_sloka_df, translation_df, on=common_cols)

    if not len(slokas_df) == len(translation_df) == len(meaning_df) == len(sloka_df):
        print("Something went wrong")
    else:
        # Cleanup of dataframe that are note required now
        del meaning_sloka_df, meaning_df, sloka_df, translation_df

    # Save the slokas dataframe to sqlite db
    conn = create_connection(database)
    with conn:
        # save dataframe to database
        slokas_df.to_sql(name="slokas", con=conn)
        verify_sloka_count(conn, 18422)

    # Delete the dataframe
    del slokas_df


if __name__ == '__main__':
    main()
