# Exponential Quiz
Online quiz app with exponential scoring. Built for a CCS-TIET event.

![exponential-quiz](screenshots/abifog-exponential-quiz-4.png)

## Features

* Standard Quiz Features
* Exponential Scoring and negative marking
* Know your score after each answer submission
* User auth for both quiz makers and students
* Images/Code/Text in questions.
* Anti cheat

## Running Locally

Install the requirements:

In a python3virtualenv,
```bash
pip install -r requirements.txt
```

In exponential_quiz/settings.py commment out these two lines
```
import django_heroku
.
.
.
.
django_heroku.settings(locals())
```



Link to the database by setting the DATABASE_URL environment variable. Then run:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

## Notes
* The contents of one option of a question should be 'Skip' if you want a question to be skippable.
* Basic html markup can be inserted into the questions for code, images, formatting, etc.

## Other Screenshots

![exponential-quiz](screenshots/abifog-exponential-quiz-1.png)
![exponential-quiz](screenshots/abifog-exponential-quiz-2.png)
![exponential-quiz](screenshots/abifog-exponential-quiz-3.png)


## Credits:
* [SIBTC](https://github.com/sibtc/django-multiple-user-types-example/) for the base quiz layout and mechanism.
* [StartBootstrap](https://startbootstrap.com/themes/sb-admin-2/) for the css template.

## License
The source code is released under the [MIT License](https://github.com/IceWreck/ExponentialQuizDjango/blob/master/LICENSE).
