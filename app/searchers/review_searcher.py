from typing import  Union
from requests import Response
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


from .request_builder import RequestBuilder
from ..data_objects.review_unit import SetOfReviewUnits


class ReviewSearcher:
    
    _useragent: UserAgent = UserAgent(os='linux')

    def __init__(self, url: str, company_id: str) -> None:
        """
        Forms a GET request to the page and extracts text 
        data from the <script> tag on the page

        Args:
        url (str): base url to Yelp
        company_id str: for formated correct url 
        
        Raises:
        HTTPError: An error occurs from the HTTP request.
        """
        self._url = url
        self._company_id = company_id


    def _url_builder(self):
        return f"{self._url}/biz/{self._company_id}"
    
    
    def request(self) -> Response:
        """
        Generate request to Yelp with 'application/json
        '"""
        response = RequestBuilder(
            method="GET",
            url=self._url_builder(),
            headers={
                "User-Agent": self._useragent.chrome,
            },
            message=f'for getting reviews on the client by id: {self._company_id}'
        ).request()

        return response


    def get_reviews_set(self) -> SetOfReviewUnits:
        """
        Method for get reviews data, limit 5 reviews.
        :return: SetOfReviewUnits => Tuple[ReviewUnit]
        """        
        raw_data = self._get_data_from_page()
        
        if not raw_data:
            return SetOfReviewUnits(company_id=self._company_id)
        
        return  SetOfReviewUnits(
            company_id=self._company_id
            ).get_reviews_from_text_data(raw_text_data=raw_data)
    
    
    def _get_data_from_page(self) -> Union[str, None]:
        
        page = self.request()
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        raw_data = soup.select('script[type="application/json"]')

        try:
            
            return raw_data[0].text.strip()
        
        except IndexError:
            
            return 
    