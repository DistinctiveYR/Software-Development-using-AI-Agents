import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
import customtkinter
from customtkinter import *
import time 
from textwrap import *

root = CTk()
root.geometry("1650x500")
root.title("Manager")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

wrapper = TextWrapper(width = 50)
context = ""

row = 0
server_row = 0

# client_ip = '127.0.0.1'
# client_port = 999 

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((client_ip,client_port))

# client_socket.send("MANAGER".encode())

# while(True):
#     message = input("Enter the message: ")
#     client_socket.send("DEVELOPER "+message.encode())

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyBm3QEhmxzvyl9Q2IruZAZzxs7CB9bGXAI")

chat_frame = CTkScrollableFrame(master=root,width=1400, height=250)
chat_frame.pack(pady=30)
chat_frame.grid_columnconfigure(0, weight=1)

user_frame = CTkFrame(master=root, width=800, height=1)
user_frame.pack()

chat_frame_2 = CTkScrollableFrame(master=root, width=1400, height=250)
chat_frame_2.pack(pady=30)

user_frame_2 = CTkFrame(master=root, width=800, height=1)
user_frame_2.pack()

description_entry = CTkEntry(master=user_frame, placeholder_text="Tell me about the project and let me explain you", width=800, border_color='white', text_color='white')
description_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

chat_entry = CTkEntry(master=user_frame_2, placeholder_text="Ask about your problem", width=1000, border_color='white', text_color='white')
chat_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)


def response(description):
    global row
    char_length = []

    manager = Agent(role="Manager", max_rpm=20, goal="explain the project create plan for the software projects, suggest ideas on how the project should be executed in the most effecient way and in the minimum time", backstory="You are a manager of a software developer department and you are the best at explaning a project to others managing work and delegating work among your teammates based on their skills", allow_delegation=False, llm=llm)
    manager_task = Task(description=description, agent=manager)

    crew = Crew(tasks=[manager_task], agents=[manager])
    result = crew.kickoff()

    wrapped_result = wrapper.wrap(result)
    result = "".format()

    for word in wrapped_result:
            result += word
            char_length.append(len(word))

    # loader.set(100)
    # loader.destroy()

    text_width = max(char_length)*20
    text_box_height = len(wrapped_result)*5
            
    response_message = CTkTextbox(master=chat_frame, width=text_width, height=text_box_height)
    response_message.insert(index=END, text=result)
    response_message.configure(state="disabled")
    response_message.grid(row=row, column=0, columnspan=3, padx=20, pady=30, sticky=NSEW)
    # response_message.pack()

    row += 100 + text_box_height

    print(result)

def getDescription():
    global row
    char_length = []

    description = description_entry.get()
    
    # response_thread = threading.Thread(target=response, args=(description,))
    # response_thread.start()

    wrapped_description = wrapper.wrap(text=description)
    description = ''.format()

    print("1")

    for word in wrapped_description:
        description += word
        char_length.append(len(word))
    
    
    text_width = max(char_length)*10
    text_box_height = len(wrapped_description)*20
    
    text_message = CTkTextbox(master=chat_frame, width=text_width, height=text_box_height)
    text_message.insert(index=END, text=description)
    text_message.configure(state="disabled")
    text_message.grid(row=row, column=0, columnspan=3, padx=20, pady=30, sticky=NSEW)
    

    row += 100 + text_box_height
    
    # language = combo_box.get()

    # if(language != "None"):
    #     description += "in" + language

    print("Description: \n",description)


    response(description)


    

def sendFileToAssistant():
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

        # sendFile(file_path, context)

        row += 12
        
        print(context)
    except Exception as e:
        print("An error occurred ",e)

def sendToServer():
    pass

def sendDataToServer():
    pass

upload_button_up = CTkButton(master=user_frame, text="+",command=sendFileToAssistant, width=50, hover=True)
upload_button_up.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

send_button = CTkButton(master=user_frame, text="Send",command=getDescription, width=50, hover=True)
send_button.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

upload_button_down = CTkButton(master=user_frame_2, text="+",command=sendToServer, width=50, hover=True)
upload_button_down.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)



send_button_2 = CTkButton(master=user_frame_2, text="Send",command=sendDataToServer, width=50, hover=True)
send_button_2.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)



# description = input("Tell me about the project I will make a plan for it\n")

# task = Task(description=description, agent=manager)

# result = task.execute()
# print("\n-----------------------------------------------------\n")
# print(result)

# print(task.execute())

root.mainloop()