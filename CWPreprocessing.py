"""
StudentID: F332804
Last Modified date: 22/01/2024
"""

# Import Python libraries and modules

import sqlite3
import pandas as pd
import numpy as np

from DAFunction import *

def rename_columns(df, new_cols):
    """
    Renames columns in the DataFrame based on the provided mapping.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.
    - new_cols (dict): Dictionary mapping old column names to new names.

    Returns:
    pd.DataFrame: DataFrame with renamed columns.
    """
    return df.rename(columns=new_cols).copy()

def replace_null_values(df):
    """
    Replaces null values, NaNs, and dashes with zero in the DataFrame.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with null values replaced.
    """
    df.replace(to_replace=pd.NA, value=0, inplace=True)
    df = df.replace([np.nan, None, '-'], 0)
    return df

def retain_highest_score(df):
    """
    Retains the rows with the highest grade for each research ID.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with only the rows having the highest grade 
    for each research ID.
    """
    df['grade'] = df['grade'].replace('-', '0').astype(float)
    df = df.sort_values(by=['research_id', 'grade'], ascending=[True, False])
    return df.groupby('research_id').head(1)

def drop_columns(df, columns):
    """
    Drops specified columns from the DataFrame.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.
    - columns (list): List of column names to be dropped.

    Returns:
    pd.DataFrame: DataFrame with specified columns removed.
    """
    return df.drop(columns, axis=1)

def adjust_scale(df, column_factors):
    """
    Adjusts the scale of selected columns in the DataFrame 
    by multiplying with specified factors.

    Parameters:
    - df (pd.DataFrame): Input DataFrame.
    - column_factors (dict): Dictionary mapping column names 
    to scaling factors

    Returns:
    pd.DataFrame: DataFrame with selected columns scaled according 
    to the specified factors.
    """
    for column, factor in column_factors.items():
        # Convert selected column to numeric type
        df[column] = pd.to_numeric(df[column], errors='coerce')

        # Multiply the column by the specified factor
        df[column] = (df[column] * factor).round(2)

    return df

def test_display_top_records(conn, table_name):
    """
    Fetches data from a specified table, displays the top 5 records, 
    and hides the underlying data.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - table_name (str): Name of the table to fetch data from.

    Returns:
    None
    """
    df = fetch_data_from_table(table_name,conn)
    print(f"\nDisplaying top 5 records from {table_name}:\n")
    # Hides the underlying data when displaying the top 5 records
    df_hidden = df.head(5).style.hide()
    display(df_hidden)

def main_CWPreprocess():
    """
    Main function for data preprocessing of formative mock tests, 
    formative tests 1-4, student ratings, and sum test.

    Returns:
    None
    """
    
    # Ensuring the program retains the original df 
    formative_mock_test_df, formative_test1_df, formative_test2_df, \
    formative_test3_df, formative_test4_df, stud_rate_df, \
    sum_test_df = read_csv_files()
    
    # Data Cleansing: Processing the data
  
    form_mock_prcsd_df = rename_columns(formative_mock_test_df, {
        'research id': 'research_id', 'State': 'state',
        'Started on': 'started_on', 'Completed': 'completed',
        'Time taken': 'time_taken', 'Grade/10000': 'grade', 'Q 1 /500': 'Q1',
        'Q 2 /300': 'Q2','Q 3 /600': 'Q3', 'Q 4 /700': 'Q4', 'Q 5 /500': 'Q5',
        'Q 6 /400': 'Q6', 'Q 7 /1000': 'Q7','Q 8 /2000': 'Q8', 
        'Q 9 /2000': 'Q9', 'Q 10 /2000': 'Q10'})
    
    form_test1_prcsd_df = rename_columns(formative_test1_df, {
        'research id': 'research_id', 'State': 'state',
        'Started on': 'started_on', 'Completed': 'completed',
        'Time taken': 'time_taken', 'Grade/600': 'grade',
        'Q 1 /100': 'Q1', 'Q 2 /100': 'Q2', 'Q 3 /100': 'Q3',
        'Q 4 /100': 'Q4', 'Q 5 /100': 'Q5', 'Q 6 /100': 'Q6'})
           
    form_test2_prcsd_df = rename_columns(formative_test2_df, {
        'research id': 'research_id', 'State': 'state',
        'Started on': 'started_on', 'Completed': 'completed',
        'Time taken': 'time_taken', 'Grade/700': 'grade',
        'Q 1 /100': 'Q1', 'Q 2 /100': 'Q2', 'Q 3 /100': 'Q3',
        'Q 4 /200': 'Q4', 'Q 5 /100': 'Q5', 'Q 6 /100': 'Q6'})
        
    form_test3_prcsd_df = rename_columns(formative_test3_df, {
        'research id': 'research_id', 'State': 'state',
        'Started on': 'started_on', 'Completed': 'completed',
        'Time taken': 'time_taken', 'Grade/600': 'grade',
        'Q 1 /100': 'Q1', 'Q 2 /100': 'Q2', 'Q 3 /100': 'Q3',
        'Q 4 /100': 'Q4', 'Q 5 /100': 'Q5', 'Q 6 /100': 'Q6'})
        
    form_test4_prcsd_df = rename_columns(formative_test4_df, {
        'research id': 'research_id', 'State': 'state',
        'Started on': 'started_on', 'Completed': 'completed',
        'Time taken': 'time_taken', 'Grade/1000': 'grade',
        'Q 1 /500': 'Q1', 'Q 2 /500': 'Q2'})
        
    stud_rate_prcsd_df = rename_columns(stud_rate_df, {
        'research id': 'research_id',
        'Which of followings are true for you': 'personal_status',
        'Which of the followings have you studied or had experience with':
        'study_experience',
        'What level programming knowledge do you have?':
         'prog_knowledge_level',
         'Do you like programming': 'like_prog',
         'What do you think about sci-fi movies ?': 'sci_fi_opinion',
         'What do you think about learning to program  ?':'learn_prog_opinion',
         'Can you please specify the programming language you know which a':
         'known_prog_languages'})
        
    sum_test_prcsd_df = rename_columns(sum_test_df, {
        'research id': 'research_id', 'State': 'state',
        'Started on': 'started_on', 'Completed': 'completed',
        'Time taken': 'time_taken', 'Grade/10000': 'grade',
        'Q 1 /500': 'Q1', 'Q 2 /300': 'Q2', 'Q 3 /600': 'Q3',
        'Q 4 /700': 'Q4', 'Q 5 /400': 'Q5', 'Q 6 /500': 'Q6',
        'Q 7 /1500': 'Q7', 'Q 8 /1500': 'Q8', 'Q 9 /1500': 'Q9',
        'Q 10 /1000': 'Q10', 'Q 11 /400': 'Q11', 'Q 12 /500': 'Q12',
        'Q 13 /600': 'Q13'})

    # Handling null values
    form_mock_prcsd_df = replace_null_values(form_mock_prcsd_df)
    form_test1_prcsd_df = replace_null_values(form_test1_prcsd_df)
    form_test2_prcsd_df = replace_null_values(form_test2_prcsd_df)
    form_test3_prcsd_df = replace_null_values(form_test3_prcsd_df)
    form_test4_prcsd_df = replace_null_values(form_test4_prcsd_df)
    stud_rate_prcsd_df = replace_null_values(stud_rate_prcsd_df)
    sum_test_prcsd_df = replace_null_values(sum_test_prcsd_df)

    # Retaining highest score for each student
    form_mock_prcsd_df = retain_highest_score(form_mock_prcsd_df)
    form_test1_prcsd_df = retain_highest_score(form_test1_prcsd_df)
    form_test2_prcsd_df = retain_highest_score(form_test2_prcsd_df)
    form_test3_prcsd_df = retain_highest_score(form_test3_prcsd_df)
    form_test4_prcsd_df = retain_highest_score(form_test4_prcsd_df)
    sum_test_prcsd_df = retain_highest_score(sum_test_prcsd_df)

    # Dropping unnecessary columns
    columns_to_drop = ['state', 'time_taken']
    form_mock_prcsd_df = drop_columns(form_mock_prcsd_df, columns_to_drop)
    form_test1_prcsd_df = drop_columns(form_test1_prcsd_df, columns_to_drop)
    form_test2_prcsd_df = drop_columns(form_test2_prcsd_df, columns_to_drop)
    form_test3_prcsd_df = drop_columns(form_test3_prcsd_df, columns_to_drop)
    form_test4_prcsd_df = drop_columns(form_test4_prcsd_df, columns_to_drop)
    sum_test_prcsd_df = drop_columns(sum_test_prcsd_df, columns_to_drop)

    # Scaling grade to 100 and questions as per grade factor for mock test 
    num_cols_mock = {'Q1': 1, 'Q2': 1, 'Q3': 1, 'Q4': 1, 'Q5': 1, 'Q6': 1, 
    'Q7': 1, 'Q8': 1, 'Q9': 1, 'Q10': 1, 'grade': 1}
    form_mock_prcsd_df = adjust_scale(form_mock_prcsd_df, num_cols_mock)

    # Scaling grade to 100 and questions as per grade factor for formativeTest1
    num_cols_test1 = {'Q1': 100/6, 'Q2': 100/6, 'Q3': 100/6,'Q4': 100/6, 
    'Q5': 100/6, 'Q6': 100/6,'grade': 100/6}
    form_test1_prcsd_df = adjust_scale(form_test1_prcsd_df, num_cols_test1)

    # Scaling grade to 100 and questions as per grade factor for formativeTest2
    num_cols_test2 = {'Q1': 100/7, 'Q2': 100/7, 'Q3': 100/7,'Q4': 100/7, 
    'Q5': 100/7, 'Q6': 100/7,'grade': 100/7}
    form_test2_prcsd_df = adjust_scale(form_test2_prcsd_df, num_cols_test2)

    # Scaling grade to 100 and questions as per grade factor for formativeTest3
    num_cols_test3 = {'Q1': 100/6, 'Q2': 100/6, 'Q3': 100/6,'Q4': 100/6, 
    'Q5': 100/6, 'Q6': 100/6,'grade': 100/6}
    form_test3_prcsd_df = adjust_scale(form_test3_prcsd_df, num_cols_test3)

    # Scaling grade to 100 and questions as per grade factor for formativeTest4
    num_cols_test4 = {'Q1': 10, 'Q2': 10, 'grade': 10}
    form_test4_prcsd_df = adjust_scale(form_test4_prcsd_df, num_cols_test4)
        
    # Scaling grade to 100 and questions as per grade factor for sumTest
    num_cols_sumtest = {'Q1': 1, 'Q2': 1, 'Q3': 1,'Q4': 1, 'Q5': 1, 
    'Q6': 1,'Q7': 1, 'Q8': 1, 'Q9': 1,
    'Q10': 1, 'Q11': 1, 'Q12': 1,'Q13': 1, 'grade': 1}
    sum_test_prcsd_df = adjust_scale(sum_test_prcsd_df, num_cols_sumtest)

    # Connecting to SQLite database
    conn = sqlite3.connect('CWDatabase.db')
    cursor = conn.cursor()

    # Loading cleansed data into database tables
    load_to_db(form_mock_prcsd_df, 'formative_mock_test_table', conn, cursor)
    load_to_db(form_test1_prcsd_df, 'formative_test1_table', conn, cursor)
    load_to_db(form_test2_prcsd_df, 'formative_test2_table', conn, cursor)
    load_to_db(form_test3_prcsd_df, 'formative_test3_table', conn, cursor)
    load_to_db(form_test4_prcsd_df, 'formative_test4_table', conn, cursor)
    load_to_db(stud_rate_prcsd_df, 'stud_rate_table', conn, cursor)
    load_to_db(sum_test_prcsd_df, 'sum_test_table', conn, cursor)
    conn.close()

if __name__ == "__main__":
    """
    Main entry point for the data preprocessing script.

    This function connects to the SQLite database, performs data preprocessing
    using the main_CWPreprocess function,
    and then displays sample records for each processed table using 
    the test_display_top_records function.

    Returns:
    None
    """
    conn = sqlite3.connect('CWDatabase.db')
    main_CWPreprocess()

    # Test Case Functionality
    print("Test case result display: Sample records below")
    for table in ['formative_mock_test_table', 'formative_test1_table', 
    'formative_test2_table', 'formative_test3_table', 'formative_test4_table', 
    'stud_rate_table', 'sum_test_table']:
        test_display_top_records(conn, table)


# In[ ]:




