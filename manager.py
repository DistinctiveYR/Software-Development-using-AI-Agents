from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

def getTool():
    tool = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")
    return tool


llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")

tool = getTool()

manager = Agent(role="Manager", goal="Plan the projects, guide others to succesfully accomplish the project, delegate th work between your team members", backstory="You are a manager of a software developer department and you are the best at managing work and delegating work among your teammates based on  their skills", allow_delegation=False, llm=llm)

description = "snake game is to be developed suggest the best technologies? explain your plan according to the project"

task = Task(description=description, agent=manager)

for char in task.execute():
    print(char)
# print(task.execute())