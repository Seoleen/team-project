# Initiated by Kelsey Kraus
#
# Contributors: <UPDATE ME!> 
#
# Description: <UPDATE ME!> This file currently contains the instructions for replicating the data cleaning method implemented by CTK 2016.

# NOTE: the suggested approaches below are NOT the only way to complete this task! It is merely given as a starting point. You can choose to do this in a different way if you want, but be sure to comment on your process along the way.

# !!! You may need to run in your Shell: pip install pandas !!!

import os
import pandas 
import re
from pandas import *
import csv

allTweets = []
# with open('pro-who-tweets.csv') as file:
#   allTweets = file.read()
  # print(allTweets)
# allTweets is a string

# -- Preprocessing: -- We don't care about the other data in our .csv. We want to only get the tweet text data in 'content' column.
# -- Suggested approach: -- create a list variable and save the 'content' column of the pro-who-tweets.csv file as your list. Print the length of the list. See here for more: https://www.geeksforgeeks.org/python-read-csv-columns-into-list/

# data = read_csv('pro-who-tweets.csv')
data = open('pro-who-tweets.csv', 'r')
file = csv.DictReader(data) 
for col in file:
  allTweets.append(col['content'])
# print(allTweets)



# === Part 1: Filtering ===

p_list = ['he', 'she', 'they', 'them', 'it', 'her', 'him', 'we', 'us', 'you']

# -- First filter: -- Remove duplicates. - First filter: -- Remove duplicates. 
# -- Suggested approach: -- using your list, convert the list into a dictionary, which will automatically remove duplicates. Then convert your dictionary back into a list. Print the length of the list. https://www.w3schools.com/python/python_howto_remove_duplicates.asp
print("FIRST FILTER**********************************")
allTweets = dict.fromkeys(allTweets)
allTweets = list(allTweets)
print(len(allTweets))




# -- Second filter: -- Remove tweets where the last non-whitespace character before the word 'who' is not a letter or a comma. See Lecture 3 slides for more explanation of this!
# -- Suggested approach: -- Use the list you created as a result of the previous filter. Save the 10 possible pronouns in a list. Create a loop to run through each entry in your list. Use a conditional statement to construct a regular expression match, and save the list elements matching your condition. Print the length of the list.
print("SECOND FILTER**********************************")
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ',']

for elem in allTweets:
    whos = [m.start() for m in re.finditer('who', elem.lower())]
    for num in whos:
        if(num == 0 or num == 1):
            allTweets.remove(elem)
            break
        elif not (elem[num-2] in alphabet):
            allTweets.remove(elem)
            break
print(len(allTweets))

  

# -- Third filter: -- Remove the pattern 'of PRO who'
# -- Suggested approach: -- Create another loop, and another conditional statement using a regular expression from the list you got from the previous filter. This time, save only those that DO NOT match the conditional statement. Print the length of the list.
# print(allTweets[len(allTweets)-1])
print("THIRD FILTER**********************************")
has = False
temp = allTweets.copy()
for tweet in allTweets:
  has = False
  for p in p_list:
    x = re.search("of\s"+p+"\swho", tweet)
    if(x != None):
      has = True
  if(has):
    temp.remove(tweet)
allTweets = temp;
print(len(allTweets))


# -- Fourth filter: -- Remove tweets where the pronoun 'it' preceeds the word 'who' by 2-4 words
# -- Suggested approach: -- Write a regular expression that picks out this pattern. Using the list you generated from the previous filter, use create a loop with a conditional statement that removes this pattern. Print the length of the list. 
print("FOURTH FILTER**********************************")
for tweet in allTweets:
  itty = re.findall("(it's|it)(\s\w*){2,4} who", tweet)
  if len(itty) != 0: 
    allTweets.remove(tweet)
#print(allTweets)
print(len(allTweets))

# -- Fifth filter: -- Remove tweets where 'PRO who' is preceded by the verbs 'ask', 'tell', 'wonder', 'inform', and 'show'.
# -- Suggested approach: --  Save the verbs above into a list. Create a loop that iterates through your pronoun list from above, and removes examples that contain the pattern '[element-from-verb-list] [element-from-PRO-list]'. Print the length of the list.
print("FIFTH FILTER**********************************")

v_list = ["ask", "tell", "wonder", "inform", "show"]
temp2 = allTweets.copy()
for tweet in allTweets:
  has = False
  for v in v_list:
    for p in p_list:
      q = re.search(v+"\s"+p+"\swho", tweet)
      if(q != None):
        has = True
  if(has):
    temp2.remove(tweet)
allTweets = temp2
#print(allTweets)
print(len(allTweets))
#print(allTweets)

# output your list as a .csv or .tsv file.

filtered_allTweets = pandas.DataFrame(allTweets)
filtered_allTweets.to_csv('filtered_allTweet.csv') 




# === Part 2: Uniqueness ===

# -- Instruction: -- You now need to find out whether the tweets you have left are "literary" or "non-literary", according to CTK's classification. I've written a bit of this for you. Modify the block of code below so that it runs with your variable names. You should replace 'tweetList' in the 'for' block with your variable name that holds the final filtered list of 'PRO who' tweets.

# Test variable: contains a short list of test utterances for the pattern "who <word1> <word2>"
tweetList = ['this is a quote: he who shall not be named', 'who among us really', 'jeff is wondering who sings', 'he who shall not be named again', 'but who among us is perfect']

# This evaluates each tweet in TweetList for whether it contains the specified regex search, and whether that regex pattern in a tweet matches exactly to any other tweet in the list. If it does, it is assigned a value True. If it doesn't, it's assigned a value False.
print("----------------------------------------------")
print("PART 2*************************************")


trueFalseList = []
for tweet in allTweets:
   whoPhrase = re.search("who \w+ \w+", tweet)
   if whoPhrase is None:
       trueFalseList.append(False)
   else:
       trueFalseList.append(any(whoPhrase.group(0) in t for t in allTweets))
print(trueFalseList)

# The following takes our two lists, tweetList and trueFalseList, and zips them together. It then creates a dataframe out of this list, that can then be converted to a .csv file

annotatedallTweets = list(zip(allTweets, trueFalseList))
tweetDataframe = pandas.DataFrame(annotatedallTweets)
tweetDataframe.to_csv('literary-annotated-tweets.csv', header=["Tweets", "isLiterary"], index=False)

