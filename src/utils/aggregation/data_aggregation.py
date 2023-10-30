from src.utils.aggregation.schemas import GetRequestMessage, GetData
from src.utils.aggregation.request_to_database import RequestToDataBase

class DataAggregation:
    def __init__(self, request: GetRequestMessage):
        self.request = request

    async def get_data(self) -> GetData:
        return await RequestToDataBase().get_data(self.request)

    async def is_valid_request(self, request: GetRequestMessage) -> bool:
        ...
