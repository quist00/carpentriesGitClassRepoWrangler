# gitClassRepoWrangler
* This tools is intended to help remove some of the tedium from setting up and executing the conflict resolution exercises in the carpentries GIT lessons, in particular http://swcarpentry.github.io/git-novice/09-conflict/index.html.
* This is a commandline tools that uses argh.  You can get help for the basic and sub commands by using the --help flag.  
* With appropriate permissions and depencies, you should be able to run the script using ./gcrw

## What it can do.
* invite class roster to repo
* create individual working file for user in solo directory      
* can change number of known lines in all solo files to make a conflict they have to resolve.
* divide class into two person teams and one 3 person team if necessary
* create a team file on the teams directory using a combination of their names 
* can change number of known lines in all team files to make a conflict they have to resolve. 

## What it should do.
* Maybe it shoul be able to get the roster straight from evenbrite or other registration platform.
* It needs to be better about handling existing file or existing branches.


     
## Required files
* You must create a personal access token and store it in file called ".TOKEN" in the root directory of the repository on your local machine. This is part of the git ignore and should never be checked in for any reason.
* You should also create a .REPO file that contains the name of the repo you want to manage in the form of GITNAME/Repo_Name. The repo should have a branch called "main" to which all the commits will be made.
* You must add a roster.csv file with the columns: git-username,first-name,last-name

## Dependencies
You need pygithub. 
   `conda install -c conda-forge pygithub `
or
   `pip install PyGithub`

You need argh.
   `pip install argh`
    
You need pandas
   `pip install pandas`
