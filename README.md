# School Management System

## Overview
This project is a School Management System that manages students, teachers, classes, enrollments, attendance, and comments.

## Prerequisites

### Step 1: Install Oracle Database 21c
- First, install **Oracle Database 21c** on your system.
- After installation, open **SQL Plus** and add the following tables by running the `CREATE TABLE` statements or copying the structure:

### SQL to Create Tables:

```sql
-- Create Students Table
CREATE TABLE students (
    studentid NUMBER NOT NULL,
    firstname VARCHAR2(50),
    lastname VARCHAR2(50),
    birthdate DATE,
    gender CHAR(1),
    class VARCHAR2(10),
    CONSTRAINT students_pk PRIMARY KEY (studentid)
);

-- Create Enrollments Table
CREATE TABLE enrollments (
    enrollmentid NUMBER NOT NULL,
    studentid NUMBER,
    classid NUMBER,
    enrollmentdate DATE,
    CONSTRAINT enrollments_pk PRIMARY KEY (enrollmentid),
    CONSTRAINT fk_student FOREIGN KEY (studentid) REFERENCES students(studentid),
    CONSTRAINT fk_class FOREIGN KEY (classid) REFERENCES classes(classid)
);

-- Create Teachers Table
CREATE TABLE teachers (
    teacherid NUMBER NOT NULL,
    firstname VARCHAR2(50),
    lastname VARCHAR2(50),
    subject VARCHAR2(50),
    CONSTRAINT teachers_pk PRIMARY KEY (teacherid)
);

-- Create Classes Table
CREATE TABLE classes (
    classid NUMBER NOT NULL,
    classname VARCHAR2(10),
    teacherid NUMBER,
    CONSTRAINT classes_pk PRIMARY KEY (classid),
    CONSTRAINT fk_teacher FOREIGN KEY (teacherid) REFERENCES teachers(teacherid)
);

-- Create Attendance Table
CREATE TABLE attendance (
    attendanceid NUMBER NOT NULL,
    studentid NUMBER,
    classid NUMBER,
    attendancedate DATE,
    status CHAR(1),
    CONSTRAINT attendance_pk PRIMARY KEY (attendanceid),
    CONSTRAINT fk_student_attendance FOREIGN KEY (studentid) REFERENCES students(studentid),
    CONSTRAINT fk_class_attendance FOREIGN KEY (classid) REFERENCES classes(classid)
);

-- Create Comments Table
CREATE TABLE comments (
    commentid NUMBER NOT NULL,
    studentid NUMBER NOT NULL,
    comment_text VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP(6),
    CONSTRAINT comments_pk PRIMARY KEY (commentid),
    CONSTRAINT fk_student_comments FOREIGN KEY (studentid) REFERENCES students(studentid)
);
```

After creating these tables, run `DESC` to confirm the table structure. If the data isn't showing as expected, run `COMMIT;` to save changes.

### Step 2: Install Django and Dependencies

1. **Create a Virtual Environment**:
   - It's recommended to use a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     ```

2. **Navigate to the Project Folder**:
   Navigate to the folder where your project is located and where the `requirements.txt` file is stored:
   ```bash
   cd School-Management-System  
   ```

3. **Install Dependencies**:
   Install the required dependencies via `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup in `settings.py`**:
   Update your **`settings.py`** file (inside the `school_management_system` folder) with the Oracle Database connection details. Here’s the section you should modify:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.oracle',
           'NAME': 'your_database_name',  # replace with your DB name
           'USER': 'your_db_user',        # replace with your DB username
           'PASSWORD': 'your_password',   # replace with your DB password
           'HOST': 'localhost',           # leave as localhost if local installation
           'PORT': '1521',                # Oracle DB default port
       }
   }
   ```

   Replace:
   - `your_database_name` with the name of your Oracle database.
   - `your_db_user` with your Oracle user.
   - `your_password` with your Oracle password.

5. **Run the Django Server**:
   Once you have the database set up and Django installed, run the server:
   ```bash
   python manage.py runserver
   ```

### Step 3: Sample Code to Insert Data in SQL Plus

Below is the SQL code for inserting sample data into each of the tables:

### 1. **`students` table**
```sql
INSERT INTO students (studentid, firstname, lastname, birthdate, gender, class)
VALUES (1, 'John', 'Doe', TO_DATE('2005-05-15', 'YYYY-MM-DD'), 'M', '10A');

INSERT INTO students (studentid, firstname, lastname, birthdate, gender, class)
VALUES (2, 'Jane', 'Smith', TO_DATE('2006-09-23', 'YYYY-MM-DD'), 'F', '10B');

COMMIT;
```

### 2. **`enrollments` table**
```sql
INSERT INTO enrollments (enrollmentid, studentid, classid, enrollmentdate)
VALUES (1, 1, 101, TO_DATE('2022-08-15', 'YYYY-MM-DD'));

INSERT INTO enrollments (enrollmentid, studentid, classid, enrollmentdate)
VALUES (2, 2, 102, TO_DATE('2022-09-01', 'YYYY-MM-DD'));

COMMIT;
```

### 3. **`teachers` table**
```sql
INSERT INTO teachers (teacherid, firstname, lastname, subject)
VALUES (1, 'Emily', 'Brown', 'Mathematics');

INSERT INTO teachers (teacherid, firstname, lastname, subject)
VALUES (2, 'Michael', 'Johnson', 'Physics');

COMMIT;
```

### 4. **`classes` table**
```sql
INSERT INTO classes (classid, classname, teacherid)
VALUES (101, '10A', 1);

INSERT INTO classes (classid, classname, teacherid)
VALUES (102, '10B', 2);

COMMIT;
```

### 5. **`attendance` table**
```sql
INSERT INTO attendance (attendanceid, studentid, classid, attendancedate, status)
VALUES (1, 1, 101, TO_DATE('2023-09-01', 'YYYY-MM-DD'), 'P');

INSERT INTO attendance (attendanceid, studentid, classid, attendancedate, status)
VALUES (2, 2, 102, TO_DATE('2023-09-01', 'YYYY-MM-DD'), 'A');

COMMIT;
```

### 6. **`comments` table**
```sql
INSERT INTO comments (commentid, studentid, comment_text, created_at)
VALUES (1, 1, 'Excellent performance in Mathematics.', SYSTIMESTAMP);

INSERT INTO comments (commentid, studentid, comment_text, created_at)
VALUES (2, 2, 'Needs improvement in Physics.', SYSTIMESTAMP);

COMMIT;
```

Make sure to run `COMMIT;` after inserting each set of data to ensure it is saved in the database.

### Step 4: Running the Project

1. After setting up the database and tables, run the Django server again if it’s not already running:
   ```bash
   python manage.py runserver
   ```

2. You can now access your project on the local server (e.g., `http://127.0.0.1:8000/`).
