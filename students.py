class Student:
    grade_values = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    
    def __init__(self, name: str, student_id: str):
        Student._validate_input(name, 'name', str)
        Student._validate_input(student_id, 'student_id', str)
            
        self.name = name
        self.id = student_id
        self.course_grades: dict[str, str] = {}  # course_code -> (grade, credits)
        self.course_credits: dict[str, int] = {}
        
    def enroll(self, course_code: str, credits: int):
        Student._validate_input(course_code, 'course_code', str)
        Student._validate_input(credits, 'credits', int)
        
        if credits <= 0:
            raise ValueError('Credits is non-positive integer.')
        
        if course_code in self.course_grades.keys():
            return False  # Already enrolled
        
        self.course_grades[course_code] = None
        self.course_credits[course_code] = credits
        return True
        
    def assign_grade(self, course_code: str, grade: str):
        Student._validate_input(course_code, 'course_code', str)
        Student._validate_input(grade, 'grade', str)

        if course_code not in self.course_grades.keys():
            return False # Doesn't attend this class
        
        grade = grade.upper()
        
        if grade not in Student.grade_values:
            return False
        
        # Overwrite the existing grade with a new grade
        self.course_grades[course_code] = grade # I don't love this '1' at all
        return True
        
    def calculate_gpa(self):
        total_points = 0
        total_credits = 0
        
        for course_code in self.course_grades.keys():
            grade = self.course_grades[course_code]
            if grade is not None:  # Only count courses with grades
                grade_points = Student.grade_values[grade] # F was int, but I don't think it matters
                total_points += grade_points
                total_credits += self.course_credits[course_code]
        
        if total_credits == 0:
            return 0
            
        return (total_points / total_credits) * Student.grade_values['A']
        
    def drop_course(self, course_code):
        Student._validate_input(course_code, 'course_code', str)
        
        if course_code in self.course_grades:
            del self.course_grades[course_code]
            del self.course_credits[course_code]
            return True
        
        return False
    
    @classmethod
    def _validate_input(self, obj: any, obj_name: str, correct_type: type):
        if obj is None:
            err = f'{obj_name} is None'
            print(err)
            raise TypeError(err)
        
        if not isinstance(obj, correct_type):
            err = f'{obj_name} is not a {correct_type}'
            print(err)
            raise TypeError(err) 
        
        if correct_type == str:
            if len(obj) == 0:
                err = f'{obj_name} is empty string'
                print(err)
                raise ValueError(err)



def main():
    # Create a student
    alice = Student("Alice Smith", "A12345")
    
    # Test enrollment
    courses = [
        ("CS101", 3),
        ("MATH200", 4),
        ("PHY101", 4),
        ("CS101", 3),  # Duplicate enrollment attempt
    ]
    
    for course, credits in courses:
        if alice.enroll(course, credits):
            print(f"Enrolled in {course}")
        else:
            print(f"Failed to enroll in {course}")
    
    # Assign some grades
    grades = [
        ("CS101", "A"),
        ("MATH200", "B"),
        ("PHY101", "C"),
    ]
    
    for course, grade in grades:
        if alice.assign_grade(course, grade):
            print(f"Assigned grade {grade} for {course}")
    
    # Calculate GPA
    print(f"GPA: {alice.calculate_gpa():.2f}")
    
    # Drop a course
    alice.drop_course("MATH200")
    print(f'Dropped {"MATH200"}')
    print(f"New GPA: {alice.calculate_gpa():.2f}")


if __name__ == "__main__":
    main()