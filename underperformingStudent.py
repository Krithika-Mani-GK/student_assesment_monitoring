"""
StudentID: F332804
Last Modified date: 22/01/2024
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from DAFunction import *

def underperforming_grades(df):
    """
    Filter the DataFrame to include only relevant columns 
    and rows with less than 3 NaN values.
    
    Args:
    df (pd.DataFrame): Input DataFrame.
    
    Returns:
    pd.DataFrame: Filtered DataFrame.
    """
    # Select the grade columns for the specific research_id
    grade_columns = ['research_id', 'grade', 'grade_f1r', 'grade_f2r', 
                     'grade_f3r', 'grade_f4r', 'grade_str']
    df = df[grade_columns]
    
    # Filter condition for atleast 3 columns with NaN values
    # To exclude largely inactive students
    mask = df.isnull().sum(axis=1) < 2
    df = df[mask]
    return df

def identify_underperforming_students(df):
    """
    Identify underperforming students based on specified criteria.
    
    Args:
    df (pd.DataFrame): Input DataFrame.
    
    Returns:
    pd.DataFrame: DataFrame containing underperforming students.
    """
    criteria_mask = (df['grade'] < 60) & (
    (df['grade_f1r'] < 50) | (df['grade_f2r'] < 50) |
    (df['grade_f3r'] < 50) | (df['grade_f4r'] < 50)
    ) & (df['grade_str'] < 60)
 

                                          
    underperforming_students = df[criteria_mask]
    return underperforming_students

def find_minimum_grades(df):
    """
    Find the minimum grades from each record.
    
    Args:
    df (pd.DataFrame): Input DataFrame.
    
    Returns:
    pd.Series: Series containing minimum grades.
    """
    
    # Convert the columns to numeric values
    df[['grade', 
        'grade_f1r', 
        'grade_f2r', 
        'grade_f3r', 
        'grade_f4r', 
        'grade_str']] = df[['grade', 'grade_f1r', 'grade_f2r',
                            'grade_f3r', 'grade_f4r', 'grade_str']].apply(
                                pd.to_numeric, errors='coerce')

    
    # Find the minimum grades from each record and return as a list
    min_grades = df[['grade', 'grade_f1r', 'grade_f2r', 
                     'grade_f3r', 'grade_f4r', 'grade_str']].min(
                        axis=1, skipna=True)
    
    return min_grades

def highlight_minimum_grades(row):
    """
    Apply styling to highlight the lowest mark in every record.
    
    Args:
    row (pd.Series): DataFrame row.
    
    Returns:
    List: List of CSS styles for each column in the row.
    """
    return ['background-color: blue' 
            if val == row['grade':'grade_str'].min() else '' for val in row]

def main_underperforming_students():
    """
    Main function to identify and display underperforming students.
    """
    merged_df = merge_tables()
    underperf_df = underperforming_grades(merged_df)
    
    # Identify underperforming students based on the predefined criteria
    underperforming_students = identify_underperforming_students(underperf_df)
    underperforming_students = underperforming_students.round(2).astype(str)
    
    # To get the minimum values for underperforming students
    min_grades = find_minimum_grades(underperforming_students)
    
    # Apply the style to highlight the lowest mark in every record
    styled_underperforming_students = underperforming_students.style.apply(
        highlight_minimum_grades, axis=1,
        subset=underperforming_students.columns[1:]).hide()
    display(styled_underperforming_students)

def test_underperforming_students():
    """
    Test function to check if valid 
    research_id values exist in the DataFrame.
    """
    merged_df = merge_tables()
    underperforming_students = identify_underperforming_students(merged_df)
    valid_research_ids = [34, 60, 65, 69, 90, 128, 138, 141]
    all_test_cases_passed = True
    
    # Validate the research_id and when not found, print a failure message
    for research_id in valid_research_ids:
        if research_id not in underperforming_students['research_id'].values:
            print(f"Test Case Failed: Research ID {research_id} "
            "not found in the DataFrame")
            all_test_cases_passed = False

    # Displays the result on the success of the test cases     
    if all_test_cases_passed:
        print("Test case execution is successful & Result matches perfectly")

if __name__ == "__main__":
    main_underperforming_students()
    test_underperforming_students()


# In[ ]:




