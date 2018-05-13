import random


# Takes an input of a user and returns a markov chain of their dictionary
def start_markov(user):
	dictionary_name = "dictionaries/" + user + "Dictionary.txt"
	
	try:
		f = open(dictionary_name, "r")

	except IOError:
		return dictionary_name + " doesn't exist!"

	word_list = {}

	for line in f:
		current_dictionary = line.split(" ")

		while len(current_dictionary) > 1:
			if current_dictionary[0] not in word_list:
				word_list[current_dictionary[0]] = [current_dictionary[1]]
			else:
				word_list[current_dictionary[0]].append(current_dictionary[1])

			current_dictionary.pop(0)

	word = random.choice(list(word_list.keys()))
	sentence = [word]

	while word in word_list.keys():
		word = random.choice(word_list[word])
		sentence.append(word)

	final_sentence = " ".join(sentence)

	return final_sentence
