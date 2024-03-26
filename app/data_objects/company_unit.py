from typing import List, Dict
from dataclasses import dataclass, field
import re
from .review_unit import SetOfReviewUnits

@dataclass
class CompanyUnit:
    company_id:         str = '' # 'bizId'
    company_name:       str = '' # 'searchResultBusiness' > 'name'
    bussines_raiting:   str = '' # 'searchResultBusiness' > 'rating'
    reviews_count:       str = '' # 'searchResultBusiness' > 'reviewCount'
    yelp_url:           str = ''  # 'searchResultBusiness' > 'alias' -> 'https://yelp.com/biz/' + alias
    business_site:      str  = '' # 'searchResultBusiness' > 'website' -> 'parse r'(?<=%252F%252F).+?(?=%)' r'(?<=%252F%252F).+?(?=%)'
    reviews:            list  = field(default_factory=list)
    
    
    def __lt__(self, other: 'CompanyUnit'):
         return self.reviews < other.reviews
    
    
    def _to_dict(self) -> dict:
        
        return  {      
            'company_name': self.__dict__.get('company_name'),    
            'bussines_raiting': self.__dict__.get('bussines_raiting'),
            'reviews_count': self.__dict__.get('reviews_count'),
            'yelp_url': self.__dict__.get('yelp_url'),
            'business_site': self.__dict__.get('business_site'),
            'reviews': self.__dict__.get('reviews')
        }
    
    
    @classmethod
    def from_dict(cls, values:Dict) -> 'CompanyUnit':
        
        biz_data = values.get('searchResultBusiness', {})
        
        return CompanyUnit(
            company_id=values.get('bizId', ''),
            
            company_name=biz_data.get('name', ''),
            
            bussines_raiting=biz_data.get('rating', ''),
            
            reviews_count=biz_data.get('reviewCount', ''),
            
            yelp_url= 'https://yelp.com/biz/' + biz_data.get('alias', ''),
            
            business_site=cls._get_business_site(biz_data)
            )
    
    
    @classmethod
    def _get_business_site(cls, data: Dict)-> str:
        
        try:
            url = data.get('website', '').get('href', '')
            return cls._parse_business_website_from_url(url)
        except AttributeError:
            return ''
    
    
    @classmethod
    def _parse_business_website_from_url(cls, url: str) -> str:
        
        if not 'www.yelp.com%' in url:
            return url.lower()
        
        try:
            pattern_http = r'(?<=%26url%3D).+?(?=%253A%252F%252F)'
            http_business_site = re.findall(pattern_http, url, flags=re.MULTILINE | re.DOTALL)[0]
            pattern = r'(?<=%252F%252F).+?(?=%)'
            business_site = re.findall(pattern, url, flags=re.MULTILINE | re.DOTALL)[0]

            return f'{http_business_site}://{business_site}'.lower()
        except IndexError:
            
            return ''
    
    def insert_reviews(
        self, reviews_set: SetOfReviewUnits, num_of_units:int = 5
                ) -> 'CompanyUnit':
            
            if not len(reviews_set.reviews) > num_of_units:
                
                self.reviews = reviews_set.reviews
            
            else:
                
                self.reviews = reviews_set.reviews[:num_of_units]
            return self
    
    
    @classmethod
    def drop_duplicates(
        cls, company_units: List[dict]
                )-> List[dict]:
        """
        Droping from set duplicates of data
        """
        seen = set()
        
        claen_company_units = []
        
        for unit in company_units:
            check_unit = str(unit.get('bizId'))
            
            if check_unit not in seen:
                claen_company_units.append(unit)
                seen.add(check_unit)
        
        return claen_company_units
    