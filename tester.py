from crewai import Crew, Process, Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI

description = input("Provide the code: ")

llm = ChatGoogleGenerativeAI(model="gemini-pro",verbose=True,temperature=0.6,google_api_key="AIzaSyCJKrxjDXGANCtcW7CCR1n2h4L7EbxUS9k")

tester = Agent(role="Software Tester",goal="Test the code for any errors, generate the corrected code and test cases for it",backstory="You are a code tester who hates incorrect code and love an error free code so you always correct the code", llm=llm, verbose=True, allow_delegation=True)

task = Task(description=description, agent=tester)

crew = Crew(tasks=[task], agents=[tester])

print(crew.kickoff())