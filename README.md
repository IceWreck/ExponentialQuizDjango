# Exponential Quiz
Online quiz app with exponential scoring. Built for a CCS-TIET event.  

![exponential-quiz](screenshots/abifog-exponential-quiz-4.png)

Credits to [SIBTC](https://github.com/sibtc/django-multiple-user-types-example/) for the base quiz layout and mechanism.

## Running the Project Locally

First, clone the repository to your local machine:


Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.

## Screenshots

![exponential-quiz](screenshots/abifog-exponential-quiz-1.png)
![exponential-quiz](screenshots/abifog-exponential-quiz-2.png)
![exponential-quiz](screenshots/abifog-exponential-quiz-3.png)

## License

The source code is released under the [MIT License](https://github.com/IceWreck/ExponentialQuizDjango/blob/master/LICENSE).
