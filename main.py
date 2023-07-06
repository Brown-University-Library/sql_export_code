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
    # (continue, err) = determine_whether_to_run_script()

    ## initiate a mysql dump --
    HEREZZ

    ## evaluate if there have been any changes
    """
    If some aspect of the dump contains a time-stamp, see if there's a way to determine whether the actual data has changed.
    """

    ## if the data has changed...

        ## commit to repo-A

        ## push to repo-A

        ## commit to repo-B

        ## push to repo-B

    ## end def manager()


def validate_env_vars():
    validity = True
    err = None
    return (validity, err)


if __name__ == '__main__':
    manager()
