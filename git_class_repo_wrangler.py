import pandas as pd
from github import Github
#import shutil
import random
#import time
import re


def get_repo():
    TOKEN = get_token()
    # act as me using my personal access token
    repo_owner = Github(TOKEN)
    #get a handle to class repo
    #repo = repo_owner.get_repo("quist00/2021-03-23-STROBE-git-class")
    repo = repo_owner.get_repo(get_repo_name())
    #print("Getting handle to",repo.name)
    return repo

def get_status():
    """ This returns status information abou the repo including: invites, collaborators
    """
    #invitees = []
    #collaborators = {}
    status = ""
#print out pending invites and collaborators
    repo = get_repo()
    print("Invites")
    print("*******************************")
    invitations = repo.get_pending_invitations()
    logins_invite = [i.invitee.login for i in invitations]
    names_invite = [i.invitee.name for i in invitations]
    invitees_df = pd.DataFrame.from_dict({'login':logins_invite, 'name':names_invite})
    print(invitees_df.set_index('login').sort_index())
#print out collaborators
    print("\n\nCollaborators")
    print("*******************************")
    collaborators = repo.get_collaborators()
    logins = [c.login for c in collaborators]
    names = [c.name for c in collaborators]
    collaboratros_df = pd.DataFrame.from_dict({'login':logins, 'name':names})
    print(collaboratros_df.set_index('login').sort_index())


def get_token():
    with open('.TOKEN','r') as f:
        #TOKEN = f.read()
        return f.read()

def get_repo_name():
    with open('.REPO','r') as f:
        #TOKEN = f.read()
        return f.read()

def get_roster(roster_path='roster.csv'):
    """ This prints out contents of the roster file."""
    roster = pd.read_csv(roster_path)
    return(roster)



def invite_users(user_list):
#send invites to list of git usernames in roster file
    for u in user_list:
        print('inviting {}\n'.format(u))
        get_repo().add_to_collaborators(u,'push')
    print("Notificaitons may be delayed, have users check https://github.com/"+ get_repo_name() +"/invitations")

def create_solo_files():
#create haiku file for each individual learner, this will not work if file exists
    delete_solo_files()
    
    repo = get_repo()
    roster = get_roster()
    git_users = roster['git-username'].to_list()
    content = ''
    with open('haikus.txt','r') as f:
        content = f.read()

    for u in git_users:
        repo.create_file('solo/{}.txt'.format(u), 'individual file for {}'.format(u), content)

    # TODO: revise to make it configurable repo.create_file('solo/{}.txt'.format('quist00'), 'individual file for {}'.format('quist00'), content)

def make_solo_files_conclict():
# put each solo file into a conflicting state
    repo = get_repo()
    conflict_string = "### This is an intentional conflict with your solo file. [KEEP THIS]  Resolve by preserving your changes along with anything in brackets on this line.\n"
    file_bytes = ''
    contents = repo.get_contents("/solo")
    for content_file in contents:
    # by default file just appears as hashed array I think, so have to call decode
        file_bytes= content_file.decoded_content
    #regex on file bytes requires match in file bytes. To hard to write so convert to string.
        file_as_string = file_bytes.decode('utf-8')
    #replace all the author lines with a stock phrase
        updated_contents= re.sub(r'― Kobayashi Issa.*?\n',conflict_string,file_as_string)
    #print(updated_contents)
        repo.update_file(content_file.path, "force conflict with {}".format(content_file.name), updated_contents, content_file.sha, branch="main")

# divides a list into n sized chunks
# 
def divide_chunks(l, n): 
# looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def make_teams():
#randomize list
    random.shuffle(git_users)
#divide into teams
    teams = list(divide_chunks(git_users, 2))

# if learners is odd make last team a team of 3
    if len(teams)%2 == 1:
        temp = teams.pop()
        teams[-1] = teams[-1] + temp

    print(teams)
 
def make_team_files():
# make a file for each team based on their usernames
    content = ''
    with open('haikus.txt','r') as f:
        content = f.read()

    for t in teams:
        member_names = '-'.join(t)
        repo.create_file('teams/{}.txt'.format(member_names), 'team file for{}'.format(member_names), content)
   
def make_team_files_conflict():
# put team files into a conflicting state
    repo = get_repo()
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

def delete_solo_files():
# delete all files in solo
    repo = get_repo()
    contents = repo.get_contents("/solo")
    for content_file in contents:
        repo.delete_file(content_file.path, "remove file from solo folder", content_file.sha, branch="main")

def delete_team_files():
# delete all files in teams
    contents = repo.get_contents("/teams")
    for content_file in contents:
        repo.delete_file(content_file.path, "remove file from teams folder", content_file.sha, branch="main")




#see all my repos
def list_repos():
    for repo in g.get_user().get_repos():
        print(repo.name)
