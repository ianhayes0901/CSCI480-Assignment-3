
import sys
import subprocess

#implement pip as a subprocess:
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'openai'])

#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'xlwt'])



import os
import openai
import json
import xlwt
from xlwt import Workbook


openai.api_key = "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"
openai.Model.list()

response = openai.Completion.create(
    model ="text-davinci-003",
    prompt = "Give me 1 week of a schedule for one employee with the following availability 10:00 am to 8:00 pm in format 'Day; Start Time-Endtime or Day; Unavailable', times should be in format hour:min with am or pm after, with at least 1 day off, each day must have a different start and end time, each day must have at least 4.5 hours of worktime, seperated by one new line, days off are indicated by the word Unavailable, Saturday and Sunday cannot both be days off at the same time",
    max_tokens = 2048,
    temperature = 0.9,
    presence_penalty = 0,
    frequency_penalty = 0,
    )

json_response = json.loads(str(response))
#print(json_response['choices'][0]['text'])

output = json_response['choices'][0]['text'].split("\n")
output[:] = (value for value in output if value != '')


new_output = []
schedule = {} 
for x in output:
    new_output.extend(x.split("; "))
    
    
    #schedule[x[0]].append(x[1])
print(new_output)

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

count = 0
for x in range(len(new_output)):
    if x%2 == 0:
        sheet1.write(0, count, new_output[x])
        count+=1
    else:
        sheet1.write(1,count-1, new_output[x])
    
    

wb.save('OpenAIOutput.xls')
