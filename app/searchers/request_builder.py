from typing import Union, Dict
from requests import request, Response
from urllib.error import HTTPError
from pprint import pprint
import sys
import time

from ..utils import creator_sleep_generator

sleep_generator = creator_sleep_generator(4)


class RequestBuilder:
    
    def __init__(self, method,  url, headers, message, params: Union[None, Dict]=None):
        
        self._method = method
        self._url = url
        self._headers = headers
        self._message = message
        self._params = params
        self._time_for_wait =  sleep_generator
    
    
    def request(self) -> Response:
        """
        Generate request with params
        '"""
        try:
            time.sleep(next(sleep_generator))
            response = request(
                method=self._method,
                url=self._url,
                headers=self._headers,
                params=self._params
            )
            
            pprint(f"Request to {self._url} for {self._message} success.")
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                        error.code,
                        error.url,
                        error.read()
                    )
                )

        return response