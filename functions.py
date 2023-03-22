#generate openai response; returns messages with openai response
def ideator(messages):
  import openai
  import os
  key = os.environ.get("OPENAI_API_KEY")
  openai.api_key = key

  result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= messages
  )
  response = result["choices"][0]["message"]["content"]
  response = {
    "role": "assistant", 
    "content": response
  }
  messages.append(response)

  return messages


#prompt user with botresponse in terminal and ask for an input. returns messages with human response
#change this from input function to streamlit function
def terminaltalker(messages):

  botresponse = messages[-1]["content"]
  userresponse = input(botresponse+"\n")
  messages.append(
  {
    "role": "user",
    "content": userresponse
  }
  )
  return messages

#starts terminal conversation. Respond with exit() to exit. 
def terminalbot():
    #initialize message
    messages = [
                {"role": "system", "content": "You are an AI who helps Mike, a LegalZoom tax advisor, prepare for his TAP calls. TAP Calls, which stands for Tax Advisory Plan Calls, are phone calls that LegalZoom customers schedule with our Tax advisors. Today, Mike has 3 TAP calls today: one with Susan at 11am about state and local taxes in Texas, who formed an LLC with us in 2020, another with Tim at 12pm about his employees payroll in Ohio, who is a new customer who formed an LLC with us in 2022 and has also purchased tax return preparation services from us, and last Jane at 2pm about her tax return, who had a bad call in her last TAP call with another advisor. If Mike asks any details not included in this prompt, just respond with some version of [Unfortunately I'm just in alpha and don't yet have access to that info. If you'd like access to it, get Uzair Qarni a job in LegalZoom technology and he'll build this.]"},
                {"role": "assistant", "content": "Hey Mike. Let's get you ready for your TAP calls. Ask me about your calls today."}
          ]
    while True:
       messages = terminaltalker(messages)
       if messages[-1]["content"] == "exit()":
          break
       ideator(messages)