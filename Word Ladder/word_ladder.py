from random_word import RandomWords
import enchant 
import sys
import asyncio

# Generate 2 words of given length. Need to figure out a way to generate simpler words.
def generate_words(length):
    wordGenerator = RandomWords()
    print(length)
    word1 = wordGenerator.get_random_word(hasDictionaryDef='true', includePartOfSpeech='noun,adjective,verb', minCorpusCount=10000, excludePartOfSpeech='Pronoun,name', minLength=length, maxLength=length)
    word2 = wordGenerator.get_random_word(hasDictionaryDef='true', includePartOfSpeech='noun,adjective,verb', minCorpusCount=10000, excludePartOfSpeech='Pronoun,name', minLength=length, maxLength=length)
    print(word1, word2)
    return (word1,word2)

# Function to check whether a string is a number or not.
def is_number(i):
    try: 
        int(i)
        return True
    except ValueError:
        return False 

# given two strings of equal length, find all paths of the same length within the rules of word ladder
"""
Start with word1 and word2
Make sure they're equal length
start with word1 -> change one letter at a time, check if its a word
Add to queue of words to branch from next
"""


async def find_path(word1, word2):
    print(word1,word2)
    dictionary = enchant.Dict("en_US")
    path = []
    queue = []
    used_words = []
    used_words.append(word1)
    queue.append([word1])
    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    # only solves for one path. Need to improve to show all paths (with same length). Additionally need to improve the performance of the algorithm.
    count = 1
    if len(word1) == len(word2):
        while len(queue) != 0:
            count += 1
            current_path = queue.pop(0)
            length = len(current_path)
            current_word = current_path[length-1]
            for i in range(0,len(current_word)):
                for char in alphabet:
                    temp_word = current_word
                    temp_list = list(temp_word)
                    temp_list[i] = char
                    temp_word = "".join(temp_list)
                    if dictionary.check(temp_word) and temp_word not in used_words:
                        temp_path = current_path.copy()
                        temp_path.append(temp_word)
                        used_words.append(temp_word)
                        if temp_word == word2:
                            print('solved after', count)
                            print(temp_path) 
                            # condition should be changed to only consider paths with lower length now.
                            return "->".join(temp_path)
                        if temp_path not in queue:
                            queue.append(temp_path)
    else:
        print('words need to be equal length')
    return "Not solved"