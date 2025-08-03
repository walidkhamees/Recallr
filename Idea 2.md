Idea: Make a flashcards app.


- No authentication

- Decks
    - Each deck has a name and a description.
    - Each deck has a list of cards.
    - Each deck is represented by a directory in the `decks` directory.

- Cards
    - Each card has a front and a back.
    - The front is a question and the back is the answer.
    - Each cards is stored in text file in the following format:

```txt
Question`Answer`LastTimeAnsweredEpoch`CorrectBoolean
```
- Questions(string): The question.
- Answer(string): The answer.
- LastTimeAnsweredEpoch(int): The epoch time when the
user answered the question.
- CorrectBoolean(int): 1 if the user got the answer right,
0 if the user got the answer wrong.

- Frontend
    - The user can create a new deck.
    - In each deck the user can CRUD (create, read, update, delete) cards.
    - The user can start a quiz.
        1. 10 cards are randomly selected from the deck.
        2. There is a time for each card to be answered.
        3. User can that got the answer right.
        4. if the timer runs out, the user is assumed to be wrong.
        5. whether the user is right or wrong,
        the user can see the correct answer.
        6. After the quiz is over, the user can see the results.

