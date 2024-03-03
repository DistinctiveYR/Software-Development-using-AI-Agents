import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from customtkinter import *
from tkinter import *
import customtkinter
from textwrap import *
import time

languages = ['None','Python','Java','MySQl','Javascript']
row = 0
server_row = 0
file_name = ""
context = ""
receiver = "MANAGER"
sender = "DEVELOPER"

root = CTk()
root.title("Developer")
root.geometry("1650x500")
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyA3HpbYVmRiLl4SkthICYI_x_9lGfoseyc")
developer = Agent(role="Software Developer",goal="",backstory="You are developer who can code in any technology and create the best logics and error free code", llm=llm, allow_delegation=True,verbose=True)
tester = Agent(role="Software Tester", goal="Find errors and generate a corrected code", backstory="You hate any type of errors or irregularly written code so you always correct it & generate the same code in corrected way", llm=llm, allow_delegation=True, verbose=True)

wrapper = TextWrapper(width=50)

client_ip = '127.0.0.1'
client_port = 999 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_ip,client_port))
client_socket.send("DEVELOPER".encode())

chat_frame = CTkScrollableFrame(master=root, width=1400, height=250)
chat_frame.pack(pady=30)

frame = CTkFrame(master=root, width=800, height=1)
frame.pack()

chat_frame2 = CTkScrollableFrame(master=root, width=1400, height=250)
chat_frame2.pack(pady=30)

frame2 = CTkFrame(master=root, width=800, height=1)
frame2.pack()

description_entry = CTkEntry(master=frame, placeholder_text="Description about the task to be executed", width=800, border_color='white', text_color='white')
description_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)

combo_box = CTkComboBox(master=frame,values=languages)
combo_box.grid(row=0, column=5, columnspan=3, padx=20, pady=30, sticky=NE)


query_entry = CTkEntry(master=frame2, placeholder_text="Send message to your manager", width=1000, border_color='white', text_color='white')
query_entry.grid(row=0, column=1, columnspan=3, padx=20, pady=30, sticky=NE)


def response(description):
    global context, row
    developer_task = Task(description=description, agent=developer)
    # tester_task = Task(description="Find errors, correct the code & generate whole corrected code & if no errors are found regenerate the same code", agent=tester)
    char_length = []

    loader = CTkProgressBar(master=chat_frame, width=300,height=10)
    loader.set(0)
    loader.grid()
    loader.start()

    if(context != ""):
        developer.goal = "Develop & generate the code in the provided technology and check for any errors and correction in the code with the context\ncontext: " + context

    else:
        developer.goal = "Develop & generate the code in the provided technology and check for any errors and correction in the code"

    # try:
    print("5")
    crew = Crew(tasks=[developer_task], agents=[developer], verbose=True, process=Process.sequential)
    result = crew.kickoff()
    print("6")
    
    wrapped_result = wrapper.wrap(result)
    result = "".format()

    for word in wrapped_result:
            result += word
            char_length.append(len(word))

    print(result)

    loader.set(100)
    loader.destroy()

    text_width = max(char_length)*10
    text_box_height = len(wrapped_result)*20
            
    response_message = CTkTextbox(master=chat_frame, width=text_width, height=text_box_height)
    response_message.insert(index=END, text=result)
    response_message.configure(state="disabled")
    response_message.grid(row=row, column=5, columnspan=3, padx=20, pady=30, sticky=NSEW)

    row += 100 + text_box_height

    # except Exception as e:
    #     print("An error occured while responding to the description: ",e)

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
    text_message.grid(row=row, column=70, columnspan=3, padx=20, pady=30, sticky=NSEW)

    row += 100 + text_box_height
    
    language = combo_box.get()

    if(language != "None"):
        description += "in" + language

    print("Description: \n",description)

    print("2")

    response(description)

    print("3")
    # response_thread.join()
    print("4")

def sendMessage():
    global file_name, context, sender, receiver, server_row

    if(file_name != "" and context != ""):
        message = sender + ":" + receiver + ":" + file_name + ":" + context + ":" + query_entry.get()
        client_socket.send(message.encode())

        
        text_message = CTkTextbox(master=chat_frame2, width=(len(message)*10), height=10)
        text_message.insert(index=END, text=message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=15, columnspan=3, padx=20, pady=30, sticky=NSEW)

        server_row += 12

        context = ""
    
    elif(query_entry.get() != ""):
        message = sender + ":" + receiver + ":" + query_entry.get()
        client_socket.send(message.encode())
        
        text_message = CTkTextbox(master=chat_frame2, width=(len(message)*10), height=10)
        text_message.insert(index=END, text=message)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=15, columnspan=3, padx=20, pady=30, sticky=NSEW)

        server_row += 12

    else:
        print("Message cannot be empty !")

  

def uploadFiles():
    global row, context, file_name
    file_path = filedialog.askopenfilename()

    index = file_path.rindex("/")+1
    file_name = file_path[index:]

    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: ",file_path
        text_message = CTkTextbox(master=chat_frame, width=(len(text)*10), height=10)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=row, column=5, columnspan=3, padx=20, pady=30, sticky=NSEW)

        row += 12
        
        print(context)

    except Exception as e:
        print("An error occurred ",e)

def shareFiles():
    global server_row, context, file_name
    file_path = filedialog.askopenfilename()

    print(file_path)

    index = file_path.rindex("/")+1
    file_name = file_path[index:]
    
    try:
        with open(file_path) as file:
            context = file.read()

        text = "You uploaded a file: " + file_path
        text_message = CTkTextbox(master=chat_frame2, width=(len(text)*10), height=10)
        text_message.insert(index=END, text=text)
        text_message.configure(state="disabled")
        text_message.grid(row=server_row, column=5, columnspan=3, padx=20, pady=30, sticky=NE)

        # sendFile(file_path, context)

        server_row += 12
        
        print(context)

    except Exception as e:
        print("An error occurred ",e)


file_uploader = CTkButton(master=frame, text="+",command=uploadFiles, width=50, hover=True)
file_uploader.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

share_file = CTkButton(master=frame2, text="Share Files",command=shareFiles, width=50, hover=True)
share_file.grid(row=0, column=8, columnspan=5, padx=20, pady=30, sticky=NE)

send_button = CTkButton(master=frame, text="Send",command=getDescription, width=50, hover=True)
send_button.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

send_button2 = CTkButton(master=frame2, text="Send",command=sendMessage, width=50, hover=True)
send_button2.grid(row=0, column=15, columnspan=5, padx=20, pady=30, sticky=NE)

def receiveMessages():
    print("Receiving messages")
    while(True):
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        
        except ConnectionResetError as c:
            print(c)

threading.Thread(target=receiveMessages).start()

root.mainloop()