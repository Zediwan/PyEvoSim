# pylint changes

We used pylint on the freshly created GUI_main.py.

## Run before fixing

![first pylint output](Docs/PYLINT_output_before_fix.png)

## First Fixes

The problems are numbered  (orange integers) in the screenshot above.

### 1 trailing newlines

Old code: Empty lines at the end of the file <br>
![1 old](Docs/1_old_code.png)<br>

Fixed code: removed empty lines, lkast line is now last line of code

![1 new](Docs/1_new_code.png)

### 2 missing module docstring

Old code: line 1 is not a module description

![2 old](Docs/2_old_code.png)

Fixed code: line 1 is now a desciption of the module

![2 new](Docs/2_new_code.png)

### 3 module name "GUI_main.py" doesn't conform to snake_case naming confention

We renamend GUI_main.py to gui.py

### 4 missing function or method doscstring

Old code: 

![4 old](Docs/4_old_code.png)

Fixed code: 

![4 new](Docs/4_new_code.png)

### 5 missing function or method doscstring

Old code: 

![5 old](Docs/5_old_code.png)

Fixed code: 

![5 new](Docs/5_new_code.png)

### 6 missing function or method doscstring

Old code: 

![6 old](Docs/6_old_code.png)

Fixed code: 

![6 new](Docs/6_new_code.png)

### 7 unnecessary-lambda-assignment

Old code: 

![7 old](Docs/7_old_code.png)

Fixed code: 

![7 new](Docs/7_new_code.png)

### 8 Wrong import order

Old code: 

![8 old](Docs/8_old_code.png)

Fixed code: 

![8 new](Docs/8_new_code.png)

### 9 Wrong import order

We can discared this change, because we noticed we don't  need the os library.

## Second fixes

We reruned pylint and this was the reslust:

![second plyint output](docs/PYLINT_output_after_first_fix.png)

### 1 Final new line missing

Old code:

![2.1 old](docs/2.1_old_code.png)

Fixed code:

![2.1 new code](docs/2.1_new_code.png)

### Third fixes

![third pylint output](docs/PYLINT_output_after_second_fix.png)