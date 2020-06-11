# Brill's Tagger Illustration

### An Implementation of a Modular Brill's Tagger with Analysis on Formulation of Disambiguation Schemes

#### Tasks

1. List all possible tags for each word in the development data by looking up provided 'english_pos_brown.txt'

2. Disambiguate tags for each word manually, considering context and lexical properties & make rules in the process

3. Tag the testing data using the formulated disambiguation rules

4. Analyze annotation of the testing data, reformalize the rule-set

<p align="justify">
The list of tags for a particular word in the Brown Corpus is maintained in the decreasing order of frequency of the word with that particular tag. At the first stage, we should ideally assign to each word, the tag for that word with the highest frequency of occurence. Since, we do not have frequencies available as part of the task, the tag assigned to the first occurence of a word in the corpus will be the default tag for the word and then we shall then apply methods of disambiguation.
</p>

---

#### By analyzing sentences with their words mapped to their default tags, we find the following discrepancies:

- "It doesn't matter": "matter" should be a verb

- "I canceled...": "cancelled" should be a VBD and not VBN

- NOT_FOUND tags becomes Proper Nouns and we check for 's or s' to assign corresponding $ tags

- "to Smriti Sthal": "to" should be IN and not TO

- Some Proper Nouns listed as NN

#### Disambiguation Rules:

1. NN -> VB if DO* before NN

2. VBN -> VBD unless \[HV, HVZ, HVD, HVN, HVG\] VBN

3. VBD -> VBN if \[HV, HVZ, HVD, HVN, HVG\] VBD

4. NULL -> NP, if ends with 's or s' : consider NP$

5. TO -> IN unless "\[VB(#, D, G, N, P, Z)\] to" OR "to \[VB(#, D, G, N, P, Z)\]"

6. NN with first letter capitalized is NP

#### The final tagging results by applying the handcrafted rules to the testing data have been provided.

---

#### Observations from System Tagged Test Dataset and Newly Proposed Rules:

1. 'how to assess player value' : "how" should be WRB and not QL

	Rule 7: if WRB tag is available for a word and the next word is not a JJ or NN, change the tag to WRB

2. 'tests theory by asking' : "tests" should be VBZ and not NNS

	Rule 8: if VB* tag is available for a word and the next word is a NN*, change tag to VB*

3. 'assistant manager' : 'assistant' should be JJ and not NN

	Rule 9: Change tag from NN to JJ if JJ is an available tag and the tag of the next word is NN*

4. 'hugely promising' : The problem arised since the Brown Dataset did not have "hugely" as a separate word and hence it got the NULL tag. By default, I assigned NNP tags to NULL values and hence this problem arose.

	Rule 10: For a word with a NULL tag, check if it ends with "ly" and if it is not the first word in the sentence, check if the first letter is lower case. If the above checks hold, Assign to the word the RB tag for adverbs.

- These are the only 4 discrepancies found. And 4 new rules have been assigned to deal with these.

- Note that these scenarios were not encountered in the the training data and hence could not be taken care of.

- Another issue lies in determining whether the first word in a sentence starting with a capitalized letter is an NNP or not.

- Suppose the word also exists as a NN, then we have to look at the discourse level to analyze whether it is an NNP or an NN. This is precisely the problem of Named Entity Recognition which is beyond the scope of our simple rule based disambiguation scheme.

---

#### References

1. [A Simple Rule-Based Part of Speech Tagger](https://www.aclweb.org/anthology/A92-1021/)

2. [CLAWS Word Tagging System](http://ucrel.lancs.ac.uk/papers/ClawsWordTaggingSystemRG87.pdf)

---
