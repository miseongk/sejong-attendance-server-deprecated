from datetime import datetime

def parseLectureName(lectureName):
    fullDate = lectureName[-35:]
    startDate = fullDate[5:7] + fullDate[8:10] + fullDate[11:13] + fullDate[14:16]
    endDate = fullDate[24:26] + fullDate[27:29] + fullDate[30:32] + fullDate[33:35]
    onlyLectureName = lectureName[6: len(lectureName) - 38]

    return startDate, endDate, onlyLectureName


def parseLectureStatus(startDate, endDate, currentDate, isPass):
    # 상태 1 : 아직 기간 안됨
    # 상태 2 : 들음
    # 상태 3 : 지금 수강기간, 안들음
    # 상태 4 : 수강기간 지남, 안들음
    if currentDate < startDate:
        return 1;
    elif isPass == 'P':
        return 2;
    elif currentDate <= endDate and isPass == 'F':
        return 3;
    else:
        return 4;


def getCurrentDate():
    time = datetime.now()

    month = '0' + str(time.month) if time.month < 10 else str(time.month)
    date =  '0' + str(time.day) if time.day < 10 else str(time.day)
    hour = '0' + str(time.hour) if time.hour < 10 else str(time.hour)
    min = '0' + str(time.minute) if time.minute < 10 else str(time.minute)

    return month + date + hour + min


def checkStatusCounter(lectures):
    thisWeekUnpassCount = 0
    allUnpassCount = 0
    if len(lectures) != 0:
        for lecture in lectures:
            if lecture['status'] == 3:
                thisWeekUnpassCount += 1
                allUnpassCount += 1
            if lecture['status'] == 4:
                allUnpassCount += 1

    return thisWeekUnpassCount, allUnpassCount



