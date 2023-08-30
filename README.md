# DateApp
 Hello! This repository contains the code for a dating application. Here, I will describe the main parts of the code and its functionality.
 Its a test work, so we have some problems with structure project. Sorry
## How to Use

1. Clone the repository to your local computer.
2. Install the necessary dependencies.
3. Create and configure a virtual environment.
4. Launch the application and enjoy its functionality.
## Dependencies

The list of dependencies can be found in the requirements.txt file.
____
![image](https://github.com/Rolleex/DateApp/assets/26228130/be867514-6626-4e0d-b322-0e65d0029d5c)
____
# Install 
```
pip install -r requirements.txt
```
Dont forget about 
```
python manage.py makemigrations
python manage.py migrate
```
# Settings
Change these settings with yours
____
![image](https://github.com/Rolleex/DateApp/assets/26228130/9cf1cc90-397d-44d5-a40f-ddfa58adc842)
____

## How the Application Works

The application consists of several main components:

### Profile Display View

File: views.py

In this code, the Index(View) class is defined, which handles GET and POST requests for profile display. The get method performs filtering and displays profiles based on filters. The post method implements the "likes" logic and sends notifications in case of mutual "likes."
```
http://127.0.0.1:8000/
```
### User Registration

File: views.py

Here, the user registration process is described. In the register method, POST requests are processed to create a new user and an associated profile. The add_watermark function is also used here to add a watermark to avatars. And authenticate.
```
http://127.0.0.1:8000/register/
```
### API for Registration and Profile Viewing

File: views.py

The RegistrationView and ProfileListAPIView classes provide APIs for user registration and profile viewing. The ProfileListAPIView implements profile filtering.
____
All users
```
http://127.0.0.1:8000/api/list
```
____
Filters
```
http://127.0.0.1:8000/api/list?distance=12312
http://127.0.0.1:8000/api/list?first_name=bibo
http://127.0.0.1:8000/api/list?last_name=Begins
http://127.0.0.1:8000/api/list?gender=Мужчина
```
For filtering gender, pls use 'Мужчина' or 'Женщина'  
____
For register i use Postman
```
http://127.0.0.1:8000/api/clients/create
```
____
![image](https://github.com/Rolleex/DateApp/assets/26228130/fb93dcf3-1aa1-4eaa-95f3-8933960e2d4e)
____
```
http://127.0.0.1:8000/api/clients/{id}/match
```
____
![image](https://github.com/Rolleex/DateApp/assets/26228130/f182e6b6-2fc1-4a02-bb62-08b342010299)
____

### Sending Notifications

File: views.py

The mail_send function sends notifications to users in case of mutual "likes."

### All urls
 
http://127.0.0.1:8000/

http://127.0.0.1:8000/register/

http://127.0.0.1:8000/api/clients/create

http://127.0.0.1:8000/api/clients/{id}/match

http://127.0.0.1:8000/api/list
