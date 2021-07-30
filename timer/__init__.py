import datetime

def split_time_string(time_string):
    output = {
        "year": time_string[:4],
        "month": time_string[4:6],
        "day": time_string[6:8],
        "hour": time_string[8:10],
        "minute": time_string[10:12],
        "second": time_string[12:14]
    }
    return output

def time_remaining(chosen_time): #takes in format yyyymmddhhmmss
    chosen_time = split_time_string(chosen_time)
    current = split_time_string(str(datetime.date.today()).replace("-", "") + datetime.datetime.now().strftime("%H%M%S"))
    diff = lambda x: abs(int(chosen_time.get(x, 0)) - int(current.get(x, 0)))
    difference = [diff("year"), diff("month"), diff("day"), diff("hour"), diff("minute"), diff("second")]
    return difference



if __name__ == "__main__":
    date = str(datetime.date.today()).replace("-", "")
    time = datetime.datetime.now().strftime("%H%M%S")
    print(time_remaining("20210730134455"))