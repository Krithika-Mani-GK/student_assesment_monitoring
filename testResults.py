"""
StudentID: F332804
Last Modified date: 22/01/2024
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from DAFunction import *

def test_result_plot(df, research_id):
    """
    Display test results and plot grades for a specific student.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the student data.
    - research_id (int): Research ID of the student.

    Returns:
    - pd.DataFrame: DataFrame containing grade names and values.
    """
    
    # Convert research_id to int for comparison
    student_data = df[df['research_id'] == int(research_id)] 

    # Check if the research_id exists
    if not student_data.empty:
    # Extract grade names and values
        grade_names = ['grade', 
        'grade_f1r', 
        'grade_f2r', 
        'grade_f3r', 
        'grade_f4r', 
        'grade_str']
        grade_values = student_data.iloc[0][grade_names].tolist()
        
        # Round off the grade values to two decimal places
        grade_values = [round(value, 2) for value in grade_values]

        # Convert the list of grade values to a DataFrame for display
        all_elements_df = pd.DataFrame({'Grade Names': grade_names, 
        'Grade Values': grade_values})
        
        # Use display to show the DataFrame
        print(f"TestResults for student_id: {research_id}")
        display(all_elements_df.style.hide())
        
        # Plot the grades
        plt.bar(grade_names, grade_values, color='green')
        plt.xlabel('Grade Names')
        plt.xticks(rotation='vertical')  
        plt.ylabel('Grade Values')
        plt.title(f'Grades for Student ID {research_id}')
        
        # Set y-axis ticks with a gap of 10
        plt.yticks(range(0, int(max(grade_values)) + 10, 10))  
        plt.show()
        return all_elements_df
    else:
        print(f"No data found for Research ID {research_id}")
    
def test_case_verify_grades():
    """
    Test case to verify the correctness of the test_result_plot function.

    This test case compares the output of the test_result_plot function
    for a specific research_id with the expected subset DataFrame.

    Returns:
    None
    """
    # Create a DataFrame with data for research_id 50
    expected_subset = pd.DataFrame({
        'research_id': [50],
        'grade': [85.5],
        'grade_f1r': [90.0],
        'grade_f2r': [80.0],
        'grade_f3r': [75.0],
        'grade_f4r': [100.0],
        'grade_str': [56.0]
    })

    merged_data = merge_tables()
    cleansed_df = replace_null_values_with_zero(merged_data)
    
    # Get the DataFrame from the test_result_plot function
    all_elements_df = test_result_plot(cleansed_df, 50)
    
    # Create a DataFrame with the desired structure
    formatted_df = pd.DataFrame({
        'research_id': [50],
        'grade': [all_elements_df.loc[0, 'Grade Values']],
        'grade_f1r': [all_elements_df.loc[1, 'Grade Values']],
        'grade_f2r': [all_elements_df.loc[2, 'Grade Values']],
        'grade_f3r': [all_elements_df.loc[3, 'Grade Values']],
        'grade_f4r': [all_elements_df.loc[4, 'Grade Values']],
        'grade_str': [all_elements_df.loc[5, 'Grade Values']]
    })

    # Print the formatted and expected DataFrames
    print("Formatted DataFrame:")
    print(formatted_df)
    print("\nExpected Subset DataFrame:")
    print(expected_subset)
    
    # Assert without considering the index and data type
    assert formatted_df.reset_index(drop=True).equals(expected_subset), \
    "Test case failed: Output doesn't match expected values"
    print("\n Test results match & test case executed successfully")

def main_testResults(student_id):
    """
    Main function to test and display results for a specific student.

    This function takes a student_id as input, merges tables, 
    replaces null values, and calls the test_result_plot function to display 
    and plot the test results.

    Parameters:
    - student_id (int): The research_id of the student.

    Returns:
    None
    """
    # Take user input for research_id
    research_id_input = student_id

    # Call the main function to merge tables, replace null values
    df = merge_tables()
    cleansed_df = replace_null_values_with_zero(df)
    
    # Call the function to plot grades for the specified research_id
    all_elements_df = test_result_plot(cleansed_df,research_id_input)

if __name__ == "__main__":
    """
    Test the functionality of the main_testResults function and 
    test_case_verify_grades function when the script is run.
    """
    # Test Functionality
    main_testResults(17)
    test_case_verify_grades()


# In[ ]:




