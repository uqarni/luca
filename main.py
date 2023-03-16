import streamlit as st
from functions import ideator
import json
import os
import sys
from datetime import datetime

def main():
    # Create a title for the chat interface
    st.title("Mike Town's TAP Call Assistant Bot")
    st.write("This bot is a proof of concept. To get started, first click the button below before each new session.")
    
    if st.button('Click to Start or Restart'):
        st.write("Hey Mike. Let's get you ready for your TAP calls. Ask me about your calls today. ")
        restart_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('database.jsonl', 'r') as db, open('archive.jsonl','a') as arch:
        # add reset 
            arch.write(json.dumps({"restart": restart_time}) + '\n')
        #copy each line from db to archive
            for line in db:
                arch.write(line)

        #clear database to only first two lines
        with open('database.jsonl', 'w') as f:
        # Override database with initial json files
            messages = [
                {"role": "system", "content": "You are an AI who helps Mike, a LegalZoom tax expert, prepare for his TAP calls. TAP Calls, which stands for Tax Advisory Plan Calls, are phone calls that LegalZoom customers schedule with our Tax advisors. Today, Mike has 3 TAP calls: one with Susan at 11am about state and local taxes in Texas, who formed an LLC with us in 2020, another with Tim at 12pm about his employees payroll in Ohio, who is a new customer who formed an LLC with us in 2022 and has also purchased tax return preparation services from us, and last Jane at 2pm about her tax return, who had a bad call in her last TAP call with another advisor. If Mike asks any details, just respond with some version of [Unfortunately I'm just in alpha and don't yet have access to that info. If you'd like access to it, get Uzair Qarni a job in LegalZoom technology and he'll build this.]"},
                {"role": "assistant", "content": "Hey Mike. Another day at LegalZoom. Let's get you ready for your TAP calls today. Ask me when you have calls today, with who, and what they want to know about. "}
            ]
            f.write(json.dumps(messages[0])+'\n')
            f.write(json.dumps(messages[1])+'\n')



    #initialize messages list and print opening bot message
    #st.write("Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?")

    # Create a text input for the user to enter their message and append it to messages
    userresponse = st.text_input("Enter your message")
    

    # Create a button to submit the user's message
    if st.button("Send"):
        #prep the json
        newline = {"role": "user", "content": userresponse}

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(newline) + '\n')

        #extract messages out to list
        messages = []

        with open('database.jsonl', 'r') as f:
            for line in f:
                json_obj = json.loads(line)
                messages.append(json_obj)

        #generate OpenAI response
        messages = ideator(messages)

        #append to database
        with open('database.jsonl', 'a') as f:
        # Write the new JSON object to the file
            f.write(json.dumps(messages[-1]) + '\n')



        # Display the response in the chat interface
        string = ""

        for message in messages[1:]:
            string = string + message["role"] + ": " + message["content"] + "\n\n"
        st.write(string)
            

if __name__ == '__main__':
    main()


    