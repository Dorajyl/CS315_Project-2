import json
import pandas as pd

#Read in TikTok json Files
# d1 = json.load(open("/user_data.json")) #Vid Browse empty
# d2 = json.load(open("user_data1.json")) #Vid Browse empty
d3 = json.load(open("/Users/fernandagonzalez/Desktop/school/CS 315/CS315_Project-2/user_data2.json"))

#Extract TikTok Video Links from browseList
browseList = d3['Activity']['Video Browsing History']['VideoList']
# print(len(browseList)) #27936

vidList = [] #list of tiktok browse history video links
for dict in browseList:
    vidList.append(dict['Link'])
# print(len(vidList)) #27936

#Extract List of Accounts a User is Following
followingList = d3['Activity']['Following List']['Following']
# print(len(followingList)) #56

follows = [] #list of username the user follows
for acct in followingList:
    follows.append(acct['UserName'])
# print(len(follows)) #56

#Check if there are Overlaps on Followed Accts vs News Accts
newsAcctList = pd.read_csv("/Users/fernandagonzalez/Desktop/school/CS 315/CS315_Project-2/List of News Accounts.csv")
newsAcct = newsAcctList['Username'].tolist()

overlapAccts = []
for fw in follows:
    if fw in newsAcct:
        overlapAccts.append(fw)
print(overlapAccts) #There are no overlaps