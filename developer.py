from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")

developer = Agent(role="Software Developer",goal="Develop the code in the provided technology and check for any errors and correction in the code",backstory="You are developer who can code in any technology and create the best logics and error free code", llm=llm, allow_delegation=True,verbose=True)

description = "create a snake game in any language which is suitable for it"

task = Task(description=description, agent=developer)

result = task.execute()

# streaming text
# for char in range(len(result)):
#     print(result[:char])