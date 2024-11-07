"""
StudentID: F332804
Last Modified date: 22/01/2024
"""

# Import Python libraries and modules

import sqlite3
import pandas as pd

from DAFunction import *

class HardworkingStudentAnalyzer:
    """
    An analyzer for identifying hardworking students based 
    on specified criteria.
    """
    def __init__(self, db_path):
        """
        Initializes a HardworkingStudentAnalyzer object.

        Parameters:
        - db_path (str): The path to the SQLite database.
        """
        self.conn = sqlite3.connect(db_path)

    def generate_hardworking_students(self, df_results, df_rate_table):
        """
        Generates a DataFrame of hardworking students based on criteria.

        Criteria:
        - Grade greater than or equal to 60
        - Program knowledge level is 'Below beginner' or 'Beginner'

        Parameters:
        - results_df (pd.DataFrame): DataFrame containing student results.
        - rate_table_df (pd.DataFrame): DataFrame containing 
        student rate information.

        Returns:
        pd.DataFrame: DataFrame of hardworking students.
        """
        
        # Merge the result and rate tables 
        merged_df = pd.merge(df_results, df_rate_table, on='research_id')

        # Filter hardworking students based on criteria
        hardworking_students = merged_df[
            (merged_df['grade_str'] >= 60) &
            (merged_df['prog_knowledge_level'].isin(
                ['Below beginner', 'Beginner']))
        ].round(2)
        
        # Sort the DataFrame by grade in descending order
        hardworking_students = hardworking_students.sort_values(
            by='grade_str', ascending=False)
        
        hardworking_students= hardworking_students.astype(str)
        # Select and return relevant columns
        return hardworking_students[['research_id', 
        'grade_str', 'prog_knowledge_level']]

    def test_prog_knowledge_level_counts(self):
        """
        Tests the counts of hardworking students at 'Beginner' 
        and 'Below beginner' prog knowledge levels.
        Prints success message if the counts match the expected values.
        """
        result = self.generate_hardworking_students(df_results,df_rate_table)
        
        # Count students at 'Beginner' and 'Below beginner' prog levels
        beginner_count = result[
            result['prog_knowledge_level'] == 'Beginner'].shape[0]

        below_beginner_count = result[
            result['prog_knowledge_level'] == 'Below beginner'].shape[0]
        
        # Assert counts match expected values
        assert beginner_count == 33, "TC Failed: Incorrect count"
        assert below_beginner_count == 8, "TC Failed: Incorrect count"
        print("The beginner level hardworking student count is 33, \
        and below beginner level hardworking student count is 8. \
        \nTest case for counting prog_knowledge_level is successful")

if __name__ == "__main__":
    
    """
    Main block for standalone script execution.

    - Connects to the 'CWDatabase.db' database.
    - Merges tables and fetches data.
    - Creates an instance of HardworkingStudentAnalyzer.
    - Generates and displays hardworking students using the analyzer.
    - Executes a test case to validate the count of prog knowledge levels.
    """
    
    # Connect to the database
    conn = sqlite3.connect("CWDatabase.db")
    
    # Merge tables and fetch data
    stud_tbl_df = merge_tables()
    df_rate_table = fetch_data_from_table('stud_rate_table',conn)
    df_results = replace_null_values_with_zero(stud_tbl_df)
    
    # Creation of HardworkingStudentAnalyzer instance
    analyzer = HardworkingStudentAnalyzer('CWDatabase.db')
    hardworking_students_df = analyzer.generate_hardworking_students(
        df_results,df_rate_table)
    display(hardworking_students_df.style.hide())
    
    # Test case execution to validate prog knowledge level count
    analyzer.test_prog_knowledge_level_counts()


# In[ ]:




