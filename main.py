import argparse
import sys
from urllib.error import HTTPError

from app.crawler import YelpCrawler



# Defaults for our example.
DEFAULT_TERM = 'contractors'
DEFAULT_LOCATION =  'Washington' #'San Francisco, CA'
DEFAULT_SEARCH_LIMIT = 15



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')
    
    parser.add_argument('-n', '--num', dest='limit',
                    default=DEFAULT_SEARCH_LIMIT, type=str,
                    help='What limit of business search (default: %(default)s)')

    input_values = parser.parse_args()

    
    
    try:
        YelpCrawler(input_values.term, input_values.location, int(input_values.limit)).run()
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read()
            )
        )


if __name__ == '__main__':
    main()