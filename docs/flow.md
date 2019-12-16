## Start Server
python app.py
## Start mongo
mongod --fork --logpath /var/log/mongodb.log


### This part defines different sections of Application flow
####Registration service
```
    User has to register as admin user.
    create his group.
    add employees to his group.
    Let's add email as authentication for now.
    Each employees are registered by their emailids.
    Employees can then register using their registered email address.
    Password will be the same as emailid for now.
    This is for registration service.
```
####User Service
```
    There are two kinds of users in this system for now.
    One is admin and another is employee.
    Admin has to create a group to add employees.
    Each employees are registered to their groups as members.
        
```
####Attendance service
```
    This service assumes different user types by default.
    Employees submit their attendance by submitting their location, Fingerprint.
    
    
```

