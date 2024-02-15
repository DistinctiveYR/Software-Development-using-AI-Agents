import socket, threading
from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

def getTool():
    tool = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")
    return tool

client_ip = '127.0.0.1'
client_port = 999 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((client_ip,client_port))

client_socket.send("MANAGER".encode())

while(True):
    message = input("Enter the message: ")
    client_socket.send("DEVELOPER "+message.encode())

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")

tool = getTool()

manager = Agent(role="Manager", goal="explain the project create plan for the software projects, suggest ideas on how the project should be executed in the most effecient way and in the minimum time", backstory="You are a manager of a software developer department and you are the best at explaning a project to others managing work and delegating work among your teammates based on their skills", allow_delegation=False, llm=llm)

description = input("Tell me about the project I will make a plan for it\n")

task = Task(description=description, agent=manager)

result = task.execute()
print("\n-----------------------------------------------------\n")
print(result)

# print(task.execute())