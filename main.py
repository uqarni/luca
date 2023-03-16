import streamlit as st
from functions import ideator
import json
import os
import sys
from datetime import datetime

def main():
    # Create a title for the chat interface
    st.title("Tara Ideator Bot")
    st.write("This bot is still in alpha. To get started, first click the button below.")
    
    if st.button('Click to Start or Restart'):
        st.write("Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?")
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
                {"role": "system", "content": "You are a quick-witted entrepeneur named Tara who helps people think of new app ideas based on their business or hobby. You ask clarifying questions about their job and hobby, then guide them towards ideas. Avoid giving giving them too many app ideas; make it interactive and shepherd them through the process. Keep your responses brief. If the user is not responding posivitely, switch to asking clarifying questions for a bit before proceeding."},
                {"role": "assistant", "content": "Hi! This is Tara. Seems like you need help coming up with an idea! Let's do this. First, what's your job?"}
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


    