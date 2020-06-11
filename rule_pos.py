import tag_list

# Reverse engineer the given word to tag_list file namely "english_pos_brown.txt"
# Create a dictionary to map words to a list of all of its possible tags
# This preprocessing is done to make further tasks easier

handle = open('english_pos_brown.txt')
tagged_words = []
for line in handle:
	line = line.strip()
	line = line[1:]
	line = line[:-1]

	data = []

	data.append(line[2 : line.find(',') - 1])
	data.append(line[line.find('[') + 1:])
	data[1] = (data[1][:-1]).strip()
	data[1] = data[1].split(',')
	
	modified = []

	for item in data[1]:
		item = item.strip()
		item = item[2:]
		item = item[:-1]
		modified.append(item)

	data[1] = modified

	tagged_words.append(data)

word_to_tag_map = {}

for element in  tagged_words:
	word_to_tag_map[element[0]] = element[1]


string_set = ["She has been absent since last Wednesday.",
"It doesn't matter what excuse he gives me, I can't forgive him.",
"I canceled my appointment because of urgent business.",
"What do you do in Japan?",
"The Handmaid’s Tale is an awesome piece of dystopian fiction.",
"OK. Now what?",
"I was laughed at by everyone.",
"There were people everywhere, covering the roads along the route from the BJP headquarters to the Smriti Sthal from side to side, with security personnel maintaining strict vigil to ensure that nothing goes wrong."]

print("All possible tags for a particular word in the training set based on first occurence in corpus:\n")
for sentence in string_set:
	words = sentence.split()
	for word in words:
		if word[-1].isalpha() == False:
			word = word[:-1]

		flag = 1

		if word in word_to_tag_map.keys():
			print(word, word_to_tag_map[word])

		elif word.lower() in word_to_tag_map.keys():
			print(word, word_to_tag_map[word.lower()])

		else:
			print(word, "NOT_FOUND")

'''
Brill's Tagger:
The tagger initially tags by assigning each word its most likely tag, estimated by examining a large tagged corpus, without regard to context.
'''

# The List of tags for a particular word in the Brown Corpus is assigned in the decreasing order of frequencies of that word having that particular tag.
# We will be following an approach very similar to the Brill's Tagger.
# At the first stage, we should ideally assign to each word, the tag for that word with the highest frequency of occurence i.e the first tag in the list of Brown Corpus tags for that word.
# Since, we do not have frequencies available, The tag assigned to the first occurence of a word in the corpus will be out default tag for a word and then we apply methods of disambiguation.

sentence_tag = []

for sentence in string_set:
	word_tag = []
	words = sentence.split()
	for word in words:
		if word[-1].isalpha() == False:
			word = word[:-1]

		if word in word_to_tag_map.keys():
			word_tag.append((word, word_to_tag_map[word][0]))

		elif word.lower() in word_to_tag_map.keys():
			word_tag.append((word, word_to_tag_map[word.lower()][0]))

		else:
			word_tag.append((word, "NULL"))

	sentence_tag.append(word_tag);

print("\nSentences with their words mapped to the default tags with their meanings")
print("(Using the official Brown tagset)\n")

for sentence in sentence_tag:
	for item in sentence:
		print((item[0], item[1], tag_list.get_meaning(item[1]).strip()), " ", flush=False)
	print()

'''
Wrongly tagged :

"It doesn't matter" - "matter" should be a verb
"I canceled..." - "cancelled" should be a VBD and not VBN
NOT_FOUND tags becomes Proper Nouns and we check for 's or s' to assign corresponding $ tags
"to Smriti Sthal" - "to" should be IN and not TO
Some Proper Nouns listed as NN


Disambiguation Rules:
1. DO* before NN -> VB
2. VBN -> VBD unless [HV, HVZ, HVD, HVN, HVG] VBN
3.   VBD -> VBN if [HV, HVZ, HVD, HVN, HVG] VBD
4. NULL -> NP, if ends with 's or s' : consider NP$

5. TO -> IN unless "[VB(#, D, G, N, P, Z)] to" OR "to [VB(#, D, G, N, P, Z)]"
# JJ -> NN if [VB(#, D, G, N, P, Z)] JJ - Cancel Rule

# Words with First letter Capitalized -> NP unless first word in the sentence. - Cancel Rule - handled by Rule 3
6. NN with first letter capitalized is NP
'''

# Applying disambiguation rules to the training data

print("The final tags assigned to the training data elements after applying all the disambiguation rules:\n")

for sentence in sentence_tag:
	word_id = -1
	for word in sentence:
		changed = 0

		word_id = word_id + 1
		default_tag = word[1]

		# Proposed Rule 1:
		if word_id > 0 and sentence[word_id - 1][1].startswith('DO') and word[1] == 'NN':
			word = (word[0], 'VB')
			changed = 1

		# Proposed Rule 2:
		elif word_id > 0 and word[1] == 'VBN' and not sentence[word_id - 1][1].startswith('HV'):
			word = (word[0], 'VBD')
			changed = 1

		elif word_id > 0 and word[1] == 'VBD' and sentence[word_id - 1][1].startswith('HV'):
			word = (word[0], 'VBN')
			changed = 1

		# Proposed Rule 3:
		elif word[1] == 'NULL':
			if word[0].endswith("\'s") or word[0].endswith("s\'") or word[0].endswith("’s") or word[0].endswith("s’"):
				if word[:-2] in word_to_tag_map.keys():
					new_tag = word_to_tag_map[word[:-2]] + "$"
				else:
					new_tag = "NP$"

			else:
				new_tag = "NP"
			word = (word[0], new_tag)
			changed = 1

		# Proposed Rule 5:
		elif word[1] == "TO":
			if not ( word_id + 1 < len(sentence) and sentence[word_id + 1][1].startswith('VB') ) or ( word_id > 0 and sentence[word_id - 1][1].startswith('VB') ):
				word = (word[0], 'IN')
				changed = 1


		# Invalid Rule

		# if word[1] == "JJ":
		# 	if word_id > 0 and sentence[word_id - 1][1].startswith('VB'):
		# 		word = (word[0], 'NN')

		# Invalid Rule
		# elif (word[0][0].isupper()) and (word_id > 0):
		# 		print(word)
		# 	if word[1].endswith('\'s') or word[1].endswith('\'s'):
		# 		word = (word[0], 'NP$')
		# 	else:
		# 		word = (word[0], 'NP')
		# 	changed = 1

		# Proposed Rule 6:
		elif (word[0][0].isupper()) and (word_id > 0) and word[1].startswith("NN"):
			#print(word)
			word = (word[0], 'NP' + word[1][2:])
			changed = 1


		#if changed == 1:
		print(word)
	print()


# Test Data Processing:

test_data = "During a visit to the Cleveland Indians, Beane meets Peter Brand, a young Yale economics graduate with radical ideas about how to assess player value. Beane tests Brand's theory by asking whether he would have drafted Beane out of high school. Though scouts considered Beane hugely promising, his career in the Major Leagues was disappointing. Brand admits that, based on his method of assessing player value, he would not have drafted him until the ninth round. Impressed, Beane hires Brand as his assistant manager."
test_sentences = test_data.split('.')
# Since all sentences in the given text end with a fullstop

sentence_set = []

print("Displaying all possible tags for a word in the testing set:\n")

for sentence in test_sentences:
	words = []
	for word in sentence.split():
		if word[-1].isalpha() == False:
			word = word[:-1]

		if word in word_to_tag_map.keys():
			words.append((word, word_to_tag_map[word][0]))
			print((word, word_to_tag_map[word]))

		elif word.lower() in word_to_tag_map.keys():
			words.append((word, word_to_tag_map[word.lower()][0]))
			print((word, word_to_tag_map[word.lower()]))

		else:
			words.append((word, "NULL"))
			print((word, "NULL"))
	print()
	if words != []:
		sentence_set.append(words)
		#print(words)


print("\nApplying same rules to Test Data and printing results:\n")

for sentence in sentence_set:
	word_id = -1
	for word in sentence:
		changed = 0

		word_id = word_id + 1
		default_tag = word[1]

		# Rule 1:
		if word_id > 0 and sentence[word_id - 1][1].startswith('DO') and word[1] == 'NN':
			word = (word[0], 'VB')
			changed = 1

		# Rule 2:
		elif word_id > 0 and word[1] == 'VBN' and not sentence[word_id - 1][1].startswith('HV'):
			word = (word[0], 'VBD')
			changed = 1

		elif word_id > 0 and word[1] == 'VBD' and sentence[word_id - 1][1].startswith('HV'):
			word = (word[0], 'VBN')
			changed = 1

		# Rule 3:
		elif word[1] == 'NULL':
			if word[0].endswith("\'s") or word[0].endswith("s\'") or word[0].endswith("’s") or word[0].endswith("s’"):
				if word[:-2] in word_to_tag_map.keys():
					new_tag = word_to_tag_map[word[:-2]] + "$"
				else:
					new_tag = "NP$"

			else:
				new_tag = "NP"
			word = (word[0], new_tag)
			changed = 1

		# Rule 5:
		elif word[1] == "TO":
			if not ( word_id + 1 < len(sentence) and sentence[word_id + 1][1].startswith('VB') ) or ( word_id > 0 and sentence[word_id - 1][1].startswith('VB') ):
				word = (word[0], 'IN')
				changed = 1

		# Rule 6:
		elif (word[0][0].isupper()) and (word_id > 0) and word[1].startswith("NN"):
			word = (word[0], 'NP' + word[1][2:])
			changed = 1

		print((word[0], word[1]))
	print()




'''
Issues in Test:
1. 'how to assess player value' : how should be WRB and not QL
Rule : if WRB tag is available for a word and the next word is not a JJ or NN, change the tag to WRB

2.'tests theory by asking' : tests should be VBZ and not NNS
Rule : if VBZ tag is available for a word and the next word is a NN[*], change tag to VBZ

3. 'assistant manager' : 'assistant' should be JJ and not NN
Rule : Change tag from NN to JJ if JJ is an available tag and the tag of the next word is NN

4. 'hugely promising' : The problem arised since the Brown Dataset did not have "hugely" as a separate word and hence it got the NULL tag. By default, I assigned NNP tags to NULL values and hence this problem arose.
Rule : For a word with a NULL tag, check if it ends with "ly" and if it is not the first word in the sentence, check if the first letter is lower case. If the above checks hold, Assign to the word the RB tag for adverbs.

- These are the only 4 discrepancies found. And 3 new rules have been assigned to deal with these.
Note that these scenarios were not encountered in the the testing data and hence could not be taken care of.

Another issue lies in determining whether the first word in a sentence starting with a capitalized letter is an NNP or not.
Suppose the word also exists as a NN, then we have to look at the discourse level to analyze whether it is an NNP or an NN.
Note that this is precisely the problem of named entity recognition which is beyond the scope of POS tagging and rule based disambiguation.
'''
