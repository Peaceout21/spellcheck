# Spell check


## Idea of spell check

when there are multiple words present,we assume that the words are independently distributed. 
A word with rank n in the list of words has a probability of 1/(nlogN) . N is the total no of words in the dictionary.
The most likely sentence is where there's a max of product of the probability of each word.
The cost function would be the inverse of the probability as mentioned above and we would calculate the minimum of the word cost function.
we also use a standard spell checker through the idea presented @ https://norvig.com/spell-correct.html


### Usage
```
curl -X GET http://0.0.0.0:8880//spellCorrect -d query="th e earthis round"

response:
{
  "answer": [
    "The earth is round",
    "theearthisround"
  ]
}
```
The index 0 response uses the probability model and the index 1 uses the spell checker
And repeat
