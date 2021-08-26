# gitClassRepoWrangler
you must create a personal access token and store it in file called ".TOKEN" in the root directory of the repository on your local machine. You should also create a .REPO file that contains the path to the repo you want to wrangle. This is part of the git ignore and should never be checked in for any reason.

## Dependencies
You need pygithub. options:
    conda install -c conda-forge pygithub 
    pip install PyGithub

You need argh.
    pip install argh
    
You need pandas
    pip install pandas
## What it can do.
    * invite class roster to repo
    * create individual working file for user in solo directory
      
    * can change number of known lines in all team files to make assist with making a conflict they have to resolve.


## What it should do.
???
 * divide class into two person teams and one 3 person team if necessary
        * create a team file on the teams directory using a combination of their names 