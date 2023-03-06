"""
Controller.
"""

import logging, os
import trio


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


async def main():

    ## initiate a mysql dump


    ## evaluate if there have been any changes
    """
    If some aspect of the dump contains a time-stamp, see if there's a way to determine whether the actual data has changed.
    """

    ## if the data has changed...

        ## commit to repo-A

        ## push to repo-A

        ## commit to repo-B

        ## push to repo-B


if __name__ == '__main__':
    trio.run( main )
