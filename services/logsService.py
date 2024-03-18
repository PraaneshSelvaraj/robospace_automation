from databases import mongoDB
from filters import requestFilter

mongoUtil = mongoDB.MongoUtil()

async def get_logs(query : requestFilter.LogQuery):
    logs = mongoUtil.get_logs(query.start_date, query.end_date)
    return {"message" : "Logs", "data" : {"logs" : logs}}