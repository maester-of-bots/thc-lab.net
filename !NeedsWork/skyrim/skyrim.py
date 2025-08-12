import csv
import json
from random import randint, choice
# import pickle
# import nltk
# from nltk.util import ngrams


class skyrim:
    def __init__(self):
        try:
            self.data = self.importJSON()
        except:
            data = self.importCSV()
            self.dumpJSON(data)
            self.data = self.importJSON()
    def randomQuote(self):
        character = choice(list(self.data.keys()))
        num2 = randint(0,len(self.data[character]))
        try:
            line = self.data[character][num2]['line']
        except:
            line = self.data[character][num2-1]['line']
        return character,line
    def getQuote(self,character):
        num = randint(0,len(self.data[character]))
        try:
            line = self.data[character][num]['line']
        except:
            line = self.data[character][num-1]['line']
        return line

    def list(self):
        tempdata = {}
        for key in self.data.keys():
            tempdata[key] = len(self.data[key])
        return tempdata
    def importJSON(self,filename='data/lines.json'):
        read = open(filename, encoding="utf8")
        data = json.load(read)
        return data
    def dumpJSON(self,data,filename='data/lines.json'):
        with open(filename, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
    def importCSV(self,filename='lines_trimmed.csv'):
        data = {}
        csvf =  open(filename, encoding='utf-8')
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['name']
            del rows['name']
            try:
                data[key].append(rows)
            except:
                data[key] = [rows]
        return data
    def forVoices(self,filename='lines_trimmed.csv'):
        data = {}
        csvf = open(filename, encoding='utf-8')
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['name']
            try:
                data[key].append(rows['line'])
            except:
                data[key] = [rows['line']]
        return data
    def analyze_dict(self,brain,character):
        quote_gen = {}
        for sentence in brain:
            token = nltk.word_tokenize(sentence)
            for w1, w2, w3 in ngrams(token, 3, pad_left=True, pad_right=True):
                self.PInsert(quote_gen, (w1, w2), w3)
                quote_gen[(w1, w2)][w3] += 1
        for w1_w2 in quote_gen:
            total_count = float(sum(quote_gen[w1_w2].values()))
            for w3 in quote_gen[w1_w2]:
                quote_gen[w1_w2][w3] /= total_count
        pickle.dump(quote_gen, open(character + '.pkl', 'wb'))
    # Still don't understand
    def PInsert(self, dictionary, key, value):
        if key not in dictionary:
            dictionary[key] = {}
        if value not in dictionary[key]:
            dictionary[key][value] = 0