	The code operates in a Conda environment, utilizing python libraries like sqlite3, Matplotlib, Numpy, Pandas, and ipywidgets. It strictly adheres to PEP 8 style guidelines, maintaining consistent variable naming, formatting, indentation, and line lengths below 79 characters. The snake_case convention is consistently followed for variables and functions. Assert test functionality is implemented across all five main code components, ensuring rigorous testing for accuracy and reliability to enhance the system's stability. Executing '%run {pgm}.py' independently triggers the main function with default values as the initial test case. A secondary test case, involving assert tests, is subsequently executed. The terms student_id and research_id are used interchangeably.

TestResult folder: 
	The folder contains the source csv files which are consumed by the other programs.

menu.ipynb:
	 The interface offers a slider for student IDs (1-156) and flags IDs 84, 94, and 125 as possible departures. Choose any test from the drop down list. Clicking "Test Results" handles no data gracefully. "CWPreprocessing," active by default, cleans and stores data in "CWDatabase.db." Post-processing, the system activates remaining buttons, allowing smooth data processing in the Student Assessment Monitoring System.

DAFunction.py:
	The DAFunction.py module defines helper functions with a focus on reusability. It efficiently handles diverse scenarios, offering functions for reading CSV files, fetching data from SQLite tables, merging formative and sum test tables, replacing null values with zeros, and loading processed DataFrames into the database.

CWPreprocessing.py:
	The main function, main_CWPreprocess, reads CSV files, processes data, and loads it into SQLite tables. Test cases display sample records for verification. We ensure required libraries are installed, and the DAFunction.py module is accessible.

testResults.py:
	The 'test_result_plot' function displays test results and plots grades based on input DataFrame and research_id. 'test_case_verify_grades' compares the output for a specific research_id with an expected subset DataFrame. 'main_testResults' allows users to input a student_id, merge tables, replace null values, and display test results dynamically with each change in the program slider.

studentPerformance.py:
	The script has functions for calculating absolute values, mean values, and relative differences in a given test and research ID. The main function, main_studentPerformance, extracts inputs, calls these functions, and visualizes results using bar charts. A validation test, test_case_relative_validation, ensures accurate relative differences for a specified research ID across all questions and grades.

underperformingStudent.py:
	The code identifies underperforming students based on specific grade criteria and filters out largely inactive students. It checks conditions like mock test grade < 60, at least one formative test < 50, and sum test < 60. The main code showcases underperforming students and verifies them against expected research IDs for accuracy. The test success message is printed if all expected IDs are correctly identified.

HardworkingStudents.py:
	The code follows OOP principles with a class, HardworkingStudentAnalyzer. The class streamlines analysis and it identifies and removes largely inactive users based on NaN values in over three columns, indicating non-attendance. The code handles NaN values in the final DataFrame, ensuring accurate attendance representation. Well-crafted test cases demonstrate accurate student counts for 'Beginner' and 'Below beginner' program knowledge levels.

