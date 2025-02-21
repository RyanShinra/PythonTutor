def calculate_class_stats(grades_list: list[int]):
    """
    Calculate statistics for a class given a list of student grades.
    Returns: tuple of (class_average, number_of_passing_students, highest_grade)
    A grade of 65 or higher is considered passing.
    """
    if len(grades_list) == 0:
        return 0, 0, 0
    
    total: int = 0
    passing_count: int = 0
    highest: int = grades_list[0]
    
    for grade in grades_list:
        # If it's negative (?!)
        if grade < 0:
            grade = 0
            
        total += grade
        if grade >= 65:
            passing_count += 1  # Bug #1: not incrementing the counter
        
        if highest < grade:    # Bug #2: comparison is backwards from initial value
            highest = grade
    
    average = total/len(grades_list)
    
    return (average, passing_count, highest)


# Test the function
test_grades = [55, 95, 75, 65, 85, 45]
print("Class statistics:", calculate_class_stats(test_grades))

# Should print something close to:
# Class statistics: (70.0, 4, 95)
# But won't due to the bugs!