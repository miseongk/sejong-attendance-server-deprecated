import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Union
import pandas as pd

from utils.utils import parseLectureName, parseLectureStatus, getCurrentDate, checkStatusCounter

app = FastAPI()

class Course(BaseModel):
    course_id: str
    class_id: str
    dept_id: str
    student_id: str

class Courses(BaseModel):
    courses: Union[List[Course], None] = None

@app.post("/lectures")
def get_lectures(courses: Courses):
    semester = '20222020'
    currentDate = getCurrentDate()
    lectureData = []

    for course in courses.courses:
        url = f'https://blackboard.sejong.ac.kr/webapps/bbgs-OnlineAttendance-BB5cf774ff89eaf/excel?selectedUserId={course.student_id}&crs_batch_uid={semester}{course.dept_id}{course.course_id}{course.class_id}&title={course.student_id}&column=studentId,location,lecture_name,learned_time,learning_recog_time,lecture_time,progress,is_pass'
        dfs = pd.read_html(url)
        df = dfs[0]
        result = []
        for index, row in df.iterrows():
            startDate, endDate, onlyLectureName = parseLectureName(row['lecture_name'])
            status = parseLectureStatus(startDate, endDate, currentDate, row['is_pass'])
            result.append({
                "location": row['location'],
                "lecture_name": onlyLectureName,
                "start_date": startDate,
                "end_date": endDate,
                "progress": row['progress'],
                "is_pass": True if row['is_pass'] == 'P' else False,
                "status": status
            })
        thisWeekUnpassCount, allUnpassCount = checkStatusCounter(result)
        course_result = {
            "course_id": course.course_id,
            "unpass_count": {
                "this_week": thisWeekUnpassCount,
                "all": allUnpassCount
            },
            "lectures" : result
        }
        lectureData.append(course_result)

    return lectureData

if __name__== "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)