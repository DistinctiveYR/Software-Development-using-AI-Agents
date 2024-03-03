import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from customtkinter import *
import customtkinter
from tkinter import *
import tkinter
from textwrap import *
import time

wrapper = TextWrapper(width=50)

row = 0
assitant_row = 0
context = ""

root = CTk()
root.geometry("1650x500")
root.title("Tester")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

chat_frame = CTkScrollableFrame(master=root,width=1400, height=250)
chat_frame.pack(pady=30)

user_frame = CTkFrame(master=root, width=800, height=1)
user_frame.pack()

chat_frame_2 = CTkScrollableFrame(master=root, width=1400, height=250)
chat_frame_2.pack(pady=30)

user_frame_2 = CTkFrame(master=root, width=800, height=1)
user_frame_2.pack()

# client_ip = '127.0.0.1'
# client_port = 999 

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((client_ip,client_port))

# client_socket.send("TESTER".encode())

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyA6EkQPKKMlBVnPyD51-jEZmamHnu_l_jA")

description_entry = CTkEntry(master=user_frame, placeholder_text="Send the code for generating test cases", width=800, border_color='white', text_color='white')
description_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

chat_entry = CTkEntry(master=user_frame_2, placeholder_text="Ask about your problem", width=1000, border_color='white', text_color='white')
chat_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

def receiveMessages():
    message = client_socket.recv(1024).decode()

    while(True):
        if(message == 'FILE'):
            file_content = client_socket.recv(1024).decode()
            

def response(description):
    global assitant_row
    char_length = []

    tester_agent = Agent(role="Software Tester",goal="Test the code for any errors, generate the corrected code and test cases for it",backstory="You are a code tester who hates incorrect code and love an error free code so you always correct the code", llm=llm, verbose=True, allow_delegation=True, max_rpm=20)
    task = Task(description=description, agent=tester_agent)

    crew = Crew(tasks=[task], agents=[tester_agent])
    result = crew.kickoff()

    wrapped_result = wrapper.wrap(result)
    result = "".format()

    for word in wrapped_result:
            result += word
            char_length.append(len(word))

    # loader.set(100)
    # loader.destroy()

    text_width = max(char_length)*10
    text_box_height = len(wrapped_result)*20
            
    response_message = CTkTextbox(master=chat_frame, width=text_width, height=text_box_height)
    response_message.insert(index=END, text=result)
    response_message.configure(state="disabled")
    response_message.grid(row=assitant_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

    assitant_row += 100 + text_box_height

    print(result)


def getDescription():
    global row
    description = description_entry.get()
    char_length = []
    
    wrapped_description = wrapper.wrap(text=description)
    description = ''.format()


    for word in wrapped_description:
        description += word
        char_length.append(len(word))
    
    
    text_width = max(char_length)*10
    text_box_height = len(wrapped_description)*20
    
    text_message = CTkTextbox(master=chat_frame, width=text_width, height=text_box_height)
    text_message.insert(index=END, text=description)
    text_message.configure(state="disabled")
    text_message.grid(row=row, column=70, columnspan=3, padx=20, pady=30, sticky=NE)

    row += 100 + text_box_height

    response(description=description)


def sendFile(file_path, content):
    index = file_path.rindex("\\")
    file_name = file_path[index:]
    client_socket.send(("FILE: ",file_name).encode())
    time.sleep(1)
    client_socket.send(content.encode())

def uploadFiles():
    global row, context
    file_path = filedialog.askopenfilename()
    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: ",file_path
        text_message = CTkTextbox(master=chat_frame, width=(len(text)*10), height=10)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        sendFile(file_path, context)

        row += 12
        
        print(context)
    except Exception as e:
        print("An error occurred ",e)

def sendData():
    message = chat_entry.get()

    if(message != ""):
        client_socket.send(message.encode())
    
    else:
        tkinter.messagebox.showinfo("Error","Empty message cannot be sent")

upload_button = CTkButton(master=user_frame_2, text="+",command=uploadFiles, width=50, hover=True)
upload_button.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

send_button = CTkButton(master=user_frame, text="Send",command=getDescription, width=50, hover=True)
send_button.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

send_button_2 = CTkButton(master=user_frame_2, text="Send",command=sendData, width=50, hover=True)
send_button_2.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

# description = input("Provide the code: ")

# tester = Agent(role="Software Tester",goal="Test the code for any errors, generate the corrected code and test cases for it",backstory="You are a code tester who hates incorrect code and love an error free code so you always correct the code", llm=llm, verbose=True, allow_delegation=True)

# task = Task(description=description, agent=tester)

# crew = Crew(tasks=[task], agents=[tester])

# print(crew.kickoff())

root.mainloop()