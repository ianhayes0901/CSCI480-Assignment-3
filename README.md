# CSCI480-Assignment-3
Good day! This will be a tutorial running through the various steps needed to not only take advantage of OpenAI's OpenAPI Python Library and its various functionalities, but also how to specifically use that API to generate schedules via specific prompt crafting, and then saving that in an Excel file. 

---
## Getting Started - Part 1: 

First and foremost, there are a handful of Python libraries that are required in order for this to work, most importantly being the 'openai' library, that can be installed via a pip install in your terminal. (For those not familiar with the format, install as follows: pip install openai)

However, just having the library is not enough to get the API working, as you will also need to supply the API with a personal API key. To get such a key, navigate to the following link: https://openai.com/api/

From there, create an account with OpenAI via your preferred method. Following your completion of account creation and after first signing in, you'll see a tab in the top right corner of your screen next to your profile picture called "Personal", hover your mouse over that tab and a dropdown will appear. We are looking for the "View API Keys" tab. Click that and you will be navigated to the page where you can generate API keys. 

A button will be found towards the center of the page, beneath the table that shows any existing keys (this will be empty if this is your first time generating a key), it will be titled "Create a new secret key". From there, a new window will pop up containing your newly created API key and a button that allows you to copy it to your clipboard. I would suggest saving this somewhere easily accesible, you'll need it in a little bit. 

__NOTE__: Do ___NOT___ leave this key in any files that you intend to upload to Github or the like, as it will automatically invalidate the key. 

--- 
## Getting Started - Part 2:

Now that you've got OpenAI ready to go, we can get into the meat and potatoes of the project itself. Let's get started by getting the one other library you'll likely need installed ready to go. You will be pip installing xlwt, which is a library that enables us to create/write files for Excel. Upon installing that, set up the following import statements in your code: 

    import openai
    import json
    import xlwt
    from xlwt import Workbook

Additionally, if for any reason you're having any issues with libraries not being recognized, I have found the following code works wonders for resolving it: 

    import sys
    import subprocess

    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '<library name>'])

After testing to make sure all libraries are properly recognized and ready to go, the actual coding can begin! 

---

## The Actual Coding Part 1 

The first step is to feed the OpenAI API your API Key so it can properly function, that is done via the following: 

    openai.api_key = "<YOUR API KEY HERE>"
  
From there, you can begin to build the API's request method which should go as follows: 

    response = openai.Completion.create(
        model ="text-davinci-003",
        prompt = "Tell me this is a test",
        max_tokens = 2048,
        )
        
        
To explain a little about what you're seeing: 

      Model: This parameter specifies what specific AI model the API will pass your particular prompt to, in this case, we are choosing a text generation focused one, with this particular text AI being the most capable they have at the current time (01/2023).
      Prompt: The actual messsage you are passing to the AI to get a response returned 
      Max_tokens: the number of tokens capable of being generated between both your prompt and the response. Larger values allow for larger responses/prompt combos, but the best value to work with tends to be 2048 in my experience 

Listed above are the only required paramters that need to be included when creating a Completion request function call, but there are a handful of other optional paramters that can be useful, and that I myself will be using, such as: 

    Temperature: How much risk taking the AI will employ, 0 is basic, 0.9 is more risky. Defaults to 1 if not specified. 
    Presence_penalty: Default 0, range of -2.0 to 2.0. Positive values discourages repeat topics in current text, meaning more diverse answer, negative reinforces/rewards 
    Frequency_penalty: Default 0, range of -2.0 to 2.0. Positive values discourages repeats of lines common in other tokens, negative reinforce/rewards. 

Further documentation and explanation can be found at https://beta.openai.com/docs/api-reference/completions/create

Moving on from that, running a print statement on the code we created above will print an object that should look something like this: 

    {
      "choices": [
        {
          "finish_reason": "stop",
          "index": 0,
          "logprobs": null,
          "text": "\n\nYes, this is a test."
        }
      ],
      "created": 1675041328,
      "id": "cmpl-6eD3YJuWWnsMgoKoc3aSHCn5ZOYJ7",
      "model": "text-davinci-003",
      "object": "text_completion",
      "usage": {
        "completion_tokens": 9,
        "prompt_tokens": 6,
        "total_tokens": 15
      }
   
As you can see, there's a lot of information present there, but specifically, in the "text" section, we can see the API returned a reponse to our prompt of "Tell me this is a test" with "Yes, this is a test". What this means, if we want to clean up the output to be more streamlined, we need to use the JSON library. Specifically as follows: 

    json_response = json.loads(str(response))

This will convert the API returned object into a JSON object that we can then further refine, like in this case: 

    json_response['choices'][0]['text']

This will look specifically at the 'choices' branch of the object, with the combination of the index call of [0] and the ['text'] enabling the return of only the string element of "text", which is "\n\nYes, this is a test". Running the following code: 

    print(json_response['choices'][0]['text'])

Will therefore output this: 

    Yes, this is a test (but with two newlines preceding it, Markdown format is weird) 

Now we can start playing around with prompts to modify what is returned. 

---
## The Actual Coding Part 2 

Proper prompt creation is pivotal towards ensuring that the output that you are looking for is produced by the API, as such, being as specific as possible aids in ensuring that the API doesn't encounter ambiguity or unclear parameters that could cause it to produce unwanted results. 

For example, if I was to give the prompt "Give me a week's schedule", I could get the following output (or something similar, reproducing exact results is diffcult with API) 

    Monday:

    - Wake up
    - Make breakfast
    - Go to work 
    - Have lunch 
    - Attend meetings
    - Work on project
    - Go to gym 
    - Make dinner 
    - Read
    - Get ready for sleep

    Tuesday:

    - Wake up 
    - Make breakfast 
    - Go to work
    - Have lunch
    - Work on project
    - Join a yoga class
    - Make dinner 
    - Read 
    - Get ready for sleep 

    Wednesday:

    - Wake up
    - Make breakfast 
    - Go to work
    - Have lunch 
    - Run errands 
    - Work on project 
    - Go for a walk 
    - Make dinner 
    - Watch a movie 
    - Get ready for sleep 

    Thursday:

    - Wake up 
    - Make breakfast 
    - Go to work 
    - Have lunch 
    - Attend meetings
    - Work on project
    - Go shopping 
    - Make dinner
    - Listen to music
    - Get ready for sleep 

    Friday:

    - Wake up 
    - Make breakfast
    - Go to work
    - Have lunch 
    - Work on project
    - Go to a museum 
    - Make dinner
    - Catch up with friends 
    - Get ready for sleep

    Saturday: 

    - Wake up 
    - Make breakfast 
    - Do chores 
    - Have lunch 
    - Work on a hobby 
    - Go to the park 
    - Make dinner 
    - Read a book 
    - Get ready for sleep 

    Sunday:

    - Wake up 
    - Make breakfast 
    - Go for a hike 
    - Have lunch 
    - Work on a project 
    - Go to the beach 
    - Make dinner 
    - Relax 
    - Get ready for sleep

Now such an output would be useful if one was looking for a general week's activity schedule without any particular times, as this is basically producing an untimed objective list. However, this would not be useful if we were looking to generate start and end times for each day of the week given a particular availability, as this would be of no use. As such, being more precise, like was done in the following prompt: 

"Give me 1 week of a schedule for one employee with the following availability 10:00 am to 8:00 pm in format 'Day; Start Time-Endtime or Day; Unavailable', times should be in format hour:min with am or pm after, all days in the week must not have the same start and end time, each day must have at least 4.5 hours of worktime, seperated by one new line"

Would give me something that could look like this: 

    Monday; 10:00am-6:00pm 
    Tuesday; 11:00am-7:00pm 
    Wednesday; 12:00pm-8:00pm 
    Thursday; 9:30am-5:30pm 
    Friday; 10:30am-6:30pm  
    Saturday; Unavailable 
    Sunday; Unavailable
As you can see, that is much more precise, and would be usable if we were looking to generate a weekly schedule for an employee. But how do we get that string data into an Excel sheet? That's where the xlwt libray comes in! 

First, we've got to prep the data outputted by the OpenAI Completion method. We've previously just printed it to the console, but instead, if we assign it a name, thus turning it into a string object, we can then call more methods on it. Such as the following: 

    output = json_response['choices'][0]['text'].split("\n")
    output[:] = (value for value in output if value != '')
This will not only gives us a name that we can call, but the split() method and the code following it's call will split the string whereever it finds a new line (which seperates each day to a new line) and then goes through the newly created output list object to remoev any '' (blank characters). 

But we're not quite done, as right now, we have a list that looks like this: ['Monday; 10:00am-6:00pm ', 'Tuesday; 11:00am-7:00pm ', 'Wednesday; 12:00pm-8:00pm', 'Thursday; 9:30am-5:30pm','Friday; 10:30am-6:30pm', 'Saturday; Unavailable', 'Sunday; Unavailable'] 
We could simply push this to Excel, but it wouldn't look as nice as it could be, so instead, we need to further split the output into days and times, which is possible via the following: 

    new_output = []
    for x in output:
        new_output.extend(x.split("; "))
        
What that will do is go through each of those previous day+time elements found in output and assign a new day element followed by a time element to the newly created list new_output. The list new_output will now look like this ['Monday', '10:00am-6:00pm', 'Tuesday', '11:00am-7:00pm', 'Wednesday','12:00pm-8:00pm', 'Thursday', '9:30am-5:30pm','Friday', '10:30am-6:30pm', 'Saturday', 'Unavailable', 'Sunday', 'Unavailable']. 

Now ___that___ we can work with. 

And work with it we shall! Via the following code! 

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
    
Wb calls the Workbork() method from the Workbook sublibrary that is a part of xlwt library, which generates a new Excel file, which you can then add to as necessary. We will be adding to it first by creating a new sheet, then, in order to parse our list, we create a count variable and a for loop to go through each element of the new_output list. 

All the days we generated will be on even indices in new_output, and so using modular division in a conditional will allow us to access those elements and then assign them to the first row of Sheet 1, with the column it is assigned to being the value count, which is incremented every time a day is found.

All odd indices contain our times related to the day listed in the index prior to it, and so in the else branch we simply have to write the times values to the 2nd row, with the column instead being count-1 to match it to the correct day. Following a complete pass of new_output, all days and times will be properly added to our newly created Excel file. 

All we then have to do is save the Excel file to make it accessible outside of Python, which is done via the Workbook.save('<FileName>') method. 
  
Congratulations! You have now successfully implemented the OpenAI Library, learned to generate responses via prompts, and then learned how to output that data to Excel. 
 

