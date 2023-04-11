import pandas as pd
from github import Github
#import shutil
import random
#import time
import re
import pickle
import sys


def get_repo():
    TOKEN = get_token()
    # act as me using my personal access token
    repo_owner = Github(TOKEN)
    #get a handle to class repo
    repo = repo_owner.get_repo(get_repo_name())
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


def get_token() -> str:
    '''
    This function gets the token from the .TOKEN file.
    '''
    try:
        with open('.TOKEN','r') as token_file:
            return token_file.read().strip()
    except FileNotFoundError:
        print('No .TOKEN file found. Exiting...')
        sys.exit(1)
    except PermissionError:
        print("You don't have the necessary permissions to read the .TOKEN file. Exiting...")
        sys.exit(1)
    except:
        print('Something went wrong. Exiting...')
        sys.exit(1)



def get_repo_name() -> str:
    '''
    This function gets the name of the current repository from the .REPO file.
    '''
    try:
        with open('.REPO','r') as repo_file:
            return repo_file.read().strip()
    except FileNotFoundError:
        print('No .REPO file found. Exiting...')
        sys.exit(1)
    except PermissionError:
        print("You don't have the necessary permissions to read the .REPO file. Exiting...")
        sys.exit(1)
    except:
        print('Something went wrong. Exiting...')
        sys.exit(1)



def get_roster(roster_path='roster.csv'):
    """ This prints out contents of the roster file."""
    roster = pd.read_csv(roster_path)
    return(roster)



def invite_users(user_list):
#send invites to list of git usernames in roster file and create branches for them
    repo= get_repo()
    for u in user_list:
        print('inviting {}\n'.format(u))
        repo.add_to_collaborators(u,'push')

        #create branches
        source_branch = 'main'
        sb = repo.get_branch(source_branch)
        repo.create_git_ref(ref='refs/heads/' + u, sha=sb.commit.sha)
    print("Notificaitons may be delayed, have users check https://github.com/"+ get_repo_name() +"/invitations")

def create_solo_files():
#create haiku file for each individual learner, this will not work if file exists
    #delete_solo_files()
    
    repo = get_repo()
    roster = get_roster()
    git_users = roster['git-username'].to_list()
    content = ''
    with open('haikus.txt','r') as f:
        content = f.read()

    for u in git_users:
        repo.create_file('solo/{}.txt'.format(u), 'individual file for {}'.format(u), content,branch=u)

def make_solo_files_conclict():
# put each solo file into a conflicting state
    repo = get_repo()
    roster = get_roster()
    git_users = roster['git-username'].to_list()
    conflict_string = "― Kobayashi Issa [b. June 15, 1763], loose translation/interpretation by Michael R. Burch\n"
    file_bytes = ''
    for u in git_users:
        contents = repo.get_contents("/solo",ref=u)
        #print(contents)
        for content_file in contents:
        # by default file just appears as hashed array I think, so have to call decode
            file_bytes= content_file.decoded_content
        #regex on file bytes requires match in file bytes. To hard to write so convert to string.
            file_as_string = file_bytes.decode('utf-8')
        #replace all the author lines with a stock phrase
            updated_contents= re.sub(r'― Kobayashi Issa.*?\n',conflict_string,file_as_string)
            #print(updated_contents)
        #print(updated_contents)
            repo.update_file(content_file.path, "force conflict with {}".format(content_file.name), updated_contents, content_file.sha, branch=u)

# divides a list into n sized chunks
# 
def divide_chunks(l, n): 
# looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def get_teams():
    teams = pickle.load( open( ".teams", "rb" ) )
    print(teams)

def make_teams():
#randomize list
    repo = get_repo()
    roster = get_roster()
    git_users = roster['git-username'].to_list()
    random.shuffle(git_users)
#divide into teams
    teams = list(divide_chunks(git_users, 2))

# if learners is odd make last team a team of 3
    if len(git_users)%2 == 1:
        odd = teams.pop()
        more_the_merrier = teams.pop()
        more_the_merrier.append(odd[0])
        teams.append(more_the_merrier)

    pickle.dump( teams, open( ".teams", "wb" ) )
    print(teams)
    #make branches for each team
    #create branches
    print('creating teams\n')
    for t in teams: 
        member_names = '-'.join(t)  
        source_branch = 'main'
        sb = repo.get_branch(source_branch)
        repo.create_git_ref(ref='refs/heads/' + member_names, sha=sb.commit.sha)
 
def make_team_files():
# make a file for each team based on their usernames
    teams = pickle.load( open( ".teams", "rb" ) )   
    if not teams:
        print("you must first create the teams")
        return

    repo = get_repo()
    
#{'content': ContentFile(path="example/test.txt"), 'commit': Commit(sha="5b584cf6d32d960bb7bee8ce94f161d939aec377")}
    content = ''
    with open('haikus.txt','r') as f:
        content = f.read()

    for t in teams:
        member_names = '-'.join(t)
        repo.create_file('teams/{}.txt'.format(member_names), 'team file for{}'.format(member_names), content, branch=member_names)
   
def make_team_files_conflict():
# put team files into a conflicting state
    repo = get_repo()
    teams = pickle.load( open( ".teams", "rb" ) )  
    conflict_string = "― Kobayashi Issa [b. June 15, 1763], loose translation/interpretation by Michael R. Burch\n"
    file_bytes = ''

    for t in teams:
        member_names = '-'.join(t)
        contents = repo.get_contents("/teams",ref=member_names)
        for content_file in contents:
            # by default file just appears as hashed array I think, so have to call decode
            file_bytes= content_file.decoded_content
            #regex on file bytes requires match in file bytes. Too hard to write so convert to string.
            file_as_string = file_bytes.decode('utf-8')
            #replace all the author lines with a stock phrase
            updated_contents= re.sub(r'― Kobayashi Issa.*?\n',conflict_string,file_as_string)
            #print(updated_contents)
            repo.update_file(content_file.path, "force conflict with {}".format(content_file.name), updated_contents, content_file.sha, branch=member_names)

def delete_solo_files():
# delete all files in solo
    repo = get_repo()
    roster = get_roster()
    git_users = roster['git-username'].to_list()

    for u in git_users:
        contents = repo.get_contents("/solo",ref=u)
        for content_file in contents:
            repo.delete_file(content_file.path, "remove file from solo folder", content_file.sha, branch=u)

    #repo.create_file("/solo/.keep_folder", "empty file to help create the directory", "", branch="main")

def delete_team_files():
# delete all files in teams
    repo = get_repo()
    teams = pickle.load( open( ".teams", "rb" ) )  
    for t in teams:
        member_names = '-'.join(t)
        contents = repo.get_contents("/teams",ref=member_names)
        for content_file in contents:
            repo.delete_file(content_file.path, "remove file from teams folder", content_file.sha, branch=member_names)

    #repo.create_file("/teams/.keep_folder", "empty file to help create the directory", "", branch="main")


#see all my repos
def list_repos():
    for repo in g.get_user().get_repos():
        print(repo.name)
