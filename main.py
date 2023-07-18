"""
Controller.
Note: holding off on repo-B work -- it requires conversion from sql to an sqlite-db.
"""

import logging, os, shutil, subprocess

## envars -----------------------------------------------------------
LOG_PATH = os.environ['SQL_EXPORT__LOG_PATH']
LOG_LEVEL = os.environ['SQL_EXPORT__LOG_LEVEL']
REPO_A_DIR_PATH = os.environ['SQL_EXPORT__REPO_A_DIR_PATH']                     # for repo-A commit and push
REPO_A_BRANCH = os.environ['SQL_EXPORT__REPO_A_BRANCH']                         # for repo-A commit and push
DATABASE_NAME_A = os.environ['SQL_EXPORT__DATABASE_NAME_A']                     # for mysqldump connection
DATABASE_NAME_B = os.environ['SQL_EXPORT__DATABASE_NAME_B']                     # for mysqldump connection
MYSQLDUMP_COMMAND_FILEPATH = os.environ['SQL_EXPORT__MYSQLDUMP_FILEPATH']       # for mysqldump connection
MYSQLDUMP_CONF_FILEPATH = os.environ['SQL_EXPORT__MYSQLDUMP_CONF_FILEPATH']     # for mysqldump connection
USERNAME = os.environ['SQL_EXPORT__USERNAME']                                   # for mysqldump connection
HOST = os.environ['SQL_EXPORT__HOST']                                           # for mysqldump connection
SQL_OUTPUT_FILEPATH_A = os.environ['SQL_EXPORT__SQL_OUTPUT_FILEPATH_A']         # for database-A mysqldump output

# REPO_B_DIR_PATH = os.environ['SQL_EXPORT__REPO_B_DIR_PATH']                     # for repo-B commit and push
# SQL_OUTPUT_FILEPATH_B = os.environ['SQL_EXPORT__SQL_OUTPUT_FILEPATH_B']         # for database-B mysqldump output
# SQL_OVERWRITE_PATH = os.environ['SQL_EXPORT__SQL_OVERWRITE_PATH']               # for repo-B/database-A overwrite

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


def manager():
    """ Manages flow of data from mysql to github.
        Called by dundermain. """
    
    ## possibe TODO -- determine whether to run script --------------
    continue_processing: bool = determine_whether_to_run_script()  # TODO; hard-coded to True for now

    ## checkout repo-A branch ---------------------------------------
    checkout_repo_A_branch()

    ## initiate repo-A mysql dump -----------------------------------
    initiate_mysql_dump( db_name=DATABASE_NAME_A, output_filepath=SQL_OUTPUT_FILEPATH_A )
    # initiate_mysql_dump( db_name=DATABASE_NAME_B, output_filepath=SQL_OUTPUT_FILEPATH_B )

    ## possible TODO -- evaluate if there have been any changes -----
    changes_detected = look_for_changes()  # TODO; hard-coded to True for now

    ## update repos -------------------------------------------------
    if changes_detected:

        ## commit to repo-A
        commit_to_repo_A()

        ## push to repo-A
        push_to_repo_A()

        ## update repo-B
        """ Holding off on repo-B work -- it requires conversion from sql to an sqlite-db. """
        # update_repo_B()

        ## commit to repo-B
        # commit_to_repo_B()

        ## push to repo-B
        # push_to_repo_B()

    ## end def manager()


## helper functions -------------------------------------------------


def determine_whether_to_run_script() -> bool:
    """ possible TODO -- maybe some sort of initial db query to find last-updated date? """
    return True


def checkout_repo_A_branch() -> None:
    git_checkout_command = [
        'git',
        'checkout',
        REPO_A_BRANCH,
        ]
    log.debug( f'repo-a git_checkout_command, ``{" ".join(git_checkout_command)}``' )
    return


def initiate_mysql_dump( db_name, output_filepath ) -> None:
    """ Runs mysqldump command to create a sql file. 
        Called by manager(). """
    mysqldump_command = [
        MYSQLDUMP_COMMAND_FILEPATH,
        f'--defaults-file={MYSQLDUMP_CONF_FILEPATH}',
        f'--user={USERNAME}',
        f'--host={HOST}',
        '--enable-cleartext-plugin',
        '--skip-lock-tables',
        '--no-tablespaces',
        '--skip-extended-insert',
        db_name,
    ]
    log.debug( f'mysqldump_command, ``{" ".join(mysqldump_command)}``')
    with open(output_filepath, 'w') as file:
        try:
            subprocess.run(mysqldump_command, stdout=file)
            log.debug( f'sql file produced, at ``{output_filepath}``' )
        except Exception as e:
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return


def look_for_changes() -> bool:
    """ possible TODO -- perhaps this will be the place to ascertain last-updated date? """
    return True


def commit_to_repo_A() -> None:
    """ Commits to repo-A.
        Called by manager(). """
    log.debug( 'starting commit_to_repo_A()' )
    ## change to target dir -----------------------------------------
    log.debug( f'cwd, ``{os.getcwd()}``' )
    os.chdir( REPO_A_DIR_PATH )
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
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return 


def push_to_repo_A() -> None:
    """ Pushes to repo-A.
        Called by manager(). """
    log.debug( 'starting push_to_repo_A()' )
    ## change to target dir -----------------------------------------
    log.debug( f'cwd, ``{os.getcwd()}``' )
    os.chdir( REPO_A_DIR_PATH )  # likely can be removed; should alreading be in the right place
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
            log.exception( f'exception, ``{e}``' )
            raise Exception( f'exception, ``{e}``' )
    return 


# def update_repo_B() -> None:
#     """ Copies sql-output-A file to repo-B. 
#         Called by manager(). 
#         Not currently used; sql requres conversion to sqlite db. """
#     log.debug( 'starting update_repo_B()' )
#     try:
#         shutil.copy2( SQL_OUTPUT_FILEPATH_A, SQL_OVERWRITE_PATH )
#     except Exception as e:
#         log.exception( f'exception, ``{e}``' )
#         raise Exception( f'exception, ``{e}``' )
#     return


# def commit_to_repo_B() -> None:
#     """ Commits to repo-B.
#         Possible TODO: merge with commit_to_repo_A().
#         Called by manager(). 
#         Not currently used; sql requres conversion to sqlite db. """
#     log.debug( 'starting commit_to_repo_B()' )
#     ## change to target dir -----------------------------------------
#     log.debug( f'cwd, ``{os.getcwd()}``' )
#     os.chdir( REPO_B_DIR_PATH )
#     log.debug( f'cwd, ``{os.getcwd()}``' )
#     ## run git commit -----------------------------------------------
#     git_commit_command = [
#         'git',
#         'commit',
#         '-am',
#         'updates sql from scripted mysqldump',
#         ]
#     log.debug( f'repo-b git_commit_command, ``{" ".join(git_commit_command)}``' )
#     with open(LOG_PATH, 'a') as log_file:
#         try:
#             subprocess.run(git_commit_command, stdout=log_file)
#             log.debug( f'repo-b git_commit_command output at ``{LOG_PATH}``' )
#         except Exception as e:
#             log.exception( f'exception, ``{e}``' )
#             raise Exception( f'exception, ``{e}``' )
#     return 


# def push_to_repo_B() -> None:
#     """ Pushes to repo-A.
#         Called by manager(). 
#         Not currently used; sql requres conversion to sqlite db. """
#     log.debug( 'starting push_to_repo_A()' )
#     ## change to target dir -----------------------------------------
#     log.debug( f'cwd, ``{os.getcwd()}``' )
#     os.chdir( REPO_B_DIR_PATH )  # likely can be removed; should alreading be in the right place
#     log.debug( f'cwd, ``{os.getcwd()}``' )
#     ## run git commit -----------------------------------------------
#     git_push_command = [
#         'git',
#         'push',
#         ]
#     log.debug( f'repo-B git_push_command, ``{" ".join(git_push_command)}``' )
#     with open(LOG_PATH, 'a') as log_file:
#         try:
#             subprocess.run(git_push_command, stdout=log_file)
#             log.debug( f'repo-B  git_push_command output at ``{LOG_PATH}``' )
#         except Exception as e:
#             log.exception( f'exception, ``{e}``' )
#             raise Exception( f'exception, ``{e}``' )
#     return 


if __name__ == '__main__':
    manager()
    log.debug( 'processing complete' )
