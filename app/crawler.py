
from urllib.error import HTTPError
from pprint import pprint
import sys
from typing import List
import json

from .searchers.category_searcher import CategorySearcher
from .searchers.review_searcher import ReviewSearcher
from .data_objects.company_unit import CompanyUnit
from .data_objects.review_unit import ReviewUnit, SetOfReviewUnits


class YelpCrawler:
    """
    Class to combine program logic of crawler
    """

    def __init__(self, category: str, location: str, limit: int):
        """
        Args:
        category (str): Category of serch business.
        location (str): Location of serching business.
        limit (int): unit limit in result.
        
        Raises:
        HTTPError: An error occurs from the HTTP request.
        """
        
        self._url = "https://www.yelp.com/"
        self._category = category
        self._location = location
        self._limit = limit
    
   
    def _get_category_units_list(self) -> List[CompanyUnit]:
        """
        Method get business list from XHR request and validation in pydantic schema
        :return: list[dict] -> [{biz_name1: name}, {biz_name2: name}, ...]
        """
        try:
            category_response = CategorySearcher(
                url=self._url,
                category=self._category,
                location=self._location,
                unit_limit=self._limit,
            )
            
            category_units_list = [
                CompanyUnit().from_dict(unit) for unit in 
                CompanyUnit.drop_duplicates(category_response.get_category_units_list())]
            
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read()
                    )
            )
            
        return category_units_list
            
            
    def _get_review_units_list(self, biz_id: str) -> SetOfReviewUnits:
        """
        Method for get review list by biz_id from main page of compamy on yelp.com
        :param biz_id: str, need for url
        :return: SetOfReviewUnits -> list[ReviewUnit, ReviewUnit]
        """
        
        review_response = ReviewSearcher(
            url=self._url, company_id=biz_id
        )
        pprint(review_response.get_reviews_set())
        
        return review_response.get_reviews_set()


    def _insert_reviews_to_companies(
            self, list_company_units: List[CompanyUnit]
                ) -> List[CompanyUnit]:
        
        ready_to_use_companies = [
            unit.insert_reviews(self._get_review_units_list(unit.company_id)) 
            
            for unit in list_company_units
        ]
        
        return ready_to_use_companies


    def sorted_company_units(
            self, company_set: List[CompanyUnit], key:str, reverse=True
                ) -> List[CompanyUnit]:

            if key in CompanyUnit.__annotations__.keys():
                
                company_set = sorted(
                    company_set,
                    key=lambda u: u.__dict__[key],
                    reverse=reverse
                    )
            
            return company_set
     
    def transform_company_set_to_json(self, company_set: List[CompanyUnit]):
        
        return json.dumps([company._to_dict() for company in company_set])
        
     
    def save_json_file(self, json_data) -> None:
         
        name = f'{self._category}_in_{self._location.replace(" ", "_")}_data.json'

        with open(name, 'w') as file:
            file.write(json_data)
        
        
    def run(self):
        
        company_units_list = self._get_category_units_list()
        
        company_units_sorted = self.sorted_company_units(company_units_list, 'reviews_count')
                
        companies = self._insert_reviews_to_companies(company_units_sorted[:self._limit])
        
        companies_in_json = self.transform_company_set_to_json(companies)
        
        pprint(companies_in_json)
        
        self.save_json_file(companies_in_json)  
        