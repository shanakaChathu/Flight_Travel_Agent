import os 
from dotenv import load_dotenv, find_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents.output_parsers import ReActJsonSingleInputOutputParser
from langchain.tools.render import render_text_description_and_args
from langchain_openai import ChatOpenAI
import streamlit as st 
from langchain_community.agent_toolkits.amadeus.toolkit import AmadeusToolkit


_ = load_dotenv(find_dotenv()) # read local .env file


toolkit = AmadeusToolkit()
tools = toolkit.get_tools()

llm = ChatOpenAI(temperature=0,model='gpt-4')

prompt = hub.pull("hwchase17/react-json")
agent = create_react_agent(
    llm,
    tools,
    prompt,
    tools_renderer=render_text_description_and_args,
    output_parser=ReActJsonSingleInputOutputParser(),
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

st.title("Unlocking Seamless Travel: Navigating Flight Queries with Ease")
question_input = st.text_area("Enter your flight-related inquiry below.")
if st.button("Submit"):
    
    answer=agent_executor.invoke({"input": question_input})
    st.markdown(answer['output'])
