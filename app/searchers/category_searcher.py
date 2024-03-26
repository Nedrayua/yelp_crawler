from typing import List, Dict
from requests import Response
from fake_useragent import UserAgent
from pprint import pprint


from .request_builder import RequestBuilder

class CategorySearcher:
    
    _useragent: UserAgent = UserAgent().random

    def __init__(self, url: str, location: str, category: str, unit_limit: int):
        """
        Args:
        url (str): base url to Yelp
        category (str): Category of serch category umits.
        location (str): Location of serching category unit.
        limit (int): unit limit in result.
        
        Returns:????
        dict: The JSON response from the request.
        
        Raises:
        HTTPError: An error occurs from the HTTP request.
        """
        self._url = url
        self._location = location
        self._category = category
        self._limit = unit_limit
        self.offset = 0


    def _url_builder(self):
        
        return f"{self._url}/search/snippet?"
    
    
    def params(self):
        """
        creating parameters for request with current data
        """
        
        return {
                "find_desc": self._category,
                "find_loc": self._location,
                "start": self.offset,
                "parent_request": "",
                "ns": 1,
                "request_origin": "user",
            }
    
    
    def build_message(self) -> str:
        
        return 'find companies by params:\ncategory => {cat}\nlocation => {loc}\n'


    def request(self) -> Response:
        """
        Generate request to Yelp with 'application/json
        '"""
    
        response = RequestBuilder(
                method="GET",
                url=self._url_builder(),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": self._useragent,
                },
                message = self.build_message().format(
                        cat=self._category,
                        loc=self._location
                        ),
                params=self.params(),
            ).request()
    
        return response


    def get_category_units_list(self) -> List[Dict]:
        """
        Method for getting category units from Yelp
        :return: valid and transform data
        """
        result_data = []
        
        while True:
            response = self.request()

            clear_data = [
                dict(item)
                for item in response.json()["searchPageProps"][
                    "mainContentComponentsListProps"
                ]
                if "bizId" in item.keys()
            ]
            result_data.extend(clear_data)

            pprint(f"Request business with {self.offset} offset.")

            self.offset += 10

            if not clear_data or self.offset >= self._limit:
                break
        
        try:  
            return result_data[:self._limit]

        except IndexError: 
            return result_data
