from utilities.http_request import HttpRequestBuilder, FakeHttpRequestBuilder, HttpRequestBuilderBase
from backend.utilities.processors import OpenEiProcessor

from abc import ABC, abstractmethod
from typing import Any

OPENEI_API_KEY = 'dfGKbN8UBOw7IdQrHsC63V9IdFGGfnVbFRHcuUHr'
OPENEI_UTILITY_RATES_START_DATE = '2022-01-01'
OPENEI_VERSION = '3'

class UtilityRatesServiceBase(ABC):
    user_params = {}
    response_processor = OpenEiProcessor()

    @abstractmethod
    def get_openei_results(self) -> Any:
        pass


class UtilityRatesService(UtilityRatesServiceBase):
    def __init__(self) -> None:
        self.openei_base_url = 'https://api.openei.org/utility_rates'
        self.http_request = HttpRequestBuilder(base_url=self.openei_base_url).add_param('version', OPENEI_VERSION).add_param('api_key', OPENEI_API_KEY).add_param('start_date',OPENEI_UTILITY_RATES_START_DATE)

    def get_openei_results(self) -> Any:
        self.http_request.params.update(self.user_params)
        api_director = UtilityRatesDirector(builder=self.http_request, response_processor=self.response_processor)
        openei_response = api_director.openei_request()
        result = api_director.process_request(openei_response=openei_response)

        return result

class FakeUtilityRatesService(UtilityRatesServiceBase):
    def __init__(self) -> None:
        self.fake_openei_base_url = 'https://api.fakeopenei.org/utility_rates'
        self.fake_http_request = FakeHttpRequestBuilder(self.fake_openei_base_url).add_param('api_key', 'fake_api_key').add_param('start_date','2022-01-01')

    def get_openei_results(self) -> Any:
        api_director = UtilityRatesDirector(builder=self.fake_http_request, response_processor=self.response_processor)
        openei_response = api_director.openei_request()
        result = api_director.process_request(openei_response=openei_response)

        return result

class UtilityRatesDirector:
    def __init__(self, builder: HttpRequestBuilderBase, response_processor: OpenEiProcessor):
        self.builder = builder
        self.response_processor = response_processor

    def openei_request(self) -> Any:
        api_response = self.builder.execute()
        #TODO parse response
        #TODO create an iterator from response
        return api_response
    
    def process_request(self, openei_response) -> Any:
        processed_result = self.response_processor.process_response(openei_response)

        return processed_result
