import re
import datetime

def get_integer_ratings(statements, responseText):
    integers = re.findall(r"\s*([0-9]+)\s*", responseText)
    integers = [int(entry) for entry in integers]
    ratings = {statements[x]:integers[x] for x in range(len(statements))}
    return ratings


def get_date_now():
    now = datetime.datetime.now()
    nowString = now.strftime("%m_%d_%Y_time=%H_%M_%S")
    #year, month, day, time = now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H:%M:%S")
    #nowString = year + "_" + month + "_" + day + "_" + time + "_"
    return nowString

def get_average_vote(votes):

    average = votes[0]
    for vote in votes[1:]:
        for i in range(len(vote)):
            average[i] = average[i] + vote[i]
    
   

    average = [average[i]/len(votes) for i in range(len(average))]
    
    return average
        

