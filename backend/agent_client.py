# backend/agent_client.py
import requests
import os
from typing import Dict
from openai import OpenAI
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from crewai import Crew, Process
from langchain_openai import ChatOpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.environ.get("OPENAI_MODEL_NAME")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY")

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

def get_nse_stock_overview(stock_symbol):
    
    # OpenAI model
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    prompt = f"""
    You are a financial analyst with more than 15 years of experience. Given the NSE stock symbol "{stock_symbol}", 
    provide a clear and concise overview containing:

    1. **Company Overview** – What the company does, sector, and key products/services.
    2. **Market Capitalization** – Classify as Large-cap, Mid-cap, or Small-cap based on latest available data.
    3. **Recent Stock Performance** – Mention general trend over the past few months (uptrend, downtrend, volatile, stable).
    4. **Key Strengths & Risks** – Summarize 2-3 points for each.
    5. **Industry Position** – Describe its market position relative to peers.
    6. **Future Outlook** – Brief insights based on general market sentiment.

    Keep the tone professional and easy to understand and within word limit of 200 words.
    Give the response in a single paragraph.
    If you cannot find reliable data, mention it explicitly.
    """

    response = client.responses.create(
        model=OPENAI_MODEL_NAME,
        input=prompt,
        temperature=0
    )

    return response.output_text

def create_agents():
    company_researcher_agent = Agent(
        role="Company Researcher",
        goal="Gather and analyze comprehensive information about a specified company.",
        backstory="An expert in corporate research, this agent delves into company profiles, "
                  "financial statements, market position, and sector trends to provide a "
                  "holistic overview. It is skilled at synthesizing data from various sources "
                  "to create a clear and concise company profile.",
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool, search_tool]
    )

    data_analyst_agent = Agent(
        role="Data Analyst",
        goal="Monitor and analyze market data in real-time to identify trends and predict market movements.",
        backstory="Specializing in financial markets, this agent uses statistical modeling and machine learning "
                  "to provide crucial insights. With a knack for data, the Data Analyst Agent is the cornerstone "
                  "for informing trading decisions.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )
    
    trading_strategy_agent = Agent(
        role="Trading Strategy Developer",
        goal="Develop and test various trading strategies based on insights from the Data Analyst Agent.",
        backstory="Equipped with a deep understanding of financial markets and quantitative analysis, this agent "
                  "devises and refines trading strategies. It evaluates the performance of different approaches "
                  "to determine the most profitable and risk-averse options.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )
    
    execution_agent = Agent(
        role="Trade Advisor",
        goal="Suggest optimal trade execution strategies based on approved trading strategies.",
        backstory="This agent specializes in analyzing the timing, price, and logistical details of potential trades. "
                  "By evaluating these factors, it provides well-founded suggestions for when and how trades should be "
                  "executed to maximize efficiency and adherence to strategy.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )
    
    risk_management_agent = Agent(
        role="Risk Advisor",
        goal="Evaluate and provide insights on the risks associated with potential trading activities.",
        backstory="Armed with a deep understanding of risk assessment models and market dynamics, this agent "
                  "scrutinizes the potential risks of proposed trades. It offers a detailed analysis of risk "
                  "exposure and suggests safeguards to ensure that trading activities align with the firm’s risk tolerance.",
        verbose=True,
        allow_delegation=True,
        tools=[scrape_tool, search_tool]
    )
    
    return company_researcher_agent, data_analyst_agent, trading_strategy_agent, execution_agent, risk_management_agent

def create_tasks(company_researcher_agent, data_analyst_agent, trading_strategy_agent, execution_agent, risk_management_agent):
    company_analysis_task = Task(
        description=(
            "Provide a detailed overview of the company behind the stock ({stock_selection}). "
            "Include its sector, market capitalization (large-cap, mid-cap, or small-cap), "
            "what the company does, and its primary business activities."
        ),
        expected_output=(
            "A concise report summarizing the company's profile, including its sector, "
            "market cap classification, and core business operations."
        ),
        agent=company_researcher_agent,
    )

    data_analysis_task = Task(
        description=(
            "Continuously monitor and analyze market data for the selected stock ({stock_selection}). "
            "Use statistical modeling and machine learning to identify trends and predict market movements."
        ),
        expected_output=(
            "Insights and alerts about significant market opportunities or threats for {stock_selection}."
        ),
        agent=data_analyst_agent,
    )
    
    strategy_development_task = Task(
        description=(
            "Develop and refine trading strategies based on the insights from the Data Analyst and "
            "user-defined risk tolerance ({risk_tolerance}). Consider trading preferences ({trading_strategy_preference})."
        ),
        expected_output=(
            "A set of potential trading strategies for {stock_selection} that align with the user's risk tolerance."
        ),
        agent=trading_strategy_agent,
    )
    
    execution_planning_task = Task(
        description=(
            "Analyze approved trading strategies to determine the best execution methods for {stock_selection}, "
            "considering current market conditions and optimal pricing."
        ),
        expected_output=(
            "Detailed execution plans suggesting how and when to execute trades for {stock_selection}."
        ),
        agent=execution_agent,
    )
    
    risk_assessment_task = Task(
        description=(
            "Evaluate the risks associated with the proposed trading strategies and execution plans for {stock_selection}. "
            "Provide a detailed analysis of potential risks and suggest mitigation strategies."
        ),
        expected_output=(
            "A comprehensive risk analysis report detailing potential risks and mitigation recommendations for {stock_selection}."
        ),
        agent=risk_management_agent,
    )
    
    return company_analysis_task, data_analysis_task, strategy_development_task, execution_planning_task, risk_assessment_task



def call_agent_api(payload: Dict, timeout=60) -> Dict:
    """
    POST the payload to your Agentic AI endpoint and return JSON.
    Expected to return: {"markdown_report": "## ..."}
    """
    company_researcher_agent, data_analyst_agent, trading_strategy_agent, execution_agent, risk_management_agent = create_agents()
    company_analysis_task, data_analysis_task, strategy_development_task, execution_planning_task, risk_assessment_task = create_tasks(
        company_researcher_agent, data_analyst_agent, trading_strategy_agent, execution_agent, risk_management_agent
    )
    
    # Define the crew with agents and tasks
    financial_trading_crew = Crew(
        agents=[
            company_researcher_agent,
            data_analyst_agent,
            trading_strategy_agent,
            execution_agent,
            risk_management_agent
        ],
        tasks=[
            company_analysis_task,
            data_analysis_task,
            strategy_development_task,
            execution_planning_task,
            risk_assessment_task
        ],
        manager_llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=OPENAI_MODEL_NAME, temperature=0),
        process=Process.hierarchical,
        verbose=True
    )
    
    # Example data for kicking off the process
    financial_trading_inputs = {
        'stock_selection': payload.get("stock_symbol", "RELIANCE"),
        'initial_capital': payload.get("capital", 10000),
        'risk_tolerance': payload.get("risk_tolerance", "Medium"),
        'trading_strategy_preference': payload.get("strategy", "Swing Trading"),
        'news_impact_consideration': payload.get("news_impact", True)
    }
    
    result = financial_trading_crew.kickoff(inputs=financial_trading_inputs)
    
    overview = get_nse_stock_overview(payload.get("stock_symbol", "RELIANCE"))
    
    return {"markdown_report": result, "stock_overview": overview}