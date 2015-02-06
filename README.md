Playlist Manager
===
Playlist Manager is a web app that allows users to create/manage playlists of songs. The Search functionality is powered by TinySong API for now.

Installation
---
1. Install required dependencies (in vritualenv) `pip install -r requirements.txt`
2. Run `python manage.py migrate` to migrate all models
3. Create local.py in the 'manager' directory of the project with the following settings

``` python
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '' # Random String

DEBUG = False # Set to False for production server 
ADMINS = (
    ('name', 'email'),
)
ALLOWED_HOSTS = [
    '.example.com',
    '.example.com.',
]

# Database settings, see Django documentation for more information
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Setup
---
1. Go to your admin panel website.com/admin
2. Add your website to the SITES admin category
3. Add openid credentials to Social Account Apps to enable this form of authentication
4. Full list of post-installation instructions and authentication settings go  [here](http://django-allauth.readthedocs.org/en/latest/installation.html)