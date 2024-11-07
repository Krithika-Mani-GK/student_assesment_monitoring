"""
StudentID: F332804
Last Modified date: 22/01/2024
"""
# Import the Python modules 
import sqlite3
import pandas as pd

def read_csv_files():
    """
    Reads CSV files containing formative and sum test data.

    Returns:
    Tuple of DataFrames: Contains formative and sum test DataFrames.
    """
    test_results_path = "./TestResult"
    formative_mock_test_df = pd.read_csv(
        f"{test_results_path}/Formative_Mock_Test.csv", index_col=None)
    formative_test_1_df = pd.read_csv(
        f"{test_results_path}/Formative_Test_1.csv", index_col=None)
    formative_test_2_df = pd.read_csv(
        f"{test_results_path}/Formative_Test_2.csv", index_col=None)
    formative_test_3_df = pd.read_csv(
        f"{test_results_path}/Formative_Test_3.csv", index_col=None)
    formative_test_4_df = pd.read_csv(
        f"{test_results_path}/Formative_Test_4.csv", index_col=None)
    stud_rate_df = pd.read_csv(
        f"{test_results_path}/StudentRate.csv", index_col=None)
    sum_test_df = pd.read_csv(
        f"{test_results_path}/SumTest.csv", index_col=None)
    
    return (
    formative_mock_test_df,
    formative_test_1_df,
    formative_test_2_df,
    formative_test_3_df,
    formative_test_4_df,
    stud_rate_df,
    sum_test_df)

def fetch_data_from_table(table_name, conn):
    """
    Fetches data from a specified table in the database.

    Args:
    table_name (str): Name of the table to fetch data from.
    conn (sqlite3.Connection): SQLite database connection.

    Returns:
    pd.DataFrame: DataFrame containing data from the specified table.
    """
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        return df
    # To catch the exception when the table passed doesnt exist in the db
    except pd.io.sql.DatabaseError:
        print(f"Table {table_name} does not exist in the database.")
        return pd.DataFrame()

def merge_tables():
    """
    Merges formative and sum test tables from the database.

    Returns:
    pd.DataFrame: Merged DataFrame containing formative and sum test data.
    """
    conn = sqlite3.connect("CWDatabase.db")

    # Fetch data from each table
    df_fmr = fetch_data_from_table('formative_mock_test_table', conn)
    df_f1r = fetch_data_from_table('formative_test1_table', conn)
    df_f2r = fetch_data_from_table('formative_test2_table', conn)
    df_f3r = fetch_data_from_table('formative_test3_table', conn)
    df_f4r = fetch_data_from_table('formative_test4_table', conn)
    df_str = fetch_data_from_table('sum_test_table', conn)

    # Close the connection
    conn.close()

    # Merge DataFrames using outer joins in a single line
    df = pd.merge(
         df_fmr, df_f1r, on='research_id', how='outer', suffixes=('', '_f1r'))\
        .merge(df_f2r, on='research_id', how='outer', suffixes=('', '_f2r')) \
        .merge(df_f3r, on='research_id', how='outer', suffixes=('', '_f3r')) \
        .merge(df_f4r, on='research_id', how='outer', suffixes=('', '_f4r')) \
        .merge(df_str, on='research_id', how='outer', suffixes=('', '_str'))

    # Drop duplicates based on the 'research_id' column
    df = df.drop_duplicates(subset='research_id')
    return df

def replace_null_values_with_zero(df):
    """
    Replaces null values in specified columns with zeros.

    Args:
    df (pd.DataFrame): DataFrame to replace null values.

    Returns:
    pd.DataFrame: DataFrame with null values replaced by zeros.
    """
    columns_to_replace = ['grade', 
                          'grade_f1r', 
                          'grade_f2r', 
                          'grade_f3r', 
                          'grade_f4r', 
                          'grade_str']
    
    # Replace null values 
    for column in columns_to_replace:
        df[column].fillna(0, inplace=True)
    return df

def load_to_db(df, table_name, conn, cursor):
    """
    Loads DataFrame into a specified table in the database.

    Args:
    df (pd.DataFrame): DataFrame to be loaded into the database.
    table_name (str): Name of the table to load data into.
    conn (sqlite3.Connection): SQLite database connection.
    cursor (sqlite3.Cursor): SQLite database cursor.

    Returns:
    pd.DataFrame: DataFrame that has been loaded into the database.
    """
    df.to_sql(table_name, conn, index=False, if_exists='replace')
    return df

