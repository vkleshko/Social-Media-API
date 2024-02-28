# Social Media API


The Social Media API allows users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions, writing on DRF.


## Installing using GitHub

Clone the project

```bash
  git clone https://github.com/vkleshko/Social-Media-API
```

Go to the project directory

```bash
  cd social_media_api
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Set up environment variables:

```
  set SECRET_KEY=<your secret key>
```

Migrate Database

```bash
  python manage.py migrate
```

Runserver

```bash
  python manage.py runserver
```


## Getting access

- create user via /api/user/register/
- get token via /api/user/login/
