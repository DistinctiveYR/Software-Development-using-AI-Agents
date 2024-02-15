import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

client_ip = '127.0.0.1'
client_port = 999 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_ip,client_port))

client_socket.send("DEVELOPER".encode())

def receive_messages():
    message = client_socket.recv(1024).decode()
    print(message)

threading.Thread(target=receive_messages).start()

while(True):
    message = input("Enter the message: ")
    client_socket.send(message.encode())

    

print(client_socket.recv(1024).decode())

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")

developer = Agent(role="Software Developer",goal="Develop & generate the code in the provided technology and check for any errors and correction in the code",backstory="You are developer who can code in any technology and create the best logics and error free code", llm=llm, allow_delegation=True,verbose=True)

description = input("How can I assist you?\n")

task = Task(description=description, agent=developer)

# print(task.execute())
crew = Crew(tasks=[task],agents=[developer])
result = crew.kickoff()

print(result)

# streaming text
# for char in range(len(result)):
#     print(result[:char])