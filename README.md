# studybud
A Platform for learners where users can create rooms on different topics, ask queries, share knowledge, etc
Features: create rooms, send messages in rooms, view user profiles, editing own profile, user auth, CRED, APIs, etc

Built using Django, Django Rest Framework, AWS

**Currenly Working On**: FIle Uploads and AWS S3

## APIs
- api/ - REST FRAMEWORK home page
- api/rooms - details of all rooms
- api/rooms/id - details of a particular room

# StudyBuddy
</div>

### Cloning the repository

--> Clone the repository using the command below :
```bash
git clone https://github.com/divanov11/StudyBud.git

```

--> Move into the directory with the project files : 
```bash
cd StudyBud

```

--> Create a virtual environment :
```bash
# install virtualenv first
pip install virtualenv

# Then create a virtual environment
virtualenv envname

```

--> Activate the virtual environment :
```bash
envname\scripts\activate

```

--> Install the requirements :
```bash
pip install -r requirements.txt

```

#

### Running the App

--> To run the App, use :
```bash
python manage.py runserver

```

> ⚠ Then, the development server will be started at http://127.0.0.1:8000/

## Some Resources
Traversy Media : https://www.youtube.com/watch?v=PtQiiknWUcI
Corey Schafer Django Tutorials Playlist : https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
