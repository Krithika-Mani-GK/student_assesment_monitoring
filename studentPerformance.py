"""
StudentID: F332804
Last Modified date: 22/01/2024
"""
# Import python modules
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# Import defined module DAFunction.py
from DAFunction import *

def calc_absolute_val(df, research_id, test_name):
    """
    Calculate absolute values for a specific test and research_id.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the student data.
    - research_id (int): Research ID of the student.
    - test_name (str): Name of the test for which 
    absolute values are calculated.

    Returns:
    - dict: Dictionary containing absolute values for each question 
    and the overall test grade.
    """
    
    # Mapping of test columns to corresponding grade columns
    column_mapping = {
        'mock': 'grade', 'Q1': None, 'Q2': None, 'Q3': None, 'Q4': None, 
        'Q5': None, 'Q6': None, 'Q7': None, 'Q8': None, 'Q9': None, 
        'Q10': None, 'test1': 'grade_f1r', 'Q1_f1r': None, 'Q2_f1r': None, 
        'Q3_f1r': None, 'Q4_f1r': None, 'Q5_f1r': None, 'Q6_f1r': None,
        'test2': 'grade_f2r', 'Q1_f2r': None, 'Q2_f2r': None, 'Q3_f2r': None,
        'Q4_f2r': None, 'Q5_f2r': None, 'Q6_f2r': None, 'test3':'grade_f3r', 
        'Q1_f3r': None, 'Q2_f3r': None, 'Q3_f3r': None, 'Q4_f3r': None, 
        'Q5_f3r': None, 'Q6_f3r': None, 'test4': 'grade_f4r', 'Q1_f4r': None, 
        'Q2_f4r': None, 'sumtest': 'grade_str', 'Q1_str': None, 'Q2_str': None,
        'Q3_str': None, 'Q4_str': None, 'Q5_str': None, 'Q6_str': None,
        'Q7_str': None, 'Q8_str': None, 'Q9_str': None, 'Q10_str': None
    }

    
    # Extract question columns based on the test_name
    question_columns = [f'Q{i}_{test_name}' for i in range(1, 14)]
    absolute_val = {}

    # Calculate absolute values for each question
    for col in question_columns:
        if col in df.columns:
            value = df[col].loc[df['research_id'] == int(research_id)].values
            
            if len(value) > 0 and value[0] not in ('', '-', np.nan):
                absolute_val[f'absolute_{col}'] = round(float(value[0]), 2)
            else:
                absolute_val[f'absolute_{col}'] = 0

    # Calculate absolute value for the overall test grade            
    grade_column = column_mapping[test_name]
    if test_name in column_mapping and grade_column in df.columns:
        grade_value = df[grade_column].loc[df['research_id'] 
                                           == int(research_id)].values
        
        # Calculate absolute grade value and round to two decimal places
        absolute_val[f'absolute_{test_name}_grade'] = round(float(\
            grade_value[0]), 2) \
        if len(grade_value) > 0 and not np.isnan(grade_value[0]) else 0
    else:
        print(f"Grade column {grade_column} not found in the dataframe.")

    return absolute_val

def calc_mean_val(df,test_name):
    """
    Calculate mean values of questions and grades for a specific test.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the student data.
    - test_name (str): Name of the test for which mean values are calculated.

    Returns:
    - dict: Dictionary containing mean values for each relevant column.
    """
    mean_values = {}

    if test_name:
        # Calculate mean values for the specified test
        filtered_columns = [col for col in df.columns if test_name in col]
        for col_name in filtered_columns:
            mean_values[f"mean_{col_name}"] = round(
                pd.to_numeric(df[col_name], errors='coerce').mean(), 2)
    else:
        # Calculate mean values for each question
        question_columns = [col for col in df.columns if col.startswith('Q')]

        for col_name in question_columns:
            mean_values[f"mean_{col_name}"] = round(
                df[col_name].astype(float).mean(), 2)
            
   # Map the grade column based on the test_name
    grade_col_mapping = {
        'mock': 'grade', 'test1': 'grade_f1r', 'test2': 'grade_f2r',
        'test3': 'grade_f3r', 'test4': 'grade_f4r', 'sumtest': 'grade_str'
    }

    grade_col = grade_col_mapping.get(test_name.lower(), None)
    if grade_col:
        mean_values[f"mean_{test_name}_grade"] = round(
            df[grade_col].astype(float).mean(), 2)
    else:
        print(f"Grade column mapping not found for test_name: {test_name}")

    # Calculate mean values of grades
    mean_values[f"mean_{test_name}_grade"] = round(
        df[grade_col].astype(float).mean(), 2)

    return mean_values

def calc_relative_diff(absolute_val, mean_values):
    """
    Calculate relative diff between absolute values and mean values.

    Parameters:
    - absolute_val (dict): Dictionary containing absolute values 
    for each question and test grade.
    - mean_values (dict): Dictionary containing mean values 
    for each relevant column.

    Returns:
    - dict: Dictionary containing relative diff 
    for each question and test grade.
    """
    relative_diff = {}

    # Calculate relative differences for questions
    for key, value in absolute_val.items():
        if key.startswith('absolute_') and not key.endswith('_grade'):
            test_name = key.replace('absolute_', '')
            mean_key = f"mean_{test_name}"

            if mean_key in mean_values:
                mean_value = mean_values[mean_key]
                relative_diff_key = f"relative_{test_name}"
                relative_diff[relative_diff_key] = round(value - mean_value, 2)

    # Explicitly calculate relative differences for grades
    for test_name in ['mock', 'test1', 'test2', 'test3', 'test4', 'sumtest']:
        absolute_key = f'absolute_{test_name}_grade'
        mean_key = f'mean_{test_name}_grade'
        relative_diff_key = f'relative_{test_name}_grade'

        if absolute_key in absolute_val and mean_key in mean_values:
            absolute_value = absolute_val[absolute_key]
            mean_value = mean_values[mean_key]
            relative_diff[relative_diff_key] = round(
                absolute_value - mean_value, 2)

    return relative_diff

def test_case_relative_validation():
    """
    Test case to validate the relative diff 
    for a specific research_id (44) and test (test4).

    This test case involves merging tables, replacing null values, 
    and calculating absolute and mean values.
    Then compares the calculated relative diff with the expected subset.

    Returns:
    None
    """
    expected_subset = {
        'relative_Q1_test4': 10.92,
        'relative_Q2_test4': 11.05,
        'relative_test4_grade': 21.96
    }

    print("Test Case for Research ID 44:")
    merged_data = merge_tables()
    plot_df = replace_null_values_with_zero(merged_data)
    column_mappings = {'Q1_f4r': 'Q1_test4', 'Q2_f4r': 'Q2_test4'}

    # Get the DataFrame from the test_result_plot function
    plot_df = plot_df.rename(columns=column_mappings)
    plot_df = plot_df.replace([np.nan, None, '-'], 0)

    # Test with a default value of 44 & test4
    absolute_val = calc_absolute_val(plot_df, '44', 'test4')

    if absolute_val:
        print(f"\nAbsolute Values for Test4 (Research ID: 44):")
        for key, value in absolute_val.items():
            print(f"{key}: {value}")

    # Calculate mean values
    mean_values = calc_mean_val(plot_df, 'test4')
    print("\nMean values are:")
    print(pd.Series(mean_values))

    # Calculate relative diff between absolute value and mean value
    relative_diff = calc_relative_diff(absolute_val, mean_values)
    print("\nRelative performance values are:")
    print(pd.Series(relative_diff))

    print(relative_diff)
    print(expected_subset)

    # Assert without considering the index and data type
    assert relative_diff == expected_subset, "Test case failed: \
    Output doesn't match expected values"
    print("\nTest Results match & Test case execution successful")

def main_studentPerformance(student_id, selected_test_name):
    """
    Main function to analyze and visualize 
    student performance for a specific test.

    Parameters:
    - student_id (str): Research ID of the student.
    - selected_test_name (str): Name of the selected test (mock, test1, test2, 
    test3, test4, sumtest).

    Returns:
    None
    """
    # Extraction of input values
    research_id = student_id
    test_name = selected_test_name

    # Utilizing the Functions from DAFunction.py
    merged_df = merge_tables() 
    plot_df = replace_null_values_with_zero(merged_df) 
    
    # Check if student_id is present in the DataFrame
    if research_id not in plot_df['research_id'].values:
        print(f"No data for student_id {research_id}")

    else:
        # Rename columns
        column_mappings = {
            'Q1': 'Q1_mock', 'Q2': 'Q2_mock', 'Q3': 'Q3_mock', 'Q4': 'Q4_mock', 
            'Q5': 'Q5_mock', 'Q6': 'Q6_mock','Q7': 'Q7_mock', 'Q8': 'Q8_mock', 
            'Q9': 'Q9_mock', 'Q10': 'Q10_mock','Q1_f1r': 'Q1_test1', 
            'Q2_f1r': 'Q2_test1', 'Q3_f1r': 'Q3_test1', 'Q4_f1r': 'Q4_test1',
            'Q5_f1r': 'Q5_test1', 'Q6_f1r': 'Q6_test1','Q1_f2r': 'Q1_test2', 
            'Q2_f2r': 'Q2_test2', 'Q3_f2r': 'Q3_test2', 'Q4_f2r': 'Q4_test2',
            'Q5_f2r': 'Q5_test2', 'Q6_f2r': 'Q6_test2','Q1_f3r': 'Q1_test3', 
            'Q2_f3r': 'Q2_test3', 'Q3_f3r': 'Q3_test3', 'Q4_f3r': 'Q4_test3',
            'Q5_f3r': 'Q5_test3', 'Q6_f3r': 'Q6_test3','Q1_f4r': 'Q1_test4', 
            'Q2_f4r': 'Q2_test4','Q1_str': 'Q1_sumtest', 'Q2_str': 'Q2_sumtest', 
            'Q3_str': 'Q3_sumtest', 'Q4_str': 'Q4_sumtest','Q5_str': 'Q5_sumtest',
            'Q6_str': 'Q6_sumtest', 'Q7_str': 'Q7_sumtest', 'Q8_str': 'Q8_sumtest',
            'Q9_str': 'Q9_sumtest', 'Q10_str': 'Q10_sumtest', 'Q11': 'Q11_sumtest',
            'Q12': 'Q12_sumtest', 'Q13': 'Q13_sumtest'
        }
        plot_df = plot_df.rename(columns=column_mappings)
        plot_df = plot_df.replace([np.nan, None, '-'], 0)

        # Call the absolute function to calculate absolute values 
        absolute_val = calc_absolute_val(plot_df, research_id, test_name)

        if absolute_val:
            print(f"\nAbsolute Values for {test_name.capitalize()} \
            (Research ID: {research_id}):")
            for key, value in absolute_val.items():
                print(f"{key}: {value}")

        # Call the mean function to calculate mean values
        mean_values = calc_mean_val(plot_df,test_name)
        print("\nMean values are:")
        print(pd.Series(mean_values))

        # Call the relative function to calculate relative values
        relative_diff=calc_relative_diff(absolute_val,mean_values)
        print("\nRelative performance values are:")
        print(pd.Series(relative_diff))

        # Plotting absolute values
        absolute_df = pd.DataFrame(absolute_val, index=[0])
        absolute_df.T.plot(kind='bar', legend=False, color='blue')
        plt.title(f'Absolute Values for {test_name.capitalize()} \
        (Research ID: {research_id})')
        plt.xlabel('Questions & Grade')
        plt.ylabel('Marks')
        plt.show()

        # Plotting relative diff
        relative_df = pd.DataFrame(relative_diff, index=[0])
        relative_df.T.plot(kind='bar', legend=False, color='green')
        plt.title(f'Relative diff for {test_name.capitalize()} \
        (Research ID: {research_id})')
        plt.xlabel('Questions & Grade')
        plt.ylabel('diff')
        plt.show()

if __name__ == "__main__":
    """
    Main block to execute when the script is run independently.

    This block calls the main_studentPerformance function with 
    specific parameters to analyze and visualize
    student performance for a mock test with a specified research ID. 
    Additionally, it runs the test_case_relative_validation function 
    to validate the relative diff for a specific research_id and test.

    Returns:
    None
    """
    main_studentPerformance(78, 'mock')
    test_case_relative_validation()
    


# In[ ]:




