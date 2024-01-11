# SCHOOL MANAGMENT SYSTEM
#### Video Demo:  https://youtu.be/HmZxYIQaomw
#### Short description:
Web application SCHOOL MANAGMENT SYSTEM is designed for managing small offline **schools** with a number of options for **students** and **teachers**. 

## Distinctiveness and Complexity
## Complexity
The application is complex from the following points of view.
* Users receive **different roles** (teacher vs. student) and depending on that *users have access to different functions and options*. Every page of the application behaves *differently* for teachers and for students (and mostly differently depending on whether the information is related to the user herself/himself or to the other user - even within the same role). *The menu is different as well*. (And of course not authenticated users have very limited access to the application.) So, the **structure** of the application is much more diverse than that of any course project.
* *Pages not only react to the user's role but also to the user's actions on the page and to the changing (or available) data in the database*. The level of **interactiveness** is higher than that of course projects. For example, the page where students can enroll into the courses will automatically hide the course if the number of enrolled students became equal to the maximum number of students. This page displays dates of course start and end but if there is no such information in the database the page informs that the dates are flexible. See detailed description below.
* The **range of options** for users is also wider in comparison with course projects. General options are of course common - users can *add*, *delete* and *edit* information - but there is a number of instances of every option. Also, users can *sort* results on the page. In total, the application has **13** javascripts and **2** forms in views.py (I do not count forms for registration and login).
* The **database** of application has more complex structure as well (**6** models in total).
* Due to more complex structure and inner relationships between pages and tables in the database, I had to pay **more attention to possible errors**, to **possible inconsistencies** (like one page does not allow some action but other page allows) and to **possible inappopriate user's behaviour** (like submitting empty forms or accidental removing information).

### Distinctiveness
This application is distinct from course projects in terms of:
* Its **purpose** (*school managment*) and **content** (*primary interaction between teachers and students*). Students can: choose their courses, enroll into them or leave them; view their, other students' and teachers' profiles. Teachers can: create, edit or delete courses, open them for registration, close them; add, edit and remove course groups; add and remove students from groups; view their, their colleagues' and students' profiles.
* **Level of interactivity** (as stated above);
* Implemented **features and components**. I did not use in my course projects but used in this application:
  - *Bootstrap modal and card*
  - *Django roles*
  - *Javascript for processing forms with drop-down lists*
  - *sorting the results on the page by users* (with 4 options) (including ordering by a field in a different model; also I had to solve the problem of duplicated rows in the results)
  - some new for me *CSS styles*


## Technologies
Project is created with:
* django
* python 3
* javascript
* bootstrap 5
* html
* css


## Content (html pages)
Web application has the following structure for three groups of users. The same html pages are different for those three groups (and sometimes are different for users within the same group).
### For unauthorized users:
* **index.html**: welcome page
* **register.html** (I used template and code from Network project but added some fields and updated the code)
* **login.html** (borrowed from Network project)
### For teachers:
* **index.html**: list of basic options
* **courses.html** (*Your courses* in the menu):
  - a form for *creating a new course* (all fields - title, level, hours, description - are required)
  - *list of current courses* offered by user; courses represented as cards, every card displays information about the course and offers 3 options: *go to the course page*, *edit information about the course* and *remove the course*; *all remove buttons require confirmation*
* **course.html**:
  - *course description* with 2 options: *edit information* (same as on the courses page) and *open the course for registration* or *close the course* (*close* means that new students cannot enroll into the course by themselves)
    * user can close any her/his course
    * to open the course for registration user is only required to choose groups (if there are no groups yet user receives notification about it), all other fields are optional (registration start and end dates; course start and end dates; min and max number of students in a group); user is informed that after the course is opened user can only add new groups into it but no other editing is allowed
  - *current groups*: list of current groups (if there no groups the user sees the message *"No groups so far"*)
    * user can *remove* a particular group (but only if there are no students in it; if there are students in the group user sees notification *"You cannot remove group with students! Remove students first"*)
    * user can *add* a group (only title is required; if the title is empty or the group with the provided title already exists inside the course, the group is not added into the database; but groups with the same title are allowed if they belong to different courses)
    * titles of groups are links: user can *go to the page of a group*
  - if user somehow opened the other teacher's course she/he will be able to see only course description (not groups) without any option; in this case user also sees who is the instructor (this information is not displayed for the author of the course) and can go to her/his profile page
* **group.html**:
  - *course description* with option to *go to the course page* (any group can only exist inside a course)
  - group title; user can *edit* the title (with restrictions as on the course<id>.html page)
  - students (if there no students user sees the message *"No students so far"*)
    * user can *remove* students from the group
    * user can *add* students into the group from the list of available (i.e. not enrolled into this course) students; if all students from the database are added, user sees message *"No available students"* instead of add button
    * students' names and last names are links: user can visit student's profile
  - if user somehow opened the other teacher's group page she/he will be able to see only course description (not groups) without any option, without link to the course and with a message *"You can view only your own groups"*; in this case user also sees who is the instructor (this information is not displayed for the author of the course) and can go to her/his profile page
* **stprofile.html** (Student profile): student's first and last name and student's groups (title of the group, course, level, instructor and link to the instructor profile page)

* **enroll.html** (*Open registration* in the menu): information about all courses opened for registration
  - if the course is user's course, user can *add groups* into it
  - user can *sort* the results by *popularity* (i.e. how many students are already enrolled in the course) from the most popular, by *course start date* (in chronological order; courses without start date come last), by *title* and by *instructor's last name*

* **tprofile.html** (*Your profile* in the menu): teacher's first and last name and her/his courses (title, level, hours, link to the course)
  - if teacher visits her/his *own profile*, the page displays information in the second person, but if teacher visits (e.g. from stprofile.html) *colleague's profile* page, the page displays information in the third person

* **logout.html** (borrowed from Network project)


### For students:
* **index.html**: list of basic options (different from those on the teachers index.html, of course)
* **enroll.html** (*Enroll* in the menu): information about all courses opened for registration
  - user can *sort* the results by *popularity* (i.e. how many students are already enrolled in the course) from the most popular, by *course start date* (in chronological order; courses without start date come last), by *title* and by *instructor's last name*  
  - user can *register* for the course (after user registered for the course it disappears from the results; it will appear on the page again if user will leave the group from her/his profile page)
  - the information about the course includes: 
    * *course information*: course title, instructor (link to the instructor page), level, hours, description
    * *groups* (title and the number of students already enrolled); if the number of enrolled students becomes equal to the maximum number of students (if indicated) the group disappears from the page; if the course is open for registration but currently there are no places in any group user sees message *"No available groups right now"* (in this case register button disappears)
    * *dates of opening and closing registration*; if only one date is indicated the other one is omitted (i.e. not shown as None); if both dates are absent there is a message that the registration is open (with no dates)
    * *dates of course start and end* (similar behaviour as that of the dates of opening and closing registration - dates are shown only if they are indicated; if both dates are absent there is a message that the dates are flexible)
    * *min and max number of students* in a group (if there is no such information these fields are not shown at all)
* **stprofile.html** (*Your profile* in the menu): students's first and last name, her/his groups (group title; course: course title, level, instructor, link to the instructor page)
  - user can *go to the group page*
  - user can *leave the group*
  - if student visits her/his *own profile*, the page displays information in the second person, but if student visits (e.g. from group.html) *other student's profile* page, the page displays information in the third person
* **tprofile.html** (Professor profile): teacher's first and last name and her/his courses (title, level, hours) (in the third person of course)
* **course.html**: *course description* only; students can also see who is the instructor (this information is not displayed for the author of the course) and can go to her/his profile page
* **group.html**: *course description* (without link to the course), *group title*, *enrolled students*;
  - in course description students can also see who is the *instructor* (this information is not displayed for the author of the course) and can go to her/his profile page
  - students can *visit other students' profiles*
* **logout.html** (borrowed from Network project)


## Scripts (js)
* **add_group_en.js** (enroll.html, for teachers): adds group(s) into the course opened for registration; adding multiple groups is allowed; if user selects no groups she/he receives alert about it
* **add_group.js** (course.html, for teachers): adds group into the course
* **add.js** (group.html, for teachers): adds student into the group
* **clos.js** (course.html, for teachers): after confirmation closes the registration for the course
* **edit_gr.js** (group.html, for teachers): edits group
* **edit.js** (courses.html, for teachers): edits course
* **enrol.js** (enroll.html, for students): registers student for the course
* **ope.js** (course.html, for teachers): opens registration for the course; checks if user has selected groups; adding multiple groups is allowed
* **remove_gr_s.js** (course.html, for teachers): does not allow to remove groups with students
* **remove_gr.js** (course.html, for teachers): after confirmation removes (empty) group
* **remove_stud.js** (group.html, for teachers): after confirmation removes student from the course group
* **remove_stud2.js** (stprofile.html, for students): after confirmation removes user from the course group (= students leaves the group)
* **remove.js** (courses.html, for teachers): after confirmation removes course from the database

## Folders
* directory *final/school/static/school* (javascript files)
* directory *final/school/static/school/img* (images used for the project, all created with AI)
* directory *final/school/templates/school* (html pages)


## Contact
Anzhalika Dubasava, anzhalikad@gmail.com
