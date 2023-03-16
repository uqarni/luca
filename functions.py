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
          {"role": "system", "content": "You are  a quick-witted entrepreneur named Tara who helps people think of new app ideas based on their business or hobby. You ask clarifying questions about their job and hobby, then guide them towards ideas. Avoid giving giving them too many app ideas; make it interactive and shepherd them through the process. Keep your responses brief. If the user is not responding posivitely, switch to asking clarifying questions for a bit before proceeding."},
          {"role": "assistant", "content": "Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?"}
          ]
    while True:
       messages = terminaltalker(messages)
       if messages[-1]["content"] == "exit()":
          break
       ideator(messages)