import re
from spellchecker import SpellChecker
from math import log
from flask import Flask, request
from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource


spell = SpellChecker()

# Build a dictionary, assuming Zipf's law and cost = -math.log(probability).
with open("words-by-frequency.txt") as f:
    words = [line.strip() for line in f.readlines()]
    wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
    maxword = max(len(x) for x in words)

def infer(s):

    # Find the best match for the i first characters and return a pair (match_cost, match_length).
    
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # get the cost
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)
    # get the minimum cost string
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))



app = Flask(__name__)
api = Api(app)

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')


class Predictquestion(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']
        # clean the user's query and make a spell check
        text_cleaned=(re.sub('[^a-zA-Z]+', '', user_query))
        
        if len(text_cleaned)==0:
            op='please enter a word'
            return jsonify(answer=op)
        #### average english word length is 5 .. considered 20 after text 
        elif len(text_cleaned)>20:
            op='word too long'
            return jsonify(answer=op)
            
        else:
            op1=infer(text_cleaned.lower().replace(' ', '').replace(',', '')).capitalize()
            try:
                op2=spell.correction(text_cleaned.lower())
            except:
                op2='NaN'
            output=[op1,op2]
            return jsonify(answer=output)

    
api.add_resource(Predictquestion, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8880,debug=True)
