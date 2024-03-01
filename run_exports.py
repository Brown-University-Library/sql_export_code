"""
- Controller file, normally called by cron.
- Dundermain calls manager(), which is near top of file, with helper functions below.
"""

import logging, os, pathlib, shutil, subprocess


## set up envars ----------------------------------------------------
## paths ----------------------------------------
LOG_PATH = pathlib.Path( os.environ['SQL_EXPORT__LOG_PATH'] )
REPO_DIR_PATH = pathlib.Path( os.environ['SQL_EXPORT__REPO_DIR_PATH'] )                            # for repo commit and push
MYSQLDUMP_COMMAND_FILEPATH = pathlib.Path( os.environ['SQL_EXPORT__MYSQLDUMP_FILEPATH'] )          # for mysqldump connection
MYSQLDUMP_CONF_FILEPATH = pathlib.Path( os.environ['SQL_EXPORT__MYSQLDUMP_CONF_FILEPATH'] )         # for mysqldump connection
SQL_OUTPUT_INSERTS_SEPARATE_PATH = pathlib.Path( os.environ['SQL_EXPORT__SQL_OUTPUT_INSERTS_SEPARATE_PATH'] ) # for mysqldump output
SQL_OUTPUT_INSERTS_TOGETHER_PATH = pathlib.Path( os.environ['SQL_EXPORT__SQL_OUTPUT_INSERTS_TOGETHER_PATH'] ) # for mysqldump output
## other ----------------------------------------
LOG_LEVEL = os.environ['SQL_EXPORT__LOG_LEVEL']
REPO_URL = os.environ['SQL_EXPORT__REPO_URL']                                       # for repo clone, commit, and push
REPO_BRANCH = os.environ['SQL_EXPORT__REPO_BRANCH']                                 # for repo commit and push
HOST = os.environ['SQL_EXPORT__HOST']                                               # for mysqldump connection
DATABASE_NAME = os.environ['SQL_EXPORT__DATABASE_NAME']                             # for mysqldump connection
USERNAME = os.environ['SQL_EXPORT__USERNAME']                                       # for mysqldump connection


## set up logging ---------------------------------------------------
level_dict = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    }
desired_level = level_dict[ LOG_LEVEL ]
logging.basicConfig( 
    filename=LOG_PATH,
    level=desired_level,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', 
    datefmt='%d/%b/%Y %H:%M:%S'
    )
log = logging.getLogger(__name__)
log.debug( 'log set' )


## main controller function -----------------------------------------
def manager():
    """ Manages flow of data from mysql to github.
        New flow:
        - delete existing repo.
        - shallow-clone repo.
        - run mysqldump
        - commit
        - update permissions.
        Called by dundermain. """
    ## delete existing repo ---------------------
    delete_existing_repo()
    ## shallow-clone repo -----------------------
    shallow_clone_repo()
    ## checkout branch --------------------------
    ## no need; the clone command does this!
    ## run mysqldump ----------------------------
    run_mysqldump()
    ## commit and push to repo ------------------
    commit_to_repo()
    push_to_repo()
    return
    ## end def manager()


## helper functions START -------------------------------------------


def delete_existing_repo() -> None:
    """ Deletes existing repo. 
        Called by manager(). """
    log.debug( 'starting delete_existing_repo()' )
    if REPO_DIR_PATH.exists():
        try:
            shutil.rmtree( REPO_DIR_PATH )
            log.debug( f'deleted existing repo at ``{REPO_DIR_PATH}``' )
        except Exception as e:
            msg = f'exception, ``{e}``'
            log.exception( msg )
            raise Exception( msg )
    return


def shallow_clone_repo() -> None:
    """ Shallow-clones repo -- whole purpose is to keep the repo directory on the server small.
        Called by manager(). """
    log.debug( 'starting shallow_clone_repo()' )
    ## run git clone ----------------------------
    git_clone_command = [
        'git',
        'clone',
        '--branch',
        REPO_BRANCH,
        '--single-branch',
        '--depth=1',
        REPO_URL,
        str(REPO_DIR_PATH),
        ]
    log.debug( f'repo git_clone_command, ``{" ".join(git_clone_command)}``' )
    with open(LOG_PATH, 'a') as log_file:  # for subprocess stdout capture
        try:
            subprocess.run(git_clone_command, stdout=log_file)
            log.debug( f'repo-a git_clone_command output at ``{LOG_PATH}``' )
        except Exception as e:
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return

        
# def checkout_repo_branch() -> None:
#     """ Confirms proper branch. 
#         Called by manager(). """
#     log.debug( 'starting checkout_repo__branch()' )
#     ## change to target dir ---------------------
#     os.chdir( REPO_DIR_PATH )
#     log.debug( f'cwd, ``{os.getcwd()}``' )
#     ## run git checkout -------------------------
#     git_checkout_command = [
#         'git',
#         'checkout',
#         REPO_BRANCH,
#         ]
#     log.debug( f'repo-a git_checkout_command, ``{" ".join(git_checkout_command)}``' )
#     with open(LOG_PATH, 'a') as log_file:
#         try:
#             subprocess.run(git_checkout_command, stdout=log_file)
#             log.debug( f'repo-a git_commit_command output at ``{LOG_PATH}``' )
#         except Exception as e:
#             log.exception( f'exception, ``{e}``' )
#             raise Exception( f'exception, ``{e}``' )
#     return


def run_mysqldump() -> None:
    """ Builds mysqldump commands, and runs them. 
        Called by manager(). """
    log.debug( 'starting run_mysqldump()' )
    ## build commands ---------------------------
    commands = build_commands()
    ## run mysqldump ----------------------------
    initiate_mysql_dump( commands['inserts_separate_command'], SQL_OUTPUT_INSERTS_SEPARATE_PATH )
    initiate_mysql_dump( commands['inserts_together_command'], SQL_OUTPUT_INSERTS_TOGETHER_PATH )
    return


def build_commands() -> dict:
    """ Builds two commands.
        Puts each command in a dict, for ease of reference and clarity.
        Called by run_mysqldump(). """
    commands = {}
    commands['inserts_separate_command'] = [
        MYSQLDUMP_COMMAND_FILEPATH,
        f'--defaults-file={MYSQLDUMP_CONF_FILEPATH}',
        f'--user={USERNAME}',
        f'--host={HOST}',
        '--enable-cleartext-plugin',
        '--skip-lock-tables',
        '--no-tablespaces',
        '--skip-extended-insert',  # key difference between two commands
        DATABASE_NAME,
    ]
    commands['inserts_together_command'] = [
        MYSQLDUMP_COMMAND_FILEPATH,
        f'--defaults-file={MYSQLDUMP_CONF_FILEPATH}',
        f'--user={USERNAME}',
        f'--host={HOST}',
        '--enable-cleartext-plugin',
        '--skip-lock-tables',
        '--no-tablespaces',
        DATABASE_NAME,
    ]
    log.debug( f'commands, ``{commands}``' )
    return commands


def initiate_mysql_dump( mysqldump_command: list, output_filepath: pathlib.Path ) -> None:
    """ Runs supplied mysqldump command to create the sql file. 
        Called by run_mysqldump(). """
    log.debug( f'mysqldump_command, ``{" ".join(mysqldump_command)}``')
    with open(output_filepath, 'w') as file:
        try:
            subprocess.run(mysqldump_command, stdout=file)
            log.debug( f'sql file produced, at ``{output_filepath}``' )
        except Exception as e:
            msg = f'exception, ``{e}``'
            log.exception( msg )
            raise Exception( msg )
    return


def commit_to_repo() -> None:
    """ Commits the two new sql files to the repo.
        Called by manager(). """
    log.debug( 'starting commit_to_repo_()' )
    ## change to target dir ---------------------
    log.debug( f'cwd, ``{os.getcwd()}``' )
    os.chdir( REPO_DIR_PATH )
    log.debug( f'cwd, ``{os.getcwd()}``' )
    ## run git commit ---------------------------
    git_commit_command = [
        'git',
        'commit',
        '-am',
        'updates sql from scripted mysqldump',
        ]
    log.debug( f'repo-a git_commit_command, ``{" ".join(git_commit_command)}``' )
    with open(LOG_PATH, 'a') as log_file:
        try:
            subprocess.run(git_commit_command, stdout=log_file)
            log.debug( f'repo-a git_commit_command output at ``{LOG_PATH}``' )
        except Exception as e:
            msg = f'exception, ``{e}``'
            log.exception( msg )
            raise Exception( msg )
    return 


def push_to_repo() -> None:
    """ Pushes the committed files to the repo.
        Called by manager(). """
    log.debug( 'starting push_to_repo_()' )
    ## change to target dir ---------------------
    log.debug( f'cwd, ``{os.getcwd()}``' )
    os.chdir( REPO_DIR_PATH )  # likely can be removed; should alreading be in the right place
    log.debug( f'cwd, ``{os.getcwd()}``' )
    ## run git commit ---------------------------
    git_push_command = [
        'git',
        'push',
        'origin',
        f'{REPO_BRANCH}:{REPO_BRANCH}',
        ]
    log.debug( f'repo git_push_command, ``{" ".join(git_push_command)}``' )
    with open(LOG_PATH, 'a') as log_file:
        try:
            subprocess.run(git_push_command, stdout=log_file)
            log.debug( f'repo-A  git_push_command output at ``{LOG_PATH}``' )
        except Exception as e:
            msg = f'exception, ``{e}``'
            log.exception( msg )
            raise Exception( msg )
    return 


## helper functions END ---------------------------------------------


## dundermain -------------------------------------------------------
if __name__ == '__main__':
    log.debug( '\n\nstarting sql-export-processing...' )
    manager()
    log.debug( 'processing complete' )
