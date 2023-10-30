from src.utils.aggregation.schemas import GetRequestMessage, GetData, GetDataFromDataBase
from src.database import aggregation_coll

from datetime import datetime, timedelta


class RequestToDataBase:
    def __init__(self):
        pass

    async def get_data(self, request: GetRequestMessage) -> GetData:
        return await self.request_to_database(request)

    async def request_to_database(self, request: GetRequestMessage) -> GetData:
        pipeline = await self.get_pipeline(request)
        data = list(aggregation_coll.aggregate(pipeline))
        group_type = request["group_type"]

        if group_type == "hour":
            return await self.validation_group_type_hour(data, request["dt_from"], request["dt_upto"])

        elif group_type == "day":
            return await self.validation_group_type_day(data, request["dt_from"], request["dt_upto"])

        else:
            return await self.validation_group_type_week_or_month(data)

    @staticmethod
    async def validation_group_type_hour(
            data: GetDataFromDataBase,
            dt_from: datetime,
            dt_upto: datetime
    ) -> GetData:
        date_range = [datetime.fromisoformat(dt_from) + timedelta(hours=x) for x in
                      range(((datetime.fromisoformat(dt_upto)
                              - datetime.fromisoformat(dt_from)).days * 24) + 1)]

        results_dict = {date.strftime("%Y-%m-%d %H:00:00"): 0 for date in date_range}

        for result in data:
            date_str = result["_id"]
            total_value = result["total_value"]
            results_dict[date_str] = total_value

        labels = list(results_dict.keys())
        for i, v in enumerate(labels):
            labels[i] = labels[i].replace(" ", "T")

        dataset = list(results_dict.values())

        return {"dataset": dataset, "labels": labels}

    @staticmethod
    async def validation_group_type_day(
            data: GetDataFromDataBase,
            dt_from: datetime,
            dt_upto: datetime
    ) -> GetData:
        date_range = [datetime.fromisoformat(dt_from) + timedelta(days=x) for x in
                      range((datetime.fromisoformat(dt_upto) -
                             datetime.fromisoformat(dt_from)).days + 1)]

        results_dict = {date.strftime("%Y-%m-%dT00:00:00"): 0 for date in date_range}

        for result in data:
            date_str = result["_id"]
            total_value = result["total_value"]
            results_dict[date_str] = total_value

        labels = list(results_dict.keys())
        for i, v in enumerate(labels):
            labels[i] = labels[i].replace(" ", "T")
        dataset = list(results_dict.values())

        return {"dataset": dataset, "labels": labels}

    @staticmethod
    async def validation_group_type_week_or_month(
            data: GetDataFromDataBase
    ) -> GetData:
        dataset = [result["total_value"] for result in data]
        labels = [result["_id"] for result in data]

        return {'dataset': dataset, 'labels': labels}

    @staticmethod
    async def get_pipeline(request: GetRequestMessage):
        dt_from = request["dt_from"]
        dt_upto = request["dt_upto"]
        group_type = request["group_type"]

        pipeline = [
            {
                "$match": {
                    "dt": {"$gte": datetime.fromisoformat(dt_from), "$lte": datetime.fromisoformat(dt_upto)}
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": {
                                "$switch": {
                                    "branches": [
                                        {"case": {"$eq": [group_type, "day"]}, "then": "%Y-%m-%dT00:00:00"},
                                        {"case": {"$eq": [group_type, "hour"]}, "then": "%Y-%m-%d %H:00:00"},
                                        {"case": {"$eq": [group_type, "week"]}, "then": "%Y-%m-%w-01T00:00:00"},
                                        {"case": {"$eq": [group_type, "month"]}, "then": "%Y-%m-01T00:00:00"}
                                    ],
                                    "default": "%Y-%m-01T00:00:00"
                                }
                            },
                            "date": "$dt"
                        }
                    },
                    "total_value": {"$sum": "$value"}
                }
            },
            {
                "$sort": {"_id": 1}
            }
        ]

        return pipeline
