# Recallr
Recallr is a web application designed to help users make a decks and flashcards for studying. It allows users to create, manage, and review flashcards efficiently.

- What does it do?
  Recallr allows users to CRUD (create, read, update, delete) decks of flashcards.
  also it allows users to create cards on their decks.
  each card has a question and an answer and can be CRUDed as well.

  The platform also alows users to do quizzes to see how well they remember their flashcards.
  results of quizzes can be reviewed by users to see the question they got wrong and the ones they got right.


- What is the "new feature" which you have implemented that we haven't seen before?
<!-- - [ ] The new feature is the ability to create flashcards with AI assistance from a piece of text.  -->


## Prerequisites

Did you add any additional modules that someone needs to install (for instance anything in Python that you `pip install-ed`)?  List those here (if any).

- sqlite3: for interacting with the SQLite database.


## Project Checklist

- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module. Please provide the name of the module you are using in your app. Module name: `time`, `re`.
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that  `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app.

Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: `app/services/db_interface.py`
  - Line number(s) for the class definition:
    - Line 3 for the class definition: `class DB_interface:`
  - Name of two properties:
    - `db_path`: The file path to the SQLite database.
    - `conn`: The SQLite connection object.
  - Name of two methods:
    - `execute_without_commit`: Executes a SQL query without committing the transaction.
    - `rollback`: Rolls back the current transaction in case of an error.
  - File name and line numbers where the methods are used:
    - File name: `app/services/quiz.py`
    - Line numbers:
      - `execute_without_commit`: Line 190
      - `rollback`: Line 192

- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
  - users can use localstorage to save the time preference for quizzes

- [x] It uses modern JavaScript (for example, let and const rather than var).

- [x] It makes use of the reading and writing to the same file feature.
  - quiz results can be displayed to the users via a text file.

- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least
  - File name: `app/services/quiz.py`
  - Line numbers: Line 179: `if len(quiz["cards"]) < constants.CARDS_PER_QUIZ:`

## How to run the app

1. Clone the repository.
```bash
git clone https://github.com/walidkhamees/Recallr.git
```

2. Install the required packages.
```bash
pip install -r requirements.txt
```

3. Create a .env file with the following content:
```bash
echo "FLASK_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env
```

4. Run the app.
```bash
python run.py
```

5. Open the app in your browser.
```bash
http://127.0.0.1:5000
```

