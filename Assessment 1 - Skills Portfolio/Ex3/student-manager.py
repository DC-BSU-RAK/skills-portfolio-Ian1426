import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

"""Student Marks Management GUI

This module provides a small Tkinter application to manage student records
and marks. The UI shows records, allows adding/updating/deleting students,
and computes simple statistics. The edits here are purely to make the code
more readable (constants, docstrings) while preserving original behaviour.

The user requested comments explaining the code; inline comments are
added throughout to clarify intent and important steps without changing
the runtime behavior.
"""

# Configuration constants: centralize common values so they're easy to change
DATA_FILE = "studentMarks.txt"  # file used to persist student records
COURSEWORK_MAX = 60  # total possible coursework marks (3 items x 20 each) 
EXAM_MAX = 100      # max exam mark
TOTAL_POSSIBLE = COURSEWORK_MAX + EXAM_MAX  # combined total for percentage calcs
# UI colors
MAIN_BG = "#0ff3e0"   # soft light blue
BUTTON_BG = "#1de5ff" # soft light green

class StudentMarksApp:
    def __init__(self, root):
        # Keep a reference to the main Tk root window
        self.root = root
        # Set window title and a reasonable default size
        self.root.title("Student Records")
        self.root.geometry("900x700")

        # In-memory list of student dicts. Each entry has keys:
        # 'code' (int), 'name' (str), 'course_marks' (list of 3 ints), 'exam_mark' (int)
        self.students = []
        # Load existing data from disk (or create sample data if missing)
        self.load_data()

        # Build the UI: menu and main display area
        self.create_menu()
        self.create_main_display()
        
    def load_data(self):
        """Load student data from the file"""
        try:
            # If the data file does not exist, populate with sample data and exit
            if not os.path.exists(DATA_FILE):
                self.create_sample_data()
                return

            # Read all lines from the file. The expected format is:
            # Line 1: number of student records (N)
            # Next N lines: code,name,mark1,mark2,mark3,exam
            with open(DATA_FILE, 'r') as file:
                lines = file.readlines()

            # Reset the in-memory list before loading
            self.students = []

            # If file contains content, parse it cautiously to avoid crashes
            if lines:
                # First line should be an integer count
                num_students = int(lines[0].strip())

                # Iterate over up to num_students lines (but don't exceed file length)
                for i in range(1, min(num_students + 1, len(lines))):
                    line = lines[i].strip()
                    if not line:
                        # Skip empty lines gracefully
                        continue
                    parts = line.split(',')
                    if len(parts) < 6:
                        # Skip malformed lines that don't have expected fields
                        continue

                    # Parse fields; convert numeric strings to ints
                    student_code = int(parts[0])
                    student_name = parts[1]
                    course_marks = [int(parts[2]), int(parts[3]), int(parts[4])]
                    exam_mark = int(parts[5])

                    # Build a student dict and append to the list
                    student = {
                        'code': student_code,
                        'name': student_name,
                        'course_marks': course_marks,
                        'exam_mark': exam_mark
                    }
                    self.students.append(student)
                        
        except Exception as e:
            # On any error while loading, inform the user and fall back to sample data
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.create_sample_data()
    
    def save_data(self):
        """Save student data to the file"""
        try:
            # Write the count line followed by one student per line in CSV format
            with open(DATA_FILE, 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    # Maintain the same CSV format the original code expected
                    file.write(
                        f"{student['code']},{student['name']},{student['course_marks'][0]},{student['course_marks'][1]},{student['course_marks'][2]},{student['exam_mark']}\n"
                    )
            return True
        except Exception as e:
            # If saving fails, surface an error to the user and return False
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def create_sample_data(self):
        """Create sample data for testing"""
        # Provide a small set of sample students so the UI is usable on first run
        sample_students = [
            {"code": 8439, "name": "Jake Hobbs", "course_marks": [10, 11, 10], "exam_mark": 43},
            {"code": 7562, "name": "Sarah Smith", "course_marks": [15, 14, 16], "exam_mark": 78},
            {"code": 9123, "name": "Mike Johnson", "course_marks": [12, 13, 11], "exam_mark": 65},
            {"code": 6347, "name": "Emma Wilson", "course_marks": [18, 17, 19], "exam_mark": 92},
            {"code": 5289, "name": "Tom Brown", "course_marks": [8, 9, 7], "exam_mark": 35}
        ]
        self.students = sample_students
        # Persist sample data so subsequent runs will load it
        self.save_data()
    
    def calculate_student_stats(self, student):
        """Calculate statistics for a student"""
        # Sum the three coursework marks and add the exam mark
        total_coursework = sum(student['course_marks'])
        total_marks = total_coursework + student['exam_mark']
        # Compute percentage against the defined total possible marks
        percentage = (total_marks / TOTAL_POSSIBLE) * 100

        # Determine grade using standard cutoffs used by the original code
        if percentage >= 70:
            grade = 'A'
        elif percentage >= 60:
            grade = 'B'
        elif percentage >= 50:
            grade = 'C'
        elif percentage >= 40:
            grade = 'D'
        else:
            grade = 'F'

        # Return a small stats dict used by multiple display routines
        return {
            'total_coursework': total_coursework,
            'exam_mark': student['exam_mark'],
            'percentage': percentage,
            'grade': grade
        }
    
    def create_menu(self):
        """Create the main menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu: refresh or exit
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Data", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # View menu: show all / individual / highest / lowest
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="All Student Records", command=self.view_all_students)
        view_menu.add_command(label="Individual Student Record", command=self.view_individual_student)
        view_menu.add_separator()
        view_menu.add_command(label="Highest Overall Mark", command=self.show_highest_mark)
        view_menu.add_command(label="Lowest Overall Mark", command=self.show_lowest_mark)

        # Sort menu: multiple sorting options (delegates to sort_students)
        sort_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sort", menu=sort_menu)
        sort_menu.add_command(label="By Name (Ascending)", command=lambda: self.sort_students('name', True))
        sort_menu.add_command(label="By Name (Descending)", command=lambda: self.sort_students('name', False))
        sort_menu.add_command(label="By Percentage (Ascending)", command=lambda: self.sort_students('percentage', True))
        sort_menu.add_command(label="By Percentage (Descending)", command=lambda: self.sort_students('percentage', False))
        sort_menu.add_command(label="By Student Code (Ascending)", command=lambda: self.sort_students('code', True))
        sort_menu.add_command(label="By Student Code (Descending)", command=lambda: self.sort_students('code', False))

        # Manage menu: add, delete, update operations
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Manage", menu=manage_menu)
        manage_menu.add_command(label="Add Student Record", command=self.add_student_record)
        manage_menu.add_command(label="Delete Student Record", command=self.delete_student_record)
        manage_menu.add_command(label="Update Student Record", command=self.update_student_record)
    
    def create_main_display(self):
        """Create the main display area"""
        # Build a main frame using tk.Frame so background color is visible
        main_frame = tk.Frame(self.root, bg=MAIN_BG, padx=10, pady=10)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title label at the top using tk.Label so it inherits the bg color
        title_label = tk.Label(main_frame, text="Student Marks Management System",
                               font=("Arial", 16, "bold"), bg=MAIN_BG)
        title_label.grid(row=0, column=0, pady=(0, 12), sticky=tk.W)

        # Control bar frame with green background to host quick action buttons
        control_frame = tk.Frame(main_frame, bg=BUTTON_BG, pady=6)
        control_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        # Quick-action buttons (use ttk for native look; placed on green frame)
        ttk.Button(control_frame, text="View All", command=self.view_all_students).pack(side=tk.LEFT, padx=6)
        ttk.Button(control_frame, text="Add", command=self.add_student_record).pack(side=tk.LEFT, padx=6)
        ttk.Button(control_frame, text="Update", command=self.update_student_record).pack(side=tk.LEFT, padx=6)
        ttk.Button(control_frame, text="Delete", command=self.delete_student_record).pack(side=tk.LEFT, padx=6)
        ttk.Button(control_frame, text="Refresh", command=self.refresh_data).pack(side=tk.LEFT, padx=6)

        # A read-only scrolling text widget where reports and results are shown
        # Set its background to white so content remains readable on the blue page
        self.text_area = scrolledtext.ScrolledText(main_frame, width=90, height=28,
                                                  font=("Courier", 10), bg="white")
        self.text_area.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights so the text area expands with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
    
    def refresh_data(self):
        """Refresh data from file"""
        # Reload data from disk and update the display
        self.load_data()
        self.clear_display()
        self.display_text("Data refreshed from file.\n")
    
    def clear_display(self):
        """Clear the text display area"""
        # Delete everything in the text widget
        self.text_area.delete(1.0, tk.END)
    
    def display_text(self, text):
        """Display text in the text area"""
        # Insert text at the end and scroll to show it
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)
    
    def view_all_students(self):
        """Display all student records"""
        self.clear_display()
        
        if not self.students:
            self.display_text("No student data available.\n")
            return
        
        # Header
        header = f"{'Name':<20} {'Code':<8} {'Coursework':<12} {'Exam':<6} {'Percentage':<10} {'Grade':<6}\n"
        separator = "-" * 70 + "\n"
        self.display_text(header)
        self.display_text(separator)
        
        total_percentage = 0

        # For each student compute stats and append a nicely formatted line
        for student in self.students:
            stats = self.calculate_student_stats(student)

            student_line = f"{student['name']:<20} {student['code']:<8} " \
                          f"{stats['total_coursework']:<12} {stats['exam_mark']:<6} " \
                          f"{stats['percentage']:<10.1f} {stats['grade']:<6}\n"
            self.display_text(student_line)

            # Keep a running total of percentages for the summary
            total_percentage += stats['percentage']

        # Summary block showing count and average percentage
        self.display_text(separator)
        avg_percentage = total_percentage / len(self.students)
        summary = f"\nSummary:\n"
        summary += f"Number of students: {len(self.students)}\n"
        summary += f"Average percentage: {avg_percentage:.1f}%\n"
        self.display_text(summary)
    
    def view_individual_student(self):
        """Display individual student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student data available.")
            return
        
        student_index = self.select_student_dialog("Select Student to View")
        if student_index is not None:
            self.display_individual_student(student_index)
    
    def display_individual_student(self, student_index):
        """Display individual student record in main window"""
        self.clear_display()
        
        student = self.students[student_index]
        stats = self.calculate_student_stats(student)
        
        self.display_text("INDIVIDUAL STUDENT RECORD\n")
        self.display_text("=" * 40 + "\n\n")
        
        self.display_text(f"Student Name: {student['name']}\n")
        self.display_text(f"Student Code: {student['code']}\n")
        self.display_text(f"Coursework Marks: {student['course_marks']}\n")
        # Use constants in the user-facing strings where appropriate
        self.display_text(f"Total Coursework: {stats['total_coursework']}/{COURSEWORK_MAX}\n")
        self.display_text(f"Exam Mark: {stats['exam_mark']}/{EXAM_MAX}\n")
        self.display_text(f"Overall Percentage: {stats['percentage']:.1f}%\n")
        self.display_text(f"Grade: {stats['grade']}\n")
        
        # Detailed breakdown
        self.display_text(f"\nDetailed Breakdown:\n")
        # Detailed percentage breakdown for coursework and exam
        self.display_text(f"  Coursework: {stats['total_coursework']}/{COURSEWORK_MAX} " \
                 f"({(stats['total_coursework']/COURSEWORK_MAX)*100:.1f}%)\n")
        self.display_text(f"  Exam: {stats['exam_mark']}/{EXAM_MAX} " \
                 f"({(stats['exam_mark']/EXAM_MAX)*100:.1f}%)\n")
        # Total uses TOTAL_POSSIBLE for clarity
        self.display_text(f"  Total: {stats['total_coursework'] + stats['exam_mark']}/{TOTAL_POSSIBLE}\n")
    
    def show_highest_mark(self):
        """Display student with highest overall mark"""
        self.clear_display()
        
        if not self.students:
            self.display_text("No student data available.\n")
            return
        
        # Iterate over students and track the one with the highest percentage
        highest_student = None
        highest_percentage = -1

        for student in self.students:
            stats = self.calculate_student_stats(student)
            if stats['percentage'] > highest_percentage:
                highest_percentage = stats['percentage']
                highest_student = student
                highest_stats = stats
        
        self.display_text("STUDENT WITH HIGHEST OVERALL MARK\n")
        self.display_text("=" * 45 + "\n\n")
        
        if highest_student:
            self.display_text(f"Student Name: {highest_student['name']}\n")
            self.display_text(f"Student Code: {highest_student['code']}\n")
            self.display_text(f"Coursework Marks: {highest_student['course_marks']}\n")
            self.display_text(f"Total Coursework: {highest_stats['total_coursework']}/60\n")
            self.display_text(f"Exam Mark: {highest_stats['exam_mark']}/100\n")
            self.display_text(f"Overall Percentage: {highest_stats['percentage']:.1f}%\n")
            self.display_text(f"Grade: {highest_stats['grade']}\n")
    
    def show_lowest_mark(self):
        """Display student with lowest overall mark"""
        self.clear_display()
        
        if not self.students:
            self.display_text("No student data available.\n")
            return
        
        # Iterate and find the minimum percentage
        lowest_student = None
        lowest_percentage = 101

        for student in self.students:
            stats = self.calculate_student_stats(student)
            if stats['percentage'] < lowest_percentage:
                lowest_percentage = stats['percentage']
                lowest_student = student
                lowest_stats = stats
        
        self.display_text("STUDENT WITH LOWEST OVERALL MARK\n")
        self.display_text("=" * 44 + "\n\n")
        
        if lowest_student:
            self.display_text(f"Student Name: {lowest_student['name']}\n")
            self.display_text(f"Student Code: {lowest_student['code']}\n")
            self.display_text(f"Coursework Marks: {lowest_student['course_marks']}\n")
            self.display_text(f"Total Coursework: {lowest_stats['total_coursework']}/60\n")
            self.display_text(f"Exam Mark: {lowest_stats['exam_mark']}/100\n")
            self.display_text(f"Overall Percentage: {lowest_stats['percentage']:.1f}%\n")
            self.display_text(f"Grade: {lowest_stats['grade']}\n")
    
    def sort_students(self, sort_by, ascending=True):
        """Sort students by specified field"""
        if not self.students:
            messagebox.showwarning("Warning", "No student data available.")
            return
        
        # Pair each student with its computed stats so we can sort by percentage
        students_with_stats = []
        for student in self.students:
            stats = self.calculate_student_stats(student)
            students_with_stats.append((student, stats))
        
        # Sort based on the specified field
        if sort_by == 'name':
            students_with_stats.sort(key=lambda x: x[0]['name'].lower(), reverse=not ascending)
        elif sort_by == 'percentage':
            students_with_stats.sort(key=lambda x: x[1]['percentage'], reverse=not ascending)
        elif sort_by == 'code':
            students_with_stats.sort(key=lambda x: x[0]['code'], reverse=not ascending)
        
        # Replace students list with the sorted order (extract the student element)
        self.students = [item[0] for item in students_with_stats]

        # Persist the new ordering to disk
        self.save_data()

        # Show a header and display the sorted table
        self.clear_display()
        direction = "Ascending" if ascending else "Descending"
        self.display_text(f"STUDENT RECORDS SORTED BY {sort_by.upper()} ({direction})\n")
        self.display_text("=" * 60 + "\n\n")
        self.view_all_students()
    
    def add_student_record(self):
        """Add a new student record"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Student")
        add_window.geometry("400x400")
        add_window.transient(self.root)
        add_window.grab_set()
        
        # Form fields
        ttk.Label(add_window, text="Add New Student Record", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(add_window, text="Student Code:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        code_entry = ttk.Entry(add_window)
        code_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(add_window, text="Student Name:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(add_window, text="Coursework Marks (out of 20):").grid(row=3, column=0, columnspan=2, pady=5)
        
        ttk.Label(add_window, text="Mark 1:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        mark1_entry = ttk.Spinbox(add_window, from_=0, to=20, width=10)
        mark1_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(add_window, text="Mark 2:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        mark2_entry = ttk.Spinbox(add_window, from_=0, to=20, width=10)
        mark2_entry.grid(row=5, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(add_window, text="Mark 3:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        mark3_entry = ttk.Spinbox(add_window, from_=0, to=20, width=10)
        mark3_entry.grid(row=6, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(add_window, text="Exam Mark (out of 100):").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        exam_entry = ttk.Spinbox(add_window, from_=0, to=100, width=10)
        exam_entry.grid(row=7, column=1, sticky=tk.W, padx=5, pady=5)
        
        def save_student():
            """Validate inputs from the Add dialog and append the new record."""
            try:
                # Parse form inputs (may raise ValueError)
                code = int(code_entry.get())
                name = name_entry.get().strip()
                mark1 = int(mark1_entry.get())
                mark2 = int(mark2_entry.get())
                mark3 = int(mark3_entry.get())
                exam = int(exam_entry.get())

                # Simple validation for required name
                if not name:
                    messagebox.showerror("Error", "Student name cannot be empty.")
                    return

                # Ensure student code is unique
                if any(student['code'] == code for student in self.students):
                    messagebox.showerror("Error", "Student code already exists.")
                    return

                # Validate that coursework marks and exam fall within allowed ranges
                if not (0 <= mark1 <= 20 and 0 <= mark2 <= 20 and 0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                    return

                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                    return

                # Construct and append the new student record
                new_student = {
                    'code': code,
                    'name': name,
                    'course_marks': [mark1, mark2, mark3],
                    'exam_mark': exam
                }

                self.students.append(new_student)

                # Try to save; if successful, close dialog and refresh view
                if self.save_data():
                    messagebox.showinfo("Success", "Student record added successfully!")
                    add_window.destroy()
                    self.view_all_students()
                else:
                    # If saving failed, remove the in-memory record to keep data consistent
                    self.students.remove(new_student)

            except ValueError:
                # Handles non-integer input parsing attempts
                messagebox.showerror("Error", "Please enter valid numeric values.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add student: {str(e)}")
        
        ttk.Button(add_window, text="Save", command=save_student).grid(row=8, column=0, columnspan=2, pady=20)
        
        # Configure grid weights
        add_window.columnconfigure(1, weight=1)
    
    def delete_student_record(self):
        """Delete a student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student data available.")
            return
        
        student_index = self.select_student_dialog("Select Student to Delete")
        if student_index is not None:
            student = self.students[student_index]

            # Confirm destructive action with user
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete {student['name']} (Code: {student['code']})?"
            )

            if confirm:
                # Remove from in-memory list and attempt to save
                deleted_student = self.students.pop(student_index)
                if self.save_data():
                    messagebox.showinfo("Success", f"Student {deleted_student['name']} deleted successfully!")
                    self.view_all_students()
                else:
                    # On failure, restore the record to keep memory and disk consistent
                    self.students.insert(student_index, deleted_student)
                    messagebox.showerror("Error", "Failed to delete student record.")
    
    def update_student_record(self):
        """Update a student record"""
        if not self.students:
            messagebox.showwarning("Warning", "No student data available.")
            return
        
        student_index = self.select_student_dialog("Select Student to Update")
        if student_index is not None:
            self.show_update_dialog(student_index)
    
    def show_update_dialog(self, student_index):
        """Show dialog for updating student record"""
        student = self.students[student_index]
        
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Update Student: {student['name']}")
        update_window.geometry("400x450")
        update_window.transient(self.root)
        update_window.grab_set()
        
        ttk.Label(update_window, text=f"Update {student['name']}'s Record", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Current values
        ttk.Label(update_window, text="Current Values:", font=("Arial", 10, "bold")).grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(update_window, text=f"Student Code: {student['code']}").grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5)
        ttk.Label(update_window, text=f"Student Name: {student['name']}").grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5)
        ttk.Label(update_window, text=f"Coursework Marks: {student['course_marks']}").grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=5)
        ttk.Label(update_window, text=f"Exam Mark: {student['exam_mark']}").grid(row=5, column=0, columnspan=2, sticky=tk.W, padx=5)
        
        ttk.Label(update_window, text="\nUpdate Fields:", font=("Arial", 10, "bold")).grid(row=6, column=0, columnspan=2, pady=10)
        
        # Update fields
        ttk.Label(update_window, text="New Name:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        name_entry = ttk.Entry(update_window)
        name_entry.insert(0, student['name'])
        name_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(update_window, text="Coursework Marks:").grid(row=8, column=0, columnspan=2, pady=5)
        
        ttk.Label(update_window, text="Mark 1:").grid(row=9, column=0, sticky=tk.W, padx=5, pady=2)
        mark1_entry = ttk.Spinbox(update_window, from_=0, to=20, width=10)
        mark1_entry.set(student['course_marks'][0])
        mark1_entry.grid(row=9, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(update_window, text="Mark 2:").grid(row=10, column=0, sticky=tk.W, padx=5, pady=2)
        mark2_entry = ttk.Spinbox(update_window, from_=0, to=20, width=10)
        mark2_entry.set(student['course_marks'][1])
        mark2_entry.grid(row=10, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(update_window, text="Mark 3:").grid(row=11, column=0, sticky=tk.W, padx=5, pady=2)
        mark3_entry = ttk.Spinbox(update_window, from_=0, to=20, width=10)
        mark3_entry.set(student['course_marks'][2])
        mark3_entry.grid(row=11, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(update_window, text="Exam Mark:").grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
        exam_entry = ttk.Spinbox(update_window, from_=0, to=100, width=10)
        exam_entry.set(student['exam_mark'])
        exam_entry.grid(row=12, column=1, sticky=tk.W, padx=5, pady=5)
        
        def save_updates():
            """Validate updated fields and persist changes to disk."""
            try:
                name = name_entry.get().strip()
                mark1 = int(mark1_entry.get())
                mark2 = int(mark2_entry.get())
                mark3 = int(mark3_entry.get())
                exam = int(exam_entry.get())

                if not name:
                    messagebox.showerror("Error", "Student name cannot be empty.")
                    return

                # Validate numeric ranges
                if not (0 <= mark1 <= 20 and 0 <= mark2 <= 20 and 0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                    return

                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                    return

                # Apply changes to the in-memory record
                self.students[student_index]['name'] = name
                self.students[student_index]['course_marks'] = [mark1, mark2, mark3]
                self.students[student_index]['exam_mark'] = exam

                # Try to persist; on success refresh the view, otherwise inform user
                if self.save_data():
                    messagebox.showinfo("Success", "Student record updated successfully!")
                    update_window.destroy()
                    self.view_all_students()
                else:
                    messagebox.showerror("Error", "Failed to update student record.")

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update student: {str(e)}")
        
        ttk.Button(update_window, text="Save Updates", command=save_updates).grid(row=13, column=0, columnspan=2, pady=20)
        
        # Configure grid weights
        update_window.columnconfigure(1, weight=1)
    
    def select_student_dialog(self, title):
        """Generic dialog for selecting a student"""
        selection_window = tk.Toplevel(self.root)
        selection_window.title(title)
        selection_window.geometry("300x150")
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        ttk.Label(selection_window, text="Select Student:").pack(pady=10)
        
        # Create a combobox listing each student by 'code - name'
        student_options = [f"{s['code']} - {s['name']}" for s in self.students]
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(selection_window, textvariable=student_var,
                                   values=student_options, state="readonly")
        student_combo.pack(pady=10)

        # We'll capture the selected index via a single-element list so the
        # nested confirm_selection() can mutate it (closure over the list).
        selected_index = [None]

        def confirm_selection():
            # Set the selected index from the combobox and close the dialog
            selected_index[0] = student_combo.current()
            selection_window.destroy()

        ttk.Button(selection_window, text="Select",
                  command=confirm_selection).pack(pady=10)

        # Block until the selection window is closed, then return the index
        self.root.wait_window(selection_window)

        return selected_index[0]

def main():
    root = tk.Tk()
    app = StudentMarksApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()