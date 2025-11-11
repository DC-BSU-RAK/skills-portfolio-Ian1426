import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os

class StudentMarksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management System")
        self.root.geometry("900x700")
        
        # Initialize data storage
        self.students = []
        self.load_data()
        
        # Create GUI
        self.create_menu()
        self.create_main_display()
        
    def load_data(self):
        """Load student data from the file"""
        try:
            file_path = "studentMarks.txt"
            if not os.path.exists(file_path):
                # Create sample data if file doesn't exist
                self.create_sample_data()
                return
                
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            self.students = []  # Clear existing data
                
            # First line is number of students
            if lines:
                num_students = int(lines[0].strip())
                
                # Process each student line
                for i in range(1, min(num_students + 1, len(lines))):
                    line = lines[i].strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 6:
                            student_code = int(parts[0])
                            student_name = parts[1]
                            course_marks = [int(parts[2]), int(parts[3]), int(parts[4])]
                            exam_mark = int(parts[5])
                            
                            student = {
                                'code': student_code,
                                'name': student_name,
                                'course_marks': course_marks,
                                'exam_mark': exam_mark
                            }
                            self.students.append(student)
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.create_sample_data()
    
    def save_data(self):
        """Save student data to the file"""
        try:
            with open("studentMarks.txt", 'w') as file:
                file.write(f"{len(self.students)}\n")
                for student in self.students:
                    file.write(f"{student['code']},{student['name']},{student['course_marks'][0]},{student['course_marks'][1]},{student['course_marks'][2]},{student['exam_mark']}\n")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False
    
    def create_sample_data(self):
        """Create sample data for testing"""
        sample_students = [
            {"code": 8439, "name": "Jake Hobbs", "course_marks": [10, 11, 10], "exam_mark": 43},
            {"code": 7562, "name": "Sarah Smith", "course_marks": [15, 14, 16], "exam_mark": 78},
            {"code": 9123, "name": "Mike Johnson", "course_marks": [12, 13, 11], "exam_mark": 65},
            {"code": 6347, "name": "Emma Wilson", "course_marks": [18, 17, 19], "exam_mark": 92},
            {"code": 5289, "name": "Tom Brown", "course_marks": [8, 9, 7], "exam_mark": 35}
        ]
        self.students = sample_students
        self.save_data()
    
    def calculate_student_stats(self, student):
        """Calculate statistics for a student"""
        total_coursework = sum(student['course_marks'])
        total_marks = total_coursework + student['exam_mark']
        percentage = (total_marks / 160) * 100
        
        # Determine grade
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
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh Data", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="All Student Records", command=self.view_all_students)
        view_menu.add_command(label="Individual Student Record", command=self.view_individual_student)
        view_menu.add_separator()
        view_menu.add_command(label="Highest Overall Mark", command=self.show_highest_mark)
        view_menu.add_command(label="Lowest Overall Mark", command=self.show_lowest_mark)
        
        # Sort menu
        sort_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sort", menu=sort_menu)
        sort_menu.add_command(label="By Name (Ascending)", command=lambda: self.sort_students('name', True))
        sort_menu.add_command(label="By Name (Descending)", command=lambda: self.sort_students('name', False))
        sort_menu.add_command(label="By Percentage (Ascending)", command=lambda: self.sort_students('percentage', True))
        sort_menu.add_command(label="By Percentage (Descending)", command=lambda: self.sort_students('percentage', False))
        sort_menu.add_command(label="By Student Code (Ascending)", command=lambda: self.sort_students('code', True))
        sort_menu.add_command(label="By Student Code (Descending)", command=lambda: self.sort_students('code', False))
        
        # Manage menu
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Manage", menu=manage_menu)
        manage_menu.add_command(label="Add Student Record", command=self.add_student_record)
        manage_menu.add_command(label="Delete Student Record", command=self.delete_student_record)
        manage_menu.add_command(label="Update Student Record", command=self.update_student_record)
    
    def create_main_display(self):
        """Create the main display area"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Student Marks Management System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Text area for displaying results
        self.text_area = scrolledtext.ScrolledText(main_frame, width=90, height=30, 
                                                  font=("Courier", 10))
        self.text_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
    
    def refresh_data(self):
        """Refresh data from file"""
        self.load_data()
        self.clear_display()
        self.display_text("Data refreshed from file.\n")
    
    def clear_display(self):
        """Clear the text display area"""
        self.text_area.delete(1.0, tk.END)
    
    def display_text(self, text):
        """Display text in the text area"""
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
        
        # Display each student
        for student in self.students:
            stats = self.calculate_student_stats(student)
            
            student_line = f"{student['name']:<20} {student['code']:<8} " \
                          f"{stats['total_coursework']:<12} {stats['exam_mark']:<6} " \
                          f"{stats['percentage']:<10.1f} {stats['grade']:<6}\n"
            self.display_text(student_line)
            
            total_percentage += stats['percentage']
        
        # Summary
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
        self.display_text(f"Total Coursework: {stats['total_coursework']}/60\n")
        self.display_text(f"Exam Mark: {stats['exam_mark']}/100\n")
        self.display_text(f"Overall Percentage: {stats['percentage']:.1f}%\n")
        self.display_text(f"Grade: {stats['grade']}\n")
        
        # Detailed breakdown
        self.display_text(f"\nDetailed Breakdown:\n")
        self.display_text(f"  Coursework: {stats['total_coursework']}/60 " \
                         f"({(stats['total_coursework']/60)*100:.1f}%)\n")
        self.display_text(f"  Exam: {stats['exam_mark']}/100 " \
                         f"({(stats['exam_mark']/100)*100:.1f}%)\n")
        self.display_text(f"  Total: {stats['total_coursework'] + stats['exam_mark']}/160\n")
    
    def show_highest_mark(self):
        """Display student with highest overall mark"""
        self.clear_display()
        
        if not self.students:
            self.display_text("No student data available.\n")
            return
        
        # Find student with highest percentage
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
        
        # Find student with lowest percentage
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
        
        # Create a copy to avoid modifying original during calculation
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
        
        # Update the main students list with sorted order
        self.students = [item[0] for item in students_with_stats]
        
        # Save the sorted data
        self.save_data()
        
        # Display sorted results
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
            try:
                # Validate inputs
                code = int(code_entry.get())
                name = name_entry.get().strip()
                mark1 = int(mark1_entry.get())
                mark2 = int(mark2_entry.get())
                mark3 = int(mark3_entry.get())
                exam = int(exam_entry.get())
                
                if not name:
                    messagebox.showerror("Error", "Student name cannot be empty.")
                    return
                
                # Check if code already exists
                if any(student['code'] == code for student in self.students):
                    messagebox.showerror("Error", "Student code already exists.")
                    return
                
                # Validate marks
                if not (0 <= mark1 <= 20 and 0 <= mark2 <= 20 and 0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                    return
                
                # Add new student
                new_student = {
                    'code': code,
                    'name': name,
                    'course_marks': [mark1, mark2, mark3],
                    'exam_mark': exam
                }
                
                self.students.append(new_student)
                
                if self.save_data():
                    messagebox.showinfo("Success", "Student record added successfully!")
                    add_window.destroy()
                    self.view_all_students()
                else:
                    # Remove the student if save failed
                    self.students.remove(new_student)
                    
            except ValueError:
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
            
            confirm = messagebox.askyesno(
                "Confirm Delete", 
                f"Are you sure you want to delete {student['name']} (Code: {student['code']})?"
            )
            
            if confirm:
                deleted_student = self.students.pop(student_index)
                if self.save_data():
                    messagebox.showinfo("Success", f"Student {deleted_student['name']} deleted successfully!")
                    self.view_all_students()
                else:
                    # Restore the student if save failed
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
            try:
                name = name_entry.get().strip()
                mark1 = int(mark1_entry.get())
                mark2 = int(mark2_entry.get())
                mark3 = int(mark3_entry.get())
                exam = int(exam_entry.get())
                
                if not name:
                    messagebox.showerror("Error", "Student name cannot be empty.")
                    return
                
                # Validate marks
                if not (0 <= mark1 <= 20 and 0 <= mark2 <= 20 and 0 <= mark3 <= 20):
                    messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                    return
                
                if not (0 <= exam <= 100):
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                    return
                
                # Update student record
                self.students[student_index]['name'] = name
                self.students[student_index]['course_marks'] = [mark1, mark2, mark3]
                self.students[student_index]['exam_mark'] = exam
                
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
        
        # Create combobox with student names and codes
        student_options = [f"{s['code']} - {s['name']}" for s in self.students]
        student_var = tk.StringVar()
        student_combo = ttk.Combobox(selection_window, textvariable=student_var, 
                                   values=student_options, state="readonly")
        student_combo.pack(pady=10)
        
        selected_index = [None]  # Use list to store mutable value
        
        def confirm_selection():
            selected_index[0] = student_combo.current()
            selection_window.destroy()
        
        ttk.Button(selection_window, text="Select", 
                  command=confirm_selection).pack(pady=10)
        
        # Wait for window to close
        self.root.wait_window(selection_window)
        
        return selected_index[0]

def main():
    root = tk.Tk()
    app = StudentMarksApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()