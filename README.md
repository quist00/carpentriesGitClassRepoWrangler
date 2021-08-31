# gitClassRepoWrangler
* This tools is intended to help remove some of the tedium from setting up and executing the conflict resolution exercises in the carpentries GIT lessons, in particular http://swcarpentry.github.io/git-novice/09-conflict/index.html.
* This is a commandline tools that uses argh.  You can get help for the basic and sub commands by using the --help flag.  
* With appropriate permissions and depencies, you shoud be able to run the script using ./gcrw

## What it can do.
* invite class roster to repo
* create individual working file for user in solo directory      
* can change number of known lines in all solo files to make a conflict they have to resolve.


## What it should do.
???
 * divide class into two person teams and one 3 person team if necessary
 * create a team file on the teams directory using a combination of their names 
 * can change number of known lines in all team files to make a conflict they have to resolve. 
     
## Required files
* You must create a personal access token and store it in file called ".TOKEN" in the root directory of the repository on your local machine. This is part of the git ignore and should never be checked in for any reason.
* You should also create a .REPO file that contains the path to the repo you want to wrangle. 
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
