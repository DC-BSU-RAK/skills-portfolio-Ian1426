import os

def load_students(filename="studentMarks.txt"):
    """Load student records from file"""
    students = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Skip empty lines
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 4:
                        student = {
                            'code': parts[0],
                            'name': parts[1],
                            'exam_mark': int(parts[2]),
                            'grade': parts[3]
                        }
                        students.append(student)
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Starting with empty student list.")
    return students

def save_students(students, filename="studentMarks.txt"):
    """Save student records to file"""
    with open(filename, 'w') as file:
        for student in students:
            file.write(f"{student['code']},{student['name']},{student['exam_mark']},{student['grade']}\n")

def calculate_grade(mark):
    """Calculate grade based on mark"""
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"

def display_students(students):
    """Display all students in a formatted table"""
    if not students:
        print("No student records found.")
        return
    
    print("\nStudent Records:")
    print("-" * 60)
    print(f"{'Code':<10} {'Name':<20} {'Exam Mark':<10} {'Grade':<5}")
    print("-" * 60)
    for student in students:
        print(f"{student['code']:<10} {student['name']:<20} {student['exam_mark']:<10} {student['grade']:<5}")
    print("-" * 60)

def sort_students(students):
    """Sort student records"""
    if not students:
        print("No student records to sort.")
        return students
    
    print("\nSort Options:")
    print("1. Sort by Student Code (Ascending)")
    print("2. Sort by Student Code (Descending)")
    print("3. Sort by Name (Ascending)")
    print("4. Sort by Name (Descending)")
    print("5. Sort by Exam Mark (Ascending)")
    print("6. Sort by Exam Mark (Descending)")
    
    choice = input("Enter your choice (1-6): ")
    
    if choice == '1':
        students.sort(key=lambda x: x['code'])
    elif choice == '2':
        students.sort(key=lambda x: x['code'], reverse=True)
    elif choice == '3':
        students.sort(key=lambda x: x['name'])
    elif choice == '4':
        students.sort(key=lambda x: x['name'], reverse=True)
    elif choice == '5':
        students.sort(key=lambda x: x['exam_mark'])
    elif choice == '6':
        students.sort(key=lambda x: x['exam_mark'], reverse=True)
    else:
        print("Invalid choice. Returning to main menu.")
        return students
    
    print("Students sorted successfully!")
    return students

def add_student(students):
    """Add a new student record"""
    print("\nAdd New Student")
    print("-" * 20)
    
    code = input("Enter student code: ").strip()
    name = input("Enter student name: ").strip()
    
    # Check if student code already exists
    for student in students:
        if student['code'] == code:
            print(f"Error: Student with code '{code}' already exists.")
            return students
    
    # Validate and get exam mark
    try:
        exam_mark = int(input("Enter exam mark (0-100): "))
        if exam_mark < 0 or exam_mark > 100:
            print("Error: Exam mark must be between 0 and 100.")
            return students
    except ValueError:
        print("Error: Please enter a valid number for exam mark.")
        return students
    
    # Calculate grade
    grade = calculate_grade(exam_mark)
    
    # Add new student
    new_student = {
        'code': code,
        'name': name,
        'exam_mark': exam_mark,
        'grade': grade
    }
    students.append(new_student)
    
    print(f"Student '{name}' added successfully!")
    return students

def delete_student(students):
    """Delete a student record"""
    if not students:
        print("No student records to delete.")
        return students
    
    print("\nDelete Student")
    print("-" * 20)
    print("Search by:")
    print("1. Student Code")
    print("2. Student Name")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == '1':
        code = input("Enter student code to delete: ").strip()
        found = [s for s in students if s['code'] == code]
    elif choice == '2':
        name = input("Enter student name to delete: ").strip()
        found = [s for s in students if s['name'].lower() == name.lower()]
    else:
        print("Invalid choice.")
        return students
    
    if not found:
        print("No matching student found.")
        return students
    
    if len(found) > 1:
        print("Multiple students found:")
        for i, student in enumerate(found, 1):
            print(f"{i}. {student['code']} - {student['name']}")
        
        try:
            selection = int(input("Select student to delete (enter number): ")) - 1
            if 0 <= selection < len(found):
                student_to_delete = found[selection]
            else:
                print("Invalid selection.")
                return students
        except ValueError:
            print("Invalid input.")
            return students
    else:
        student_to_delete = found[0]
    
    # Confirm deletion
    print(f"\nStudent to delete: {student_to_delete['code']} - {student_to_delete['name']}")
    confirm = input("Are you sure you want to delete this student? (y/n): ").lower()
    
    if confirm == 'y':
        students.remove(student_to_delete)
        print("Student deleted successfully!")
    else:
        print("Deletion cancelled.")
    
    return students

def update_student(students):
    """Update a student record"""
    if not students:
        print("No student records to update.")
        return students
    
    print("\nUpdate Student")
    print("-" * 20)
    print("Search by:")
    print("1. Student Code")
    print("2. Student Name")
    
    choice = input("Enter your choice (1-2): ")
    
    if choice == '1':
        code = input("Enter student code to update: ").strip()
        found = [s for s in students if s['code'] == code]
    elif choice == '2':
        name = input("Enter student name to update: ").strip()
        found = [s for s in students if s['name'].lower() == name.lower()]
    else:
        print("Invalid choice.")
        return students
    
    if not found:
        print("No matching student found.")
        return students
    
    if len(found) > 1:
        print("Multiple students found:")
        for i, student in enumerate(found, 1):
            print(f"{i}. {student['code']} - {student['name']}")
        
        try:
            selection = int(input("Select student to update (enter number): ")) - 1
            if 0 <= selection < len(found):
                student_to_update = found[selection]
            else:
                print("Invalid selection.")
                return students
        except ValueError:
            print("Invalid input.")
            return students
    else:
        student_to_update = found[0]
    
    print(f"\nUpdating student: {student_to_update['code']} - {student_to_update['name']}")
    
    # Sub-menu for updating specific fields
    while True:
        print("\nUpdate Options:")
        print("1. Update Name")
        print("2. Update Exam Mark")
        print("3. Update Student Code")
        print("4. Finish Updating")
        
        update_choice = input("Enter your choice (1-4): ")
        
        if update_choice == '1':
            new_name = input("Enter new name: ").strip()
            if new_name:
                student_to_update['name'] = new_name
                print("Name updated successfully!")
            else:
                print("Name cannot be empty.")
        
        elif update_choice == '2':
            try:
                new_mark = int(input("Enter new exam mark (0-100): "))
                if 0 <= new_mark <= 100:
                    student_to_update['exam_mark'] = new_mark
                    student_to_update['grade'] = calculate_grade(new_mark)
                    print("Exam mark and grade updated successfully!")
                else:
                    print("Error: Exam mark must be between 0 and 100.")
            except ValueError:
                print("Error: Please enter a valid number for exam mark.")
        
        elif update_choice == '3':
            new_code = input("Enter new student code: ").strip()
            if new_code:
                # Check if new code already exists (excluding current student)
                if any(s['code'] == new_code and s != student_to_update for s in students):
                    print(f"Error: Student code '{new_code}' already exists.")
                else:
                    student_to_update['code'] = new_code
                    print("Student code updated successfully!")
            else:
                print("Student code cannot be empty.")
        
        elif update_choice == '4':
            print("Student update completed!")
            break
        
        else:
            print("Invalid choice. Please try again.")
    
    return students

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 40)
    print("        STUDENT MANAGER SYSTEM")
    print("=" * 40)
    print("1. Display all student records")
    print("2. Display students with grade A+ or A")
    print("3. Display students with grade F")
    print("4. Display class average and standard deviation")
    print("5. Sort student records")
    print("6. Add a student record")
    print("7. Delete a student record")
    print("8. Update a student record")
    print("9. Exit")
    print("-" * 40)

def calculate_statistics(students):
    """Calculate class average and standard deviation"""
    if not students:
        print("No student records available for statistics.")
        return
    
    marks = [student['exam_mark'] for student in students]
    average = sum(marks) / len(marks)
    
    # Calculate standard deviation
    variance = sum((mark - average) ** 2 for mark in marks) / len(marks)
    std_dev = variance ** 0.5
    
    print(f"\nClass Statistics:")
    print(f"Average Mark: {average:.2f}")
    print(f"Standard Deviation: {std_dev:.2f}")

def main():
    """Main program function"""
    students = load_students()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-9): ")
        
        if choice == '1':
            display_students(students)
        
        elif choice == '2':
            top_students = [s for s in students if s['grade'] in ['A+', 'A']]
            display_students(top_students)
        
        elif choice == '3':
            failing_students = [s for s in students if s['grade'] == 'F']
            display_students(failing_students)
        
        elif choice == '4':
            calculate_statistics(students)
        
        elif choice == '5':
            students = sort_students(students)
            display_students(students)
        
        elif choice == '6':
            students = add_student(students)
            save_students(students)
        
        elif choice == '7':
            students = delete_student(students)
            save_students(students)
        
        elif choice == '8':
            students = update_student(students)
            save_students(students)
        
        elif choice == '9':
            save_students(students)
            print("Student records saved. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()