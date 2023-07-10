"""
Controller.
"""

import logging, os, subprocess

## envars -----------------------------------------------------------
SQL_EXPORT__LOG_PATH = os.environ['SQL_EXPORT__LOG_PATH']
SQL_OUTPUT_FILEPATH = os.environ['SQL_EXPORT__SQL_OUTPUT_FILEPATH']
MYSQLDUMP_FILEPATH = os.environ['SQL_EXPORT__MYSQLDUMP_FILEPATH']
MYSQLDUMP_CONF_FILEPATH = os.environ['SQL_EXPORT__MYSQLDUMP_CONF_FILEPATH']
USERNAME = os.environ['SQL_EXPORT__USERNAME']
HOST = os.environ['SQL_EXPORT__HOST']
DATABASE_NAME = os.environ['SQL_EXPORT__DATABASE_NAME']
REPO_DIR_PATH = os.environ['SQL_EXPORT__REPO_DIR_PATH']

## set up logging ---------------------------------------------------
level_dict = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    }
desired_level = level_dict[ os.environ.get('SQL_EXPORT__LOG_LEVEL', 'debug') ]
logging.basicConfig( 
    filename=SQL_EXPORT__LOG_PATH,
    level=desired_level,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', 
    datefmt='%d/%b/%Y %H:%M:%S'
    )
log = logging.getLogger(__name__)
log.debug( 'log set' )


def manager():
    """ Manages flow of data from mysql to github.
        Called by dunder-main. """
    
    ## possibe TODO -- determine whether to run script --------------
    continue_processing: bool = determine_whether_to_run_script()  # TODO; hard-coded to True for now

    ## initiate a mysql dump ----------------------------------------
    initiate_mysql_dump()

    ## possible TODO -- evaluate if there have been any changes -----
    changes_detected = look_for_changes()  # TODO; hard-coded to True for now

    ## update repos -------------------------------------------------
    if changes_detected:

        ## commit to repo-A
        commit_to_repo_A()

        ## push to repo-A
        (ok, err) = push_to_repo_A()

        # ## commit to repo-B
        # (ok, err) = commit_to_repo_B()

        # ## push to repo-B
        # (ok, err) = push_to_repo_B()

    ## end def manager()


## helper functions -------------------------------------------------


def determine_whether_to_run_script() -> bool:
    """ possible TODO -- maybe some sort of initial db query to find last-updated date? """
    return True


def initiate_mysql_dump():
    """ Runs mysqldump command to create a sql file. 
        Called by manager(). """
    mysqldump_command = [
        MYSQLDUMP_FILEPATH,
        f'--defaults-file={MYSQLDUMP_CONF_FILEPATH}',
        f'--user={USERNAME}',
        f'--host={HOST}',
        '--enable-cleartext-plugin',
        '--skip-lock-tables',
        '--no-tablespaces',
        '--skip-extended-insert',
        DATABASE_NAME,
    ]
    log.debug( f'mysqldump_command, ``{" ".join(mysqldump_command)}``')
    with open(SQL_OUTPUT_FILEPATH, 'w') as file:
        try:
            subprocess.run(mysqldump_command, stdout=file)
            log.debug( f'sql file produced, at ``{SQL_OUTPUT_FILEPATH}``' )
        except Exception as e:
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return


def look_for_changes() -> bool:
    """ possible TODO -- perhaps this will be the place to ascertain last-updated date? """
    return True


def commit_to_repo_A():
    """ Commits to repo-A.
        Called by manager(). """
    log.debug( 'starting commit_to_repo_A()' )
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
    log.debug( f'git_commit_command, ``{" ".join(git_commit_command)}``' )
    with open(SQL_EXPORT__LOG_PATH, 'w') as log_file:
        try:
            subprocess.run(git_commit_command, stdout=log_file)
            log.debug( f'git_commit_command output at ``{SQL_EXPORT__LOG_PATH}``' )
        except Exception as e:
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return 


if __name__ == '__main__':
    manager()
    log.debug( 'processing complete' )
