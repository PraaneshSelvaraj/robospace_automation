from databases import mongoDB
from filters import requestFilter
import pandas as pd
import io
from fastapi.responses import StreamingResponse

mongoUtil = mongoDB.MongoUtil()

async def get_logs(query : requestFilter.LogQuery):
    logs = mongoUtil.get_logs(query.start_date, query.end_date)
    return {"message" : "Logs", "data" : {"logs" : logs}}

async def get_logs_excel(query: requestFilter.LogQuery):
    logs = mongoUtil.get_logs(query.start_date, query.end_date)

    df = pd.DataFrame(logs)

    df['datetime'] = pd.to_datetime(df['datetime'])

    excel_output = io.BytesIO()
    df.to_excel(excel_output, index=False)
    excel_output.seek(0)

    return StreamingResponse(
        iter([excel_output.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=logs_report.xlsx"}
    )