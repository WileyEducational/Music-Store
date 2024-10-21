# Introduction

Welcome to the readme file for the MusicStore-project!

This project focusses on creating an application that can securely save files from music creators and protect them against copyright infringement.
<br>
Firstly, this project deviates from the initial design (Miah et al., 2024). To make for more maintainable software the projects is based on the MVC pattern (Syromiatnikov and Weyns, 2014). This also enable the majority of the code being reusable if switching to a different technology (e.g. web based) instead of CLI, just having to change the view classes.
<br>
The majority of the functionalities of the classes from the class diagram from the initial design (Miah et al., 2024) have been moved to the controller classes. When this is the case there is a comment added to the code referring to the original method of the class diagram. Next to that a lot of businesslogic has been extracted to dedicated utility classes, such as the FileHandler and Checksum classes.
<br>
Nextly, there is a deviation from certain domain model classes. To simplify the design and the software account no longer has the derived classes "User" and "Administrator" but instead has the role attribute based on an enumeration. Considering the functionalities in charge of authorization are mostly employed in the musicartefact_controller, there was no need to overcomplicate the software with derived classes that have no real added value. This is also true for the MusicArtefact class, where there was no distinction between the different types of MusicArtefact thus resulting in the use of an enumeration instead of inheritance.
<br>
These are all the changes made to the software going from the initial design, the next session will focus on installation followed by running instructions.

# Installation(from zip)
1. This zip will contain a premade virtualenv called venv this has all dependecies installed and can be used, if this does not work please refer to installation(clean venv). <br>
2. Open a terminal <br>
3. Navigate to the project folder, just one level above the vent <br>
4. Activate the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)<br>
5. This zip already has a database attached, alternatively if no database is present one can be created via the command ```python createdb```
6. Run the project using ```python main.py```
Optionally you can run the project tests via the command: ```pytest```

# Installation(clean venv)
1. This zip will contain a premade virtualenv called venv this has all dependecies installed and can be used, this instruction focusses on creating a clean venv. <br>
2. Open a terminal <br>
3. Navigate to the project folder <br>
4. Create a virtualenv by using ```python virtualenv venv```<br>
5. Activate the virtualenv by using ```source ./venv/bin/activate``` (note: this command is different for windows machines)<br>
6. This zip already has a database attached, alternatively if no database is present one can be created via the command ```python createdb```
7. Run the project using ```python main.py```
Optionally you can run the project tests via the command: ```pytest```

# References
Miah, A., Youness, M., Koster, A. and Finch, W. (2024) Development Team Project: Design Document.
<br><br>
Syromiatnikov, A. and Weyns, D. (2014) ‘A journey through the land of model-view-design patterns’, in 2014 IEEE/IFIP Conference on Software Architecture. IEEE, pp. 21–30. Available at: https://ieeexplore.ieee.org/abstract/document/6827095/ (Accessed: 11 June 2024).

