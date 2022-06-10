#%%
import pandas as pd
from github import Github
#import shutil
import random
#import time
import re
#%%

with open('.TOKEN','r') as f:
    TOKEN = f.read()
    #print(TOKEN)
#%%
roster = pd.read_csv('roster.csv')
git_users = roster['git-username'].to_list()
print(roster)
print(git_users)

#%%
# act as me using my personal access token
g = Github(TOKEN)

#see all my repos
for repo in g.get_user().get_repos():
    print(repo.name)

# %%
#get a handle to class repo
repo = g.get_repo("quist00/2021-03-23-STROBE-git-class")
print(repo.name)

#%%
#send invites to list of git usernames in roster file
for u in git_users:
    repo.add_to_collaborators(u,'push')
# %%
#print out pending invites and collaborators
print("Invites")
for i in repo.get_pending_invitations():
    print(i.invitee)

#print out collaborators
print("\nCollaborators")
for c in repo.get_collaborators():
    print(c.name)
# %%
#create haiku file for each individual leaner, this will not work if file exists
content = ''
with open('haikus.txt','r') as f:
    content = f.read()

for u in git_users:
    repo.create_file('solo/{}.txt'.format(u), 'individual file for{}'.format(u), content)
#%%
# put each solo file into a conflicting state
conflict_string = "### This is an intentional conflict with your solo file. [KEEP THIS]  Resolve by preserving your changes along with anything in brackets on this line.\n"
file_bytes = ''
contents = repo.get_contents("/solo")
for content_file in contents:
    # by default file just appears as hashed array I think, so have to call decode
    file_bytes= content_file.decoded_content
    #regex on file bytes requires match in file bytes. To hard to write so convert to string.
    file_as_string = file_bytes.decode('utf-8')
    #replace all teh author lines with a stock phrase
    updated_contents= re.sub(r'###.*?\n',conflict_string,file_as_string)
    #print(updated_contents)
    repo.update_file(content_file.path, "force conflict with {}".format(content_file.name), updated_contents, content_file.sha, branch="main")
# %%
#make random teams

# divides a list into n sized chunks
def divide_chunks(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

#randomize list
random.shuffle(git_users)
#divide into teams
teams = list(divide_chunks(git_users, 2))

# if learners is odd make last team a team of 3
if len(teams)%2 == 1:
    temp = teams.pop()
    teams[-1] = teams[-1] + temp

print(teams)
 
# %%
# make a file for each team based on their usernames
content = ''
with open('haikus.txt','r') as f:
    content = f.read()

for t in teams:
    member_names = '-'.join(t)
    repo.create_file('teams/{}.txt'.format(member_names), 'team file for{}'.format(member_names), content)
    #shutil.copy('haikus.txt',('teams/{}.txt'.format('-'.join(t))))
# %%

# put team files into a conflicting state
conflict_string = "### This is an intentional conflict. [KEEP THIS]  Resolve by preserving your changes along with anything in brackets on this line.\n"
file_bytes = ''
contents = repo.get_contents("/teams")
for content_file in contents:
    # by default file just appears as hashed array I think, so have to call decode
    file_bytes= content_file.decoded_content
    #regex on file bytes requires match in file bytes. Too hard to write so convert to string.
    file_as_string = file_bytes.decode('utf-8')
    #replace all the author lines with a stock phrase
    updated_contents= re.sub(r'###.*?\n',conflict_string,file_as_string)
    #print(updated_contents)
    repo.update_file(content_file.path, "force conflict with {}".format(content_file.name), updated_contents, content_file.sha, branch="main")
#%% 
# delete all files in solo
contents = repo.get_contents("/solo")
for content_file in contents:
    #repo.delete_file(content_file.path, "remove file from solo folder", content_file.sha, branch="main")
    

#%% 
# delete all files in teams
contents = repo.get_contents("/teams")
for content_file in contents:
    #repo.delete_file(content_file.path, "remove file from teams folder", content_file.sha, branch="main")
