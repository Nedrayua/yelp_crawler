from typing import List, Dict
from dataclasses import dataclass, field
import re

@dataclass
class ReviewUnit:
    reviewer_name: str
    reviewer_raitig: str
    review_date: str
        
    
    @classmethod
    def from_dict(cls, values:dict) -> 'ReviewUnit':
        return ReviewUnit(
                reviewer_name = values.get('name', ''),
                reviewer_raitig = values.get('raiting', ''),
                review_date = values.get('date', '')
                )
    
    def review_to_dict(self) -> Dict:
        
        return {
            'rewiever_name': self.reviewer_name,
            'rewiever_raiting': self.reviewer_raitig,
            'review_date': self.review_date
        }
    

@dataclass
class SetOfReviewUnits:
    company_id:     str
    reviews:        list = field(default_factory=list)


    def get_reviews_from_text_data(
            self, raw_text_data: str, limit: int=5) -> 'SetOfReviewUnits':
        
        raw_reviews_text = self._get_raw_text_from_text(raw_text_data)
        split_raw_reviews_text = self._split_raw_text_on_reviews(
                raw_reviews_text
                )

        reviews = []
        
        keys = 'name', 'raiting', 'date'
        
        for review in split_raw_reviews_text:
            if  review:
                
                values = self._get_clean_review_data(review)
                
                if any(values):
                    reviews.append(dict(zip(keys, values)))

        reviews = list(reviews[:limit]) if reviews else []
        
        return SetOfReviewUnits(self.company_id, reviews)
    
    
    def _get_raw_text_from_text(self, text:str) -> str:

        _start_pattern = '.reviews({\&quot;first\&quot;:20}).edges.0.node&quot;:'
        
        _end_pattern = '.reviews({\&quot;first\&quot;:20})&quot;:'
        
        start = text.find(_start_pattern)
        
        end = text.find(_end_pattern)
        
        raw_text = text[start:end + len(_end_pattern)]
        
        
        return raw_text.replace('\&quot;', '"').replace('&quot;', '"')
    
    
    def _split_raw_text_on_reviews(self, raw_text) -> List[str]:

        _split_pattern ='"__typename":"ReviewEdge"'

        return  raw_text.split(_split_pattern)

    
    def _get_clean_review_data(self, text:str) -> tuple:
        
        pattern_find_rating = r'\"rating\":([^,]+)'

        pattern_find_name = r'\"displayName\":([^,]+)'
        element_date_pattern = '\{\"localDateTime\(\{\"forBusiness\":\"' + \
            f'{self.company_id}' + '\"\}\)\":([^,]+)'

        pattern_find_date = rf'{element_date_pattern}'
        name_data = re.findall(pattern_find_name, text)
        clean_name = self._get_first_element_from_list(name_data).replace('"', '')
        rating_data = re.findall(pattern_find_rating, text)
        clean_raining = self._get_first_element_from_list(rating_data).replace('"', '')
        date_data = re.findall(pattern_find_date, text)
        date = self._get_first_element_from_list(date_data).replace('"', '')
        clean_date = self._get_first_element_from_list(self._clean_date(date))
        
        return clean_name, clean_raining, clean_date


    def _clean_date(self, text_date):
        pattern = r'(\d\d\d\d-\d\d-\d\d)'
        
        return re.findall(pattern, text_date)
    
    def _get_first_element_from_list(self, list_data):
        
        try:
            return list_data[0]
        except IndexError:
            return ''
