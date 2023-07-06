"""
Controller.
"""

import logging, os
# import trio


## set up logging ---------------------------------------------------
level_dict = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    }
desired_level = level_dict[ os.environ.get('SQL_EXPORT__LOG_LEVEL', 'debug') ]
logging.basicConfig( 
    filename=os.environ['SQL_EXPORT__LOG_PATH'],
    level=desired_level,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s', 
    datefmt='%d/%b/%Y %H:%M:%S'
    )
log = logging.getLogger(__name__)
log.debug( 'log set' )


def manager():
    """ Manages flow of data from mysql to github.
        Called by dunder-main. """
    
    ## validate environment variables -------------------------------
    (ok , err) = validate_env_vars()

    ## TODO-determine whether to run script -------------------------
    (continue_processing, err) = determine_whether_to_run_script()  # TODO; hard-coded to True for now

    ## initiate a mysql dump ----------------------------------------
    (sql_filepath, err) = initiate_mysql_dump()

    ## evaluate if there have been any changes ----------------------
    (changes_detected, err) = look_for_changes( sql_filepath )  # TODO; hard-coded to True for now

    ## update repos -------------------------------------------------
    ## if the data has changed...
    continue_flow = True
    if continue_flow:

        ## commit to repo-A
        (ok, err) = commit_to_repo_A()

        ## push to repo-A
        (ok, err) = push_to_repo_A()

        ## commit to repo-B
        (ok, err) = commit_to_repo_B()

        ## push to repo-B
        (ok, err) = push_to_repo_B()

    ## end def manager()


def validate_env_vars():
    validity = True
    err = None
    return (validity, err)


if __name__ == '__main__':
    manager()
