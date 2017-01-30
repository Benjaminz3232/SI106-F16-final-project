# SI106-F16-final-project
University of Michigan SI106 final project by Benjamin Zeffer

This code is meant to mash two google APIs (Google Finance News and Google Finance) in order to create a stock checking program. The
program automatically stores the data in caches. The program has two inputs: exchange and stock symbol. Once the user enters these, the
program will return a list containing common stock figures (such as dividend, yield, stock price, percent change, etc), and then the top
new sources related to these stocks will be returned as wel. All of this is returned through the command window in a user-friendly format.
The code also utilizes two lists: a list of positive words and negative words, in order to compile an "emotion score" which is used to
determine a prediction for the stock's path (increasing or decreasing).
