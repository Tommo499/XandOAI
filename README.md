# XandOAI
A python-based naughts and crosses engine, which learns through a monte-carlo tree search

Monte-Carlo formula based off [https://en.wikipedia.org/wiki/Monte_Carlo_tree_search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)

I might try to remake it in a faster language, but that will be later

# Running
1. Download the files
2. If you want to just play a game, run ```python3 ./play.py```, since the default data.db has some training data
3. If you want to train your own model, delete the data.db file, then run ```python3 ./Training.py```, which will make the model play against itself 1000 times then record the results.

Initially, the model will choose random moves to play, but if you let it train, it will get better.
