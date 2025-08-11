Idea: Make a flashcards app.

# TODO

- [x] make the logo point to /
- [x] make the deck header uniform across all pages

- [ ] Implement quiz feature
    - [x] route the user to result page for quiz
    - [x] store user `answer` to the database `quiz_card`
    - [x] store quiz `status` in the database `quiz`
        - [ ] remove `status` from quiz and relay on quiz_card table.
    - [x] Fix
        - [ ] User can see the quiz result even if the quiz is not over.
        - [ ] Also happens in the all results page.


- [x] all results page

- [x] Implement card update feature

- [ ] Implement deck update feature
- [ ] Implement deck delete feature

- [ ] Implement authentication with Sessions

# Some Missing Features

- No authentication
- No user profiles

# Decks

- Each deck has a name.
- Each deck has a list of cards.
- Each deck is a simple text file in the following format:

```txt
Id`Question`Answer`LastTimeAnsweredEpoch`CorrectBoolean
```

Quiz
```txt
QuizTime`CardIds`Answered
```

- Id(int): The id of the card.
- Questions(string): The question.
- Answer(string): The answer.
- LastTimeAnsweredEpoch(int): The epoch time when the
user answered the question.
- CorrectBoolean(int): 1 if the user got the answer right, 0 if the user
got the answer wrong.

# Cards

- Each card has a front and a back.
- The front is a question and the back is the answer.
- Each cards is stored in text file in the following format:


# Frontend

- The user can create a new deck.
- CRUD (create, read, update, delete) Decks.
- In each deck the user can CRUD (create, read, update, delete) cards.
- The user can start a quiz.
    1. 10 cards are randomly selected from the deck.
    2. There is a time for each card to be answered.
    3. User can that got the answer right.
    4. if the timer runs out, the user is assumed to be wrong.
    5. whether the user is right or wrong,
    the user can see the correct answer.
    6. After the quiz is over, the user can see the results.
