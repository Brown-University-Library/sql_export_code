"""
Controller.
Note: holding off on repo-B work -- it requires conversion from sql to an sqlite-db.
"""

import logging, os, shutil, subprocess

## set up envars ----------------------------------------------------
LOG_PATH = os.environ['SQL_EXPORT__LOG_PATH']
LOG_LEVEL = os.environ['SQL_EXPORT__LOG_LEVEL']
REPO_DIR_PATH = os.environ['SQL_EXPORT__REPO_DIR_PATH']                             # for repo commit and push
REPO_BRANCH = os.environ['SQL_EXPORT__REPO_BRANCH']                                 # for repo commit and push
MYSQLDUMP_COMMAND_FILEPATH = os.environ['SQL_EXPORT__MYSQLDUMP_FILEPATH']           # for mysqldump connection
MYSQLDUMP_CONF_FILEPATH = os.environ['SQL_EXPORT__MYSQLDUMP_CONF_FILEPATH']         # for mysqldump connection
USERNAME = os.environ['SQL_EXPORT__USERNAME']                                       # for mysqldump connection
HOST = os.environ['SQL_EXPORT__HOST']                                               # for mysqldump connection
DATABASE_NAME = os.environ['SQL_EXPORT__DATABASE_NAME']                             # for mysqldump connection
SQL_OUTPUT_INSERTS_SEPARATE = os.environ['SQL_EXPORT__SQL_OUTPUT_INSERTS_SEPARATE'] # for mysqldump output
SQL_OUTPUT_INSERTS_TOGETHER = os.environ['SQL_EXPORT__SQL_OUTPUT_INSERTS_TOGETHER'] # for mysqldump output

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

## get to work ------------------------------------------------------
def manager():
    """ Manages flow of data from mysql to github.
        Called by dundermain. """
    ## checkout branch ----------------------------------------------
    checkout_repo_branch()
    ## build the two commands ---------------------------------------
    commands: dict = build_commands()
    ## initiate mysql dump ------------------------------------------
    initiate_mysql_dump( commands['inserts_separate_command'], output_filepath=SQL_OUTPUT_INSERTS_SEPARATE )
    initiate_mysql_dump( commands['inserts_together_command'], output_filepath=SQL_OUTPUT_INSERTS_TOGETHER )
    ## update repo --------------------------------------------------
    commit_to_repo()
    push_to_repo()

    ## end def manager()

## helper functions -------------------------------------------------

def checkout_repo_branch() -> None:
    """ Confirms proper branch. """
    log.debug( 'starting checkout_repo__branch()' )
    ## change to target dir -----------------------------------------
    os.chdir( REPO_DIR_PATH )
    log.debug( f'cwd, ``{os.getcwd()}``' )
    ## run git checkout ---------------------------------------------
    git_checkout_command = [
        'git',
        'checkout',
        REPO_BRANCH,
        ]
    log.debug( f'repo-a git_checkout_command, ``{" ".join(git_checkout_command)}``' )
    with open(LOG_PATH, 'a') as log_file:
        try:
            subprocess.run(git_checkout_command, stdout=log_file)
            log.debug( f'repo-a git_commit_command output at ``{LOG_PATH}``' )
        except Exception as e:
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return

def build_commands() -> dict:
    """ Builds two commands.
        Called by manager(). """
    commands = {}
    commands['inserts_separate_command'] = [
        MYSQLDUMP_COMMAND_FILEPATH,
        f'--defaults-file={MYSQLDUMP_CONF_FILEPATH}',
        f'--user={USERNAME}',
        f'--host={HOST}',
        '--enable-cleartext-plugin',
        '--skip-lock-tables',
        '--no-tablespaces',
        '--skip-extended-insert',
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

def initiate_mysql_dump( mysqldump_command: list, output_filepath: str ) -> None:
    """ Runs supplied mysqldump command to create the sql file. 
        Called by manager(). """
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

# def initiate_mysql_dump( db_name: str, output_filepath: str ) -> None:
#     """ Runs mysqldump command to create a sql file. 
#         Called by manager(). """
#     mysqldump_command = [
#         MYSQLDUMP_COMMAND_FILEPATH,
#         f'--defaults-file={MYSQLDUMP_CONF_FILEPATH}',
#         f'--user={USERNAME}',
#         f'--host={HOST}',
#         '--enable-cleartext-plugin',
#         '--skip-lock-tables',
#         '--no-tablespaces',
#         '--skip-extended-insert',
#         db_name,
#     ]
#     log.debug( f'mysqldump_command, ``{" ".join(mysqldump_command)}``')
#     with open(output_filepath, 'w') as file:
#         try:
#             subprocess.run(mysqldump_command, stdout=file)
#             log.debug( f'sql file produced, at ``{output_filepath}``' )
#         except Exception as e:
#             log.exception( f'exception, ``{e}``' )
#             raise Exception( f'exception, ``{e}``' )
#     return

def commit_to_repo() -> None:
    """ Commits the two new sql files to the repo.
        Called by manager(). """
    log.debug( 'starting commit_to_repo_()' )
    ## change to target dir -----------------------------------------
    log.debug( f'cwd, ``{os.getcwd()}``' )
    os.chdir( REPO_DIR_PATH )
    log.debug( f'cwd, ``{os.getcwd()}``' )
    ## run git commit -----------------------------------------------
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
    ## change to target dir -----------------------------------------
    log.debug( f'cwd, ``{os.getcwd()}``' )
    os.chdir( REPO_DIR_PATH )  # likely can be removed; should alreading be in the right place
    log.debug( f'cwd, ``{os.getcwd()}``' )
    ## run git commit -----------------------------------------------
    git_push_command = [
        'git',
        'push',
        ]
    log.debug( f'repo-A git_push_command, ``{" ".join(git_push_command)}``' )
    with open(LOG_PATH, 'a') as log_file:
        try:
            subprocess.run(git_push_command, stdout=log_file)
            log.debug( f'repo-A  git_push_command output at ``{LOG_PATH}``' )
        except Exception as e:
            msg = f'exception, ``{e}``'
            log.exception( msg )
            raise Exception( msg )
    return 

## dundermain -------------------------------------------------------
if __name__ == '__main__':
    log.debug( '\n\nstarting sql-export-processing...' )
    manager()
    log.debug( 'processing complete' )
