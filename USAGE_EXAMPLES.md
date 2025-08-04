# Master AI Agentic Engineering - Usage Examples

This document provides comprehensive usage examples and tutorials for all modules in the Master AI Agentic Engineering course codebase.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Module 1: Foundations Examples](#module-1-foundations-examples)
3. [Module 2: OpenAI Agents SDK Examples](#module-2-openai-agents-sdk-examples)
4. [Module 3: CrewAI Examples](#module-3-crewai-examples)
5. [Module 4: LangGraph Examples](#module-4-langgraph-examples)
6. [Module 5: AutoGen Examples](#module-5-autogen-examples)
7. [Module 6: MCP Examples](#module-6-mcp-examples)
8. [Advanced Integration Patterns](#advanced-integration-patterns)
9. [Troubleshooting Common Issues](#troubleshooting-common-issues)

---

## Getting Started

### Environment Setup

First, ensure you have all required environment variables:

```bash
# Create .env file in project root
cat > .env << EOF
# Core OpenAI API
OPENAI_API_KEY=your_openai_api_key_here

# Pushover for notifications
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user_key

# SendGrid for email
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_sender_email

# Search capabilities
SERPER_API_KEY=your_serper_api_key

# Alternative AI models (optional)
DEEPSEEK_API_KEY=your_deepseek_api_key
GROK_API_KEY=your_grok_api_key
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
EOF
```

### Installation

```bash
# Install dependencies using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

---

## Module 1: Foundations Examples

### Basic Personal Assistant

Create a personal AI assistant that represents you:

```python
# 1_foundations/example_personal_assistant.py
import os
from dotenv import load_dotenv
from app import Me
import gradio as gr

load_dotenv()

def create_personal_assistant():
    """Create and launch a personal AI assistant"""
    
    # Ensure required files exist
    os.makedirs("me", exist_ok=True)
    
    # Create sample files if they don't exist
    if not os.path.exists("me/summary.txt"):
        with open("me/summary.txt", "w") as f:
            f.write("""
            I am an AI engineer with expertise in machine learning and software development.
            I have experience building AI agents and working with various AI frameworks.
            I enjoy helping people learn about AI and solve complex technical problems.
            """)
    
    # Initialize the assistant
    me = Me()
    
    # Create Gradio interface
    interface = gr.ChatInterface(
        me.chat,
        type="messages",
        title="Personal AI Assistant",
        description="Chat with my personal AI assistant"
    )
    
    return interface

if __name__ == "__main__":
    app = create_personal_assistant()
    app.launch(debug=True, share=False)
```

### Custom Tool Integration

Add custom tools to your assistant:

```python
# 1_foundations/example_custom_tools.py
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def calculate_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number"""
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def get_weather_mock(city: str) -> dict:
    """Mock weather function - replace with real API"""
    return {
        "city": city,
        "temperature": "22°C",
        "condition": "Sunny",
        "humidity": "65%"
    }

# Tool definitions
fibonacci_tool = {
    "type": "function",
    "function": {
        "name": "calculate_fibonacci",
        "description": "Calculate the nth Fibonacci number",
        "parameters": {
            "type": "object",
            "properties": {
                "n": {
                    "type": "integer",
                    "description": "The position in the Fibonacci sequence"
                }
            },
            "required": ["n"]
        }
    }
}

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather_mock",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name"
                }
            },
            "required": ["city"]
        }
    }
}

class CustomAssistant:
    def __init__(self):
        self.client = OpenAI()
        self.tools = [fibonacci_tool, weather_tool]
        self.available_functions = {
            "calculate_fibonacci": calculate_fibonacci,
            "get_weather_mock": get_weather_mock
        }
    
    def chat(self, message: str) -> str:
        """Chat with the assistant using custom tools"""
        messages = [
            {"role": "system", "content": "You are a helpful assistant with access to mathematical and weather tools."},
            {"role": "user", "content": message}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=self.tools
        )
        
        message = response.choices[0].message
        
        # Handle tool calls
        if message.tool_calls:
            messages.append(message)
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if function_name in self.available_functions:
                    function_response = self.available_functions[function_name](**function_args)
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(function_response),
                        "tool_call_id": tool_call.id
                    })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return final_response.choices[0].message.content
        
        return message.content

# Usage example
if __name__ == "__main__":
    assistant = CustomAssistant()
    
    # Test Fibonacci
    print("User: What's the 10th Fibonacci number?")
    print("Assistant:", assistant.chat("What's the 10th Fibonacci number?"))
    
    print("\nUser: What's the weather like in London?")
    print("Assistant:", assistant.chat("What's the weather like in London?"))
```

---

## Module 2: OpenAI Agents SDK Examples

### Basic Research Agent

Create a research agent that can investigate topics:

```python
# 2_openai/example_research_agent.py
import asyncio
from deep_research.deep_research import run
from deep_research.email_agent import send_email

async def research_example():
    """Example of using the research system"""
    
    # Define research topics
    topics = [
        "Latest developments in quantum computing",
        "Impact of AI on healthcare industry",
        "Sustainable energy technologies 2024"
    ]
    
    results = []
    
    for topic in topics:
        print(f"\n🔍 Researching: {topic}")
        print("=" * 50)
        
        try:
            result = await run(topic)
            results.append({
                "topic": topic,
                "report": result,
                "status": "success"
            })
            print(f"✅ Research completed for: {topic}")
            
        except Exception as e:
            print(f"❌ Error researching {topic}: {e}")
            results.append({
                "topic": topic,
                "error": str(e),
                "status": "error"
            })
    
    # Generate summary report
    summary = generate_research_summary(results)
    print("\n📊 Research Summary:")
    print(summary)
    
    # Optionally send via email
    # send_email("Research Summary", summary)
    
    return results

def generate_research_summary(results):
    """Generate a summary of all research results"""
    summary = "# Research Summary Report\n\n"
    
    successful = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] == "error"]
    
    summary += f"## Overview\n"
    summary += f"- Total topics researched: {len(results)}\n"
    summary += f"- Successful: {len(successful)}\n"
    summary += f"- Failed: {len(failed)}\n\n"
    
    if successful:
        summary += "## Successful Research\n\n"
        for result in successful:
            summary += f"### {result['topic']}\n"
            summary += f"{result['report'][:500]}...\n\n"
    
    if failed:
        summary += "## Failed Research\n\n"
        for result in failed:
            summary += f"### {result['topic']}\n"
            summary += f"Error: {result['error']}\n\n"
    
    return summary

if __name__ == "__main__":
    asyncio.run(research_example())
```

### Multi-Agent Research Pipeline

Create a pipeline with multiple specialized agents:

```python
# 2_openai/example_multi_agent_pipeline.py
import asyncio
from typing import List, Dict
from openai import AsyncOpenAI
import json

class ResearchPipeline:
    """Multi-agent research pipeline with specialized roles"""
    
    def __init__(self):
        self.client = AsyncOpenAI()
        self.agents = {
            "planner": self.create_planner_agent(),
            "researcher": self.create_researcher_agent(),
            "analyst": self.create_analyst_agent(),
            "writer": self.create_writer_agent()
        }
    
    def create_planner_agent(self):
        """Agent that creates research plans"""
        return {
            "role": "Research Planner",
            "system_prompt": """You are a research planning specialist. Your job is to break down 
            research topics into specific, actionable research questions. Create a structured plan 
            with 3-5 focused research questions that will comprehensively cover the topic."""
        }
    
    def create_researcher_agent(self):
        """Agent that gathers information"""
        return {
            "role": "Information Researcher", 
            "system_prompt": """You are an information gathering specialist. For each research 
            question, provide detailed findings with specific facts, statistics, and examples. 
            Focus on recent, credible information."""
        }
    
    def create_analyst_agent(self):
        """Agent that analyzes and synthesizes information"""
        return {
            "role": "Research Analyst",
            "system_prompt": """You are a research analyst. Your job is to analyze the gathered 
            information, identify patterns, draw insights, and highlight key findings. Look for 
            trends, implications, and connections between different pieces of information."""
        }
    
    def create_writer_agent(self):
        """Agent that creates final reports"""
        return {
            "role": "Report Writer",
            "system_prompt": """You are a professional report writer. Create comprehensive, 
            well-structured reports that synthesize all research findings into a coherent narrative. 
            Include executive summary, key findings, analysis, and conclusions."""
        }
    
    async def run_agent(self, agent_key: str, prompt: str, context: str = "") -> str:
        """Run a specific agent with given prompt and context"""
        agent = self.agents[agent_key]
        
        messages = [
            {"role": "system", "content": agent["system_prompt"]},
        ]
        
        if context:
            messages.append({"role": "user", "content": f"Context from previous steps:\n{context}"})
        
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def execute_pipeline(self, topic: str) -> Dict:
        """Execute the full research pipeline"""
        results = {"topic": topic, "steps": {}}
        
        # Step 1: Planning
        print(f"🎯 Planning research for: {topic}")
        plan_prompt = f"Create a detailed research plan for the topic: '{topic}'"
        plan = await self.run_agent("planner", plan_prompt)
        results["steps"]["plan"] = plan
        print("✅ Research plan created")
        
        # Step 2: Research
        print("🔍 Gathering information...")
        research_prompt = f"Based on this research plan, gather detailed information for the topic '{topic}':\n{plan}"
        research = await self.run_agent("researcher", research_prompt, plan)
        results["steps"]["research"] = research
        print("✅ Information gathered")
        
        # Step 3: Analysis
        print("📊 Analyzing findings...")
        analysis_prompt = f"Analyze the research findings for '{topic}'"
        analysis = await self.run_agent("analyst", analysis_prompt, f"{plan}\n\n{research}")
        results["steps"]["analysis"] = analysis
        print("✅ Analysis completed")
        
        # Step 4: Report Writing
        print("📝 Writing final report...")
        report_prompt = f"Write a comprehensive report for '{topic}'"
        context = f"Plan:\n{plan}\n\nResearch:\n{research}\n\nAnalysis:\n{analysis}"
        report = await self.run_agent("writer", report_prompt, context)
        results["steps"]["final_report"] = report
        print("✅ Report completed")
        
        return results

async def pipeline_example():
    """Example usage of the research pipeline"""
    pipeline = ResearchPipeline()
    
    topics = [
        "The future of remote work post-pandemic",
        "Ethical implications of AI in hiring"
    ]
    
    for topic in topics:
        print(f"\n{'='*60}")
        print(f"RESEARCHING: {topic}")
        print(f"{'='*60}")
        
        results = await pipeline.execute_pipeline(topic)
        
        # Save results
        filename = f"research_{topic.replace(' ', '_').lower()}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📄 Final Report for '{topic}':")
        print("-" * 40)
        print(results["steps"]["final_report"])
        print(f"\n💾 Full results saved to: {filename}")

if __name__ == "__main__":
    asyncio.run(pipeline_example())
```

---

## Module 3: CrewAI Examples

### Custom Debate Crew

Create a debate crew with custom agents:

```python
# 3_crew/example_custom_debate.py
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

class CustomDebateCrew:
    """Custom debate crew with specialized agents"""
    
    def __init__(self):
        self.search_tool = SerperDevTool()
    
    def create_agents(self):
        """Create specialized debate agents"""
        
        # Pro-argument agent
        pro_agent = Agent(
            role='Pro Debater',
            goal='Present compelling arguments in favor of the motion',
            backstory="""You are an experienced debater who specializes in building 
            strong cases for propositions. You excel at finding evidence, logical reasoning, 
            and persuasive argumentation. You always look for the strongest possible case.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool]
        )
        
        # Con-argument agent
        con_agent = Agent(
            role='Con Debater',
            goal='Present compelling arguments against the motion',
            backstory="""You are a skilled debater who specializes in finding flaws 
            in arguments and presenting strong counter-cases. You excel at critical thinking, 
            identifying weaknesses, and building opposition arguments.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool]
        )
        
        # Moderator agent
        moderator = Agent(
            role='Debate Moderator',
            goal='Facilitate fair debate and provide balanced summary',
            backstory="""You are an experienced debate moderator who ensures fair 
            discussion and provides objective analysis. You summarize key points from 
            both sides and help identify the strongest arguments.""",
            verbose=True,
            allow_delegation=False
        )
        
        return pro_agent, con_agent, moderator
    
    def create_tasks(self, motion: str, pro_agent, con_agent, moderator):
        """Create debate tasks"""
        
        # Research and argument tasks
        pro_research = Task(
            description=f"""Research and prepare strong arguments IN FAVOR of: '{motion}'
            
            Your tasks:
            1. Find credible evidence supporting the motion
            2. Develop 3-4 key arguments with supporting evidence
            3. Anticipate potential counter-arguments
            4. Structure your case logically
            
            Focus on facts, statistics, expert opinions, and logical reasoning.""",
            agent=pro_agent,
            expected_output="A well-structured pro argument with evidence and reasoning"
        )
        
        con_research = Task(
            description=f"""Research and prepare strong arguments AGAINST: '{motion}'
            
            Your tasks:
            1. Find credible evidence opposing the motion
            2. Develop 3-4 key counter-arguments with supporting evidence
            3. Identify weaknesses in pro arguments
            4. Structure your opposition case logically
            
            Focus on facts, statistics, expert opinions, and logical reasoning.""",
            agent=con_agent,
            expected_output="A well-structured con argument with evidence and reasoning"
        )
        
        # Debate round
        debate_round = Task(
            description=f"""Conduct a structured debate on: '{motion}'
            
            Using the research from both sides, present:
            1. Opening statements (Pro then Con)
            2. Main arguments with evidence
            3. Rebuttals to opposing points
            4. Closing statements
            
            Maintain professional, respectful discourse throughout.""",
            agent=moderator,
            expected_output="A complete debate transcript with arguments from both sides",
            context=[pro_research, con_research]
        )
        
        # Final summary
        summary_task = Task(
            description=f"""Provide an objective summary and analysis of the debate on: '{motion}'
            
            Include:
            1. Summary of key arguments from both sides
            2. Strength assessment of each position
            3. Most compelling evidence presented
            4. Areas where more research might be needed
            5. Balanced conclusion
            
            Remain neutral and objective in your analysis.""",
            agent=moderator,
            expected_output="An objective debate summary and analysis",
            context=[debate_round]
        )
        
        return [pro_research, con_research, debate_round, summary_task]
    
    def run_debate(self, motion: str):
        """Run a complete debate on the given motion"""
        
        # Create agents and tasks
        pro_agent, con_agent, moderator = self.create_agents()
        tasks = self.create_tasks(motion, pro_agent, con_agent, moderator)
        
        # Create and run crew
        crew = Crew(
            agents=[pro_agent, con_agent, moderator],
            tasks=tasks,
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff()
        return result

def debate_example():
    """Example usage of custom debate crew"""
    
    debate_crew = CustomDebateCrew()
    
    # Example motions
    motions = [
        "Artificial Intelligence should be regulated by government",
        "Remote work is more productive than office work",
        "Social media has a net positive impact on society"
    ]
    
    for motion in motions:
        print(f"\n{'='*60}")
        print(f"DEBATE MOTION: {motion}")
        print(f"{'='*60}")
        
        try:
            result = debate_crew.run_debate(motion)
            print("\n📄 DEBATE RESULT:")
            print("-" * 40)
            print(result.raw)
            
            # Save result
            filename = f"debate_{motion.replace(' ', '_').lower()}.txt"
            with open(filename, 'w') as f:
                f.write(f"Debate Motion: {motion}\n")
                f.write("="*60 + "\n\n")
                f.write(result.raw)
            
            print(f"\n💾 Debate saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error in debate: {e}")

if __name__ == "__main__":
    debate_example()
```

### Financial Analysis Crew

Create a comprehensive financial analysis system:

```python
# 3_crew/example_financial_analysis.py
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
import os

load_dotenv()

class FinancialAnalysisCrew:
    """Comprehensive financial analysis crew"""
    
    def __init__(self):
        self.search_tool = SerperDevTool()
        self.web_tool = WebsiteSearchTool()
    
    def create_agents(self):
        """Create financial analysis agents"""
        
        # Financial data researcher
        researcher = Agent(
            role='Financial Data Researcher',
            goal='Gather comprehensive financial data and market information',
            backstory="""You are a financial research specialist with expertise in 
            gathering and analyzing market data, financial statements, and industry trends. 
            You know where to find the most reliable and up-to-date financial information.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool, self.web_tool]
        )
        
        # Technical analyst
        technical_analyst = Agent(
            role='Technical Analyst',
            goal='Analyze price patterns, trends, and technical indicators',
            backstory="""You are a technical analysis expert who specializes in 
            chart patterns, technical indicators, and market trends. You can identify 
            support/resistance levels, trend directions, and potential entry/exit points.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool]
        )
        
        # Fundamental analyst
        fundamental_analyst = Agent(
            role='Fundamental Analyst',
            goal='Analyze company fundamentals and intrinsic value',
            backstory="""You are a fundamental analysis expert who evaluates companies 
            based on financial statements, business models, competitive advantages, 
            and industry position. You excel at determining intrinsic value.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool, self.web_tool]
        )
        
        # Risk analyst
        risk_analyst = Agent(
            role='Risk Analyst',
            goal='Assess investment risks and potential downsides',
            backstory="""You are a risk management specialist who identifies and 
            quantifies various types of investment risks including market risk, 
            credit risk, operational risk, and regulatory risk.""",
            verbose=True,
            allow_delegation=False,
            tools=[self.search_tool]
        )
        
        # Investment advisor
        advisor = Agent(
            role='Investment Advisor',
            goal='Synthesize analysis and provide investment recommendations',
            backstory="""You are a senior investment advisor who synthesizes technical, 
            fundamental, and risk analysis to provide comprehensive investment recommendations. 
            You consider multiple perspectives and provide balanced advice.""",
            verbose=True,
            allow_delegation=False
        )
        
        return researcher, technical_analyst, fundamental_analyst, risk_analyst, advisor
    
    def create_tasks(self, company: str, agents):
        """Create financial analysis tasks"""
        researcher, technical_analyst, fundamental_analyst, risk_analyst, advisor = agents
        
        # Data gathering task
        research_task = Task(
            description=f"""Gather comprehensive financial data for {company}:
            
            Research areas:
            1. Current stock price and recent performance
            2. Latest financial statements (income, balance sheet, cash flow)
            3. Key financial ratios and metrics
            4. Recent news and developments
            5. Industry position and competitors
            6. Management team and corporate governance
            
            Provide accurate, up-to-date information with sources.""",
            agent=researcher,
            expected_output="Comprehensive financial data report with sources"
        )
        
        # Technical analysis task
        technical_task = Task(
            description=f"""Perform technical analysis for {company}:
            
            Analysis areas:
            1. Current price trends and patterns
            2. Support and resistance levels
            3. Moving averages and momentum indicators
            4. Volume analysis
            5. Chart patterns and signals
            6. Short-term and long-term outlook
            
            Provide specific technical insights and potential price targets.""",
            agent=technical_analyst,
            expected_output="Detailed technical analysis with price targets and signals",
            context=[research_task]
        )
        
        # Fundamental analysis task
        fundamental_task = Task(
            description=f"""Perform fundamental analysis for {company}:
            
            Analysis areas:
            1. Financial statement analysis
            2. Profitability and efficiency ratios
            3. Growth prospects and business model
            4. Competitive advantages and market position
            5. Management quality and strategy
            6. Intrinsic value estimation
            
            Provide detailed fundamental assessment and fair value estimate.""",
            agent=fundamental_analyst,
            expected_output="Comprehensive fundamental analysis with value estimation",
            context=[research_task]
        )
        
        # Risk analysis task
        risk_task = Task(
            description=f"""Assess investment risks for {company}:
            
            Risk categories:
            1. Business and operational risks
            2. Financial and credit risks
            3. Market and systematic risks
            4. Regulatory and compliance risks
            5. ESG (Environmental, Social, Governance) risks
            6. Scenario analysis and stress testing
            
            Quantify risks where possible and suggest mitigation strategies.""",
            agent=risk_analyst,
            expected_output="Comprehensive risk assessment with mitigation strategies",
            context=[research_task, fundamental_task]
        )
        
        # Investment recommendation task
        recommendation_task = Task(
            description=f"""Provide investment recommendation for {company}:
            
            Synthesize all analysis to provide:
            1. Clear investment thesis (buy/hold/sell)
            2. Target price and time horizon
            3. Key catalysts and risks
            4. Position sizing recommendations
            5. Entry and exit strategies
            6. Monitoring plan and key metrics to watch
            
            Provide balanced, well-reasoned recommendations.""",
            agent=advisor,
            expected_output="Comprehensive investment recommendation with rationale",
            context=[research_task, technical_task, fundamental_task, risk_task]
        )
        
        return [research_task, technical_task, fundamental_task, risk_task, recommendation_task]
    
    def analyze_company(self, company: str):
        """Perform complete financial analysis"""
        
        agents = self.create_agents()
        tasks = self.create_tasks(company, agents)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=2
        )
        
        result = crew.kickoff()
        return result

def financial_analysis_example():
    """Example usage of financial analysis crew"""
    
    analysis_crew = FinancialAnalysisCrew()
    
    # Example companies to analyze
    companies = ["Apple Inc. (AAPL)", "Tesla Inc. (TSLA)", "Microsoft Corporation (MSFT)"]
    
    for company in companies:
        print(f"\n{'='*60}")
        print(f"ANALYZING: {company}")
        print(f"{'='*60}")
        
        try:
            result = analysis_crew.analyze_company(company)
            
            print("\n📊 ANALYSIS RESULT:")
            print("-" * 40)
            print(result.raw)
            
            # Save result
            filename = f"analysis_{company.split('(')[1].replace(')', '').lower()}.txt"
            with open(filename, 'w') as f:
                f.write(f"Financial Analysis: {company}\n")
                f.write("="*60 + "\n\n")
                f.write(result.raw)
            
            print(f"\n💾 Analysis saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Error in analysis: {e}")

if __name__ == "__main__":
    financial_analysis_example()
```

---

## Module 4: LangGraph Examples

### Advanced Workflow Agent

Create a sophisticated workflow agent with multiple capabilities:

```python
# 4_langgraph/example_advanced_workflow.py
import asyncio
import json
from typing import Dict, List, Any
from sidekick import Sidekick

class AdvancedWorkflowAgent:
    """Advanced workflow agent with complex task handling"""
    
    def __init__(self):
        self.sidekick = None
        self.task_history = []
    
    async def initialize(self):
        """Initialize the workflow agent"""
        self.sidekick = Sidekick()
        await self.sidekick.setup()
        print("✅ Advanced Workflow Agent initialized")
    
    async def execute_task(self, task_description: str, success_criteria: str = None) -> Dict:
        """Execute a single task with detailed tracking"""
        
        if not success_criteria:
            success_criteria = f"Task '{task_description}' should be completed successfully with clear results"
        
        print(f"\n🎯 Executing Task: {task_description}")
        print(f"📋 Success Criteria: {success_criteria}")
        print("-" * 50)
        
        try:
            history = await self.sidekick.run_superstep(
                message=task_description,
                success_criteria=success_criteria,
                history=[]
            )
            
            # Extract results
            task_result = {
                "task": task_description,
                "success_criteria": success_criteria,
                "status": "completed",
                "result": history[-2]['content'] if len(history) >= 2 else "No result",
                "feedback": history[-1]['content'] if len(history) >= 1 else "No feedback",
                "timestamp": self._get_timestamp()
            }
            
            self.task_history.append(task_result)
            print("✅ Task completed successfully")
            return task_result
            
        except Exception as e:
            error_result = {
                "task": task_description,
                "success_criteria": success_criteria,
                "status": "failed",
                "error": str(e),
                "timestamp": self._get_timestamp()
            }
            
            self.task_history.append(error_result)
            print(f"❌ Task failed: {e}")
            return error_result
    
    async def execute_workflow(self, workflow: List[Dict]) -> List[Dict]:
        """Execute a complete workflow with multiple tasks"""
        
        print(f"\n🚀 Starting Workflow with {len(workflow)} tasks")
        print("=" * 60)
        
        results = []
        
        for i, task_config in enumerate(workflow, 1):
            print(f"\n📝 Task {i}/{len(workflow)}")
            
            task_description = task_config.get("task", "")
            success_criteria = task_config.get("success_criteria", None)
            depends_on = task_config.get("depends_on", [])
            
            # Check dependencies
            if depends_on:
                dependency_results = self._check_dependencies(depends_on, results)
                if not dependency_results["all_successful"]:
                    print(f"⚠️  Skipping task due to failed dependencies: {dependency_results['failed']}")
                    continue
                
                # Add dependency context to task
                context = self._build_dependency_context(depends_on, results)
                task_description = f"{task_description}\n\nContext from previous tasks:\n{context}"
            
            result = await self.execute_task(task_description, success_criteria)
            results.append(result)
            
            # Stop workflow if critical task fails
            if result["status"] == "failed" and task_config.get("critical", False):
                print("🛑 Critical task failed. Stopping workflow.")
                break
        
        return results
    
    def _check_dependencies(self, depends_on: List[int], results: List[Dict]) -> Dict:
        """Check if dependency tasks completed successfully"""
        failed_deps = []
        
        for dep_index in depends_on:
            if dep_index >= len(results):
                failed_deps.append(f"Task {dep_index + 1} (not executed)")
            elif results[dep_index]["status"] != "completed":
                failed_deps.append(f"Task {dep_index + 1} (failed)")
        
        return {
            "all_successful": len(failed_deps) == 0,
            "failed": failed_deps
        }
    
    def _build_dependency_context(self, depends_on: List[int], results: List[Dict]) -> str:
        """Build context from dependency task results"""
        context = ""
        for dep_index in depends_on:
            if dep_index < len(results) and results[dep_index]["status"] == "completed":
                task_result = results[dep_index]
                context += f"Task {dep_index + 1} ({task_result['task']}):\n"
                context += f"Result: {task_result['result']}\n\n"
        return context
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_report(self) -> str:
        """Generate a comprehensive workflow report"""
        if not self.task_history:
            return "No tasks executed yet."
        
        completed = len([t for t in self.task_history if t["status"] == "completed"])
        failed = len([t for t in self.task_history if t["status"] == "failed"])
        
        report = f"""
# Workflow Execution Report

## Summary
- Total Tasks: {len(self.task_history)}
- Completed: {completed}
- Failed: {failed}
- Success Rate: {(completed / len(self.task_history) * 100):.1f}%

## Task Details
"""
        
        for i, task in enumerate(self.task_history, 1):
            status_emoji = "✅" if task["status"] == "completed" else "❌"
            report += f"""
### Task {i}: {task['task']} {status_emoji}
- **Status**: {task['status']}
- **Timestamp**: {task['timestamp']}
- **Success Criteria**: {task['success_criteria']}
"""
            
            if task["status"] == "completed":
                report += f"- **Result**: {task['result'][:200]}...\n"
                report += f"- **Feedback**: {task['feedback'][:200]}...\n"
            else:
                report += f"- **Error**: {task.get('error', 'Unknown error')}\n"
        
        return report
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.sidekick:
            self.sidekick.cleanup()

# Example workflow definitions
RESEARCH_WORKFLOW = [
    {
        "task": "Research the latest trends in artificial intelligence for 2024",
        "success_criteria": "Provide a comprehensive overview of AI trends with specific examples and sources",
        "critical": True
    },
    {
        "task": "Create a summary document of the AI trends research",
        "success_criteria": "Save a well-formatted markdown document with the research summary",
        "depends_on": [0]
    },
    {
        "task": "Find and analyze 3 specific AI companies that are leading these trends",
        "success_criteria": "Provide detailed analysis of 3 companies with their contributions to AI trends",
        "depends_on": [0]
    },
    {
        "task": "Create a presentation outline based on the research",
        "success_criteria": "Generate a structured presentation outline covering all key points",
        "depends_on": [0, 1, 2]
    }
]

DEVELOPMENT_WORKFLOW = [
    {
        "task": "Create a Python script that analyzes CSV data and generates visualizations",
        "success_criteria": "Script should be saved, functional, and include sample data processing",
        "critical": True
    },
    {
        "task": "Write comprehensive documentation for the data analysis script",
        "success_criteria": "Create a README file with usage instructions and examples",
        "depends_on": [0]
    },
    {
        "task": "Create unit tests for the data analysis functions",
        "success_criteria": "Write test cases that cover main functionality and edge cases",
        "depends_on": [0]
    },
    {
        "task": "Package the script with its documentation and tests",
        "success_criteria": "Organize files in a proper project structure with requirements.txt",
        "depends_on": [0, 1, 2]
    }
]

async def workflow_examples():
    """Run example workflows"""
    
    agent = AdvancedWorkflowAgent()
    await agent.initialize()
    
    try:
        # Example 1: Research Workflow
        print("\n" + "="*60)
        print("RESEARCH WORKFLOW EXAMPLE")
        print("="*60)
        
        research_results = await agent.execute_workflow(RESEARCH_WORKFLOW)
        
        print("\n📊 Research Workflow Results:")
        for i, result in enumerate(research_results, 1):
            status = "✅" if result["status"] == "completed" else "❌"
            print(f"Task {i}: {result['task'][:50]}... {status}")
        
        # Example 2: Development Workflow
        print("\n" + "="*60)
        print("DEVELOPMENT WORKFLOW EXAMPLE")
        print("="*60)
        
        dev_results = await agent.execute_workflow(DEVELOPMENT_WORKFLOW)
        
        print("\n📊 Development Workflow Results:")
        for i, result in enumerate(dev_results, 1):
            status = "✅" if result["status"] == "completed" else "❌"
            print(f"Task {i}: {result['task'][:50]}... {status}")
        
        # Generate and save report
        report = agent.generate_report()
        with open("workflow_report.md", "w") as f:
            f.write(report)
        
        print(f"\n📄 Workflow report saved to: workflow_report.md")
        print("\n" + report[:500] + "...")
        
    finally:
        await agent.cleanup()

if __name__ == "__main__":
    asyncio.run(workflow_examples())
```

### Interactive Task Manager

Create an interactive task management system:

```python
# 4_langgraph/example_interactive_manager.py
import asyncio
import json
from typing import Dict, List
from sidekick import Sidekick

class InteractiveTaskManager:
    """Interactive task manager with real-time control"""
    
    def __init__(self):
        self.sidekick = None
        self.active_tasks = {}
        self.completed_tasks = []
        self.task_counter = 0
    
    async def initialize(self):
        """Initialize the task manager"""
        self.sidekick = Sidekick()
        await self.sidekick.setup()
        print("🎯 Interactive Task Manager ready!")
    
    async def add_task(self, description: str, priority: str = "medium", 
                      success_criteria: str = None) -> str:
        """Add a new task to the queue"""
        
        self.task_counter += 1
        task_id = f"task_{self.task_counter}"
        
        if not success_criteria:
            success_criteria = f"Complete the task: {description}"
        
        task = {
            "id": task_id,
            "description": description,
            "priority": priority,
            "success_criteria": success_criteria,
            "status": "pending",
            "created_at": self._get_timestamp()
        }
        
        self.active_tasks[task_id] = task
        print(f"➕ Added task {task_id}: {description[:50]}...")
        return task_id
    
    async def execute_task(self, task_id: str) -> Dict:
        """Execute a specific task"""
        
        if task_id not in self.active_tasks:
            return {"error": f"Task {task_id} not found"}
        
        task = self.active_tasks[task_id]
        task["status"] = "running"
        task["started_at"] = self._get_timestamp()
        
        print(f"\n🚀 Executing {task_id}: {task['description']}")
        print(f"Priority: {task['priority']}")
        print("-" * 50)
        
        try:
            history = await self.sidekick.run_superstep(
                message=task["description"],
                success_criteria=task["success_criteria"],
                history=[]
            )
            
            # Update task with results
            task["status"] = "completed"
            task["completed_at"] = self._get_timestamp()
            task["result"] = history[-2]['content'] if len(history) >= 2 else "No result"
            task["feedback"] = history[-1]['content'] if len(history) >= 1 else "No feedback"
            
            # Move to completed tasks
            self.completed_tasks.append(task)
            del self.active_tasks[task_id]
            
            print(f"✅ Task {task_id} completed successfully")
            return task
            
        except Exception as e:
            task["status"] = "failed"
            task["error"] = str(e)
            task["failed_at"] = self._get_timestamp()
            
            print(f"❌ Task {task_id} failed: {e}")
            return task
    
    async def execute_all_tasks(self, priority_order: List[str] = None) -> List[Dict]:
        """Execute all pending tasks"""
        
        if not priority_order:
            priority_order = ["high", "medium", "low"]
        
        results = []
        
        # Sort tasks by priority
        sorted_tasks = self._sort_tasks_by_priority(priority_order)
        
        print(f"\n📋 Executing {len(sorted_tasks)} tasks in priority order")
        
        for task_id in sorted_tasks:
            result = await self.execute_task(task_id)
            results.append(result)
        
        return results
    
    def _sort_tasks_by_priority(self, priority_order: List[str]) -> List[str]:
        """Sort tasks by priority"""
        
        priority_map = {priority: i for i, priority in enumerate(priority_order)}
        
        return sorted(
            self.active_tasks.keys(),
            key=lambda task_id: priority_map.get(self.active_tasks[task_id]["priority"], 999)
        )
    
    def get_status(self) -> Dict:
        """Get current status of all tasks"""
        
        return {
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "total_tasks": self.task_counter,
            "tasks_by_priority": self._count_by_priority(),
            "tasks_by_status": self._count_by_status()
        }
    
    def _count_by_priority(self) -> Dict:
        """Count tasks by priority"""
        counts = {"high": 0, "medium": 0, "low": 0}
        
        for task in self.active_tasks.values():
            priority = task.get("priority", "medium")
            if priority in counts:
                counts[priority] += 1
        
        return counts
    
    def _count_by_status(self) -> Dict:
        """Count tasks by status"""
        counts = {"pending": 0, "running": 0, "completed": 0, "failed": 0}
        
        for task in self.active_tasks.values():
            status = task.get("status", "pending")
            if status in counts:
                counts[status] += 1
        
        counts["completed"] = len([t for t in self.completed_tasks if t["status"] == "completed"])
        counts["failed"] = len([t for t in self.completed_tasks if t["status"] == "failed"])
        
        return counts
    
    def list_tasks(self, status: str = "all") -> List[Dict]:
        """List tasks by status"""
        
        if status == "all":
            return list(self.active_tasks.values()) + self.completed_tasks
        elif status == "active":
            return list(self.active_tasks.values())
        elif status == "completed":
            return [t for t in self.completed_tasks if t["status"] == "completed"]
        elif status == "failed":
            return [t for t in self.completed_tasks if t["status"] == "failed"]
        else:
            return [t for t in self.active_tasks.values() if t["status"] == status]
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.sidekick:
            self.sidekick.cleanup()

async def interactive_manager_example():
    """Example of interactive task management"""
    
    manager = InteractiveTaskManager()
    await manager.initialize()
    
    try:
        # Add various tasks with different priorities
        tasks_to_add = [
            {
                "description": "Research the top 5 programming languages in 2024",
                "priority": "high",
                "success_criteria": "Provide detailed analysis with usage statistics and trends"
            },
            {
                "description": "Create a Python script for data visualization",
                "priority": "medium",
                "success_criteria": "Save a working script with sample data and charts"
            },
            {
                "description": "Write a blog post about AI trends",
                "priority": "low",
                "success_criteria": "Create a well-structured blog post of 800+ words"
            },
            {
                "description": "Analyze the latest stock market trends",
                "priority": "high",
                "success_criteria": "Provide current market analysis with key insights"
            },
            {
                "description": "Create a simple web scraping script",
                "priority": "medium",
                "success_criteria": "Build a functional web scraper with error handling"
            }
        ]
        
        # Add all tasks
        print("📝 Adding tasks to queue...")
        task_ids = []
        for task_config in tasks_to_add:
            task_id = await manager.add_task(**task_config)
            task_ids.append(task_id)
        
        # Show initial status
        status = manager.get_status()
        print(f"\n📊 Initial Status:")
        print(f"Active tasks: {status['active_tasks']}")
        print(f"Tasks by priority: {status['tasks_by_priority']}")
        
        # Execute all tasks
        print(f"\n🚀 Executing all tasks...")
        results = await manager.execute_all_tasks()
        
        # Show final status
        final_status = manager.get_status()
        print(f"\n📊 Final Status:")
        print(f"Completed: {final_status['tasks_by_status']['completed']}")
        print(f"Failed: {final_status['tasks_by_status']['failed']}")
        
        # Show completed tasks
        completed_tasks = manager.list_tasks("completed")
        print(f"\n✅ Completed Tasks ({len(completed_tasks)}):")
        for task in completed_tasks:
            print(f"- {task['id']}: {task['description'][:50]}...")
        
        # Show failed tasks if any
        failed_tasks = manager.list_tasks("failed")
        if failed_tasks:
            print(f"\n❌ Failed Tasks ({len(failed_tasks)}):")
            for task in failed_tasks:
                print(f"- {task['id']}: {task['description'][:50]}...")
        
        # Save detailed report
        report_data = {
            "summary": final_status,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks
        }
        
        with open("task_manager_report.json", "w") as f:
            json.dump(report_data, f, indent=2, default=str)
        
        print(f"\n💾 Detailed report saved to: task_manager_report.json")
        
    finally:
        await manager.cleanup()

if __name__ == "__main__":
    asyncio.run(interactive_manager_example())
```

---

## Module 5: AutoGen Examples

### Dynamic Agent Factory

Create a system that generates specialized agents on demand:

```python
# 5_autogen/example_agent_factory.py
import asyncio
import json
from typing import Dict, List
from creator import Creator
from messages import Message
from autogen_core import AgentRuntime, MessageContext

class AgentFactory:
    """Factory for creating specialized agents dynamically"""
    
    def __init__(self):
        self.runtime = None
        self.creator = None
        self.created_agents = {}
        self.agent_templates = self._load_agent_templates()
    
    def _load_agent_templates(self) -> Dict:
        """Load predefined agent templates"""
        return {
            "data_analyst": {
                "description": "Expert in data analysis, statistics, and visualization",
                "specialties": ["pandas", "numpy", "matplotlib", "statistical analysis"],
                "system_message": """You are a data analysis expert. You excel at:
                - Processing and analyzing datasets
                - Creating visualizations and charts
                - Statistical analysis and interpretation
                - Data cleaning and preprocessing
                - Identifying patterns and insights"""
            },
            "web_developer": {
                "description": "Full-stack web developer with modern frameworks",
                "specialties": ["HTML", "CSS", "JavaScript", "React", "Node.js", "databases"],
                "system_message": """You are a web development expert. You excel at:
                - Frontend development with modern frameworks
                - Backend API development
                - Database design and optimization
                - User interface and experience design
                - Web security and performance optimization"""
            },
            "content_writer": {
                "description": "Professional content writer and copywriter",
                "specialties": ["blog posts", "marketing copy", "technical writing", "SEO"],
                "system_message": """You are a professional content writer. You excel at:
                - Creating engaging blog posts and articles
                - Writing compelling marketing copy
                - Technical documentation and guides
                - SEO-optimized content
                - Adapting tone and style for different audiences"""
            },
            "financial_advisor": {
                "description": "Financial planning and investment expert",
                "specialties": ["investment analysis", "portfolio management", "risk assessment", "financial planning"],
                "system_message": """You are a financial advisor expert. You excel at:
                - Investment analysis and recommendations
                - Portfolio optimization and diversification
                - Risk assessment and management
                - Financial planning and budgeting
                - Market analysis and economic trends"""
            }
        }
    
    async def initialize(self):
        """Initialize the agent factory"""
        self.runtime = AgentRuntime()
        self.creator = Creator("agent_creator")
        await self.creator.register(self.runtime, "agent_creator", lambda: self.creator)
        print("🏭 Agent Factory initialized")
    
    async def create_agent(self, agent_type: str, name: str = None, 
                          custom_specs: Dict = None) -> str:
        """Create a new agent of specified type"""
        
        if not name:
            name = f"{agent_type}_{len(self.created_agents) + 1}"
        
        # Get template or use custom specifications
        if agent_type in self.agent_templates:
            template = self.agent_templates[agent_type]
        elif custom_specs:
            template = custom_specs
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        print(f"🔨 Creating {agent_type} agent: {name}")
        
        # Create agent specification
        agent_spec = self._generate_agent_code(name, template)
        
        # Save agent code to file
        filename = f"{name}.py"
        with open(filename, 'w') as f:
            f.write(agent_spec)
        
        # Use creator to generate and register the agent
        try:
            result = await self.creator.handle_my_message_type(
                Message(content=filename),
                MessageContext()
            )
            
            self.created_agents[name] = {
                "type": agent_type,
                "filename": filename,
                "template": template,
                "created_at": self._get_timestamp(),
                "status": "active"
            }
            
            print(f"✅ Agent {name} created successfully")
            return name
            
        except Exception as e:
            print(f"❌ Failed to create agent {name}: {e}")
            raise
    
    def _generate_agent_code(self, name: str, template: Dict) -> str:
        """Generate Python code for the agent"""
        
        system_message = template.get("system_message", "You are a helpful AI assistant.")
        
        code = f'''
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):
    
    system_message = """{system_message}"""
    
    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)
    
    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        return messages.Message(content=response.chat_message.content)
'''
        
        return code
    
    async def send_message_to_agent(self, agent_name: str, message: str) -> str:
        """Send a message to a created agent"""
        
        if agent_name not in self.created_agents:
            return f"Agent {agent_name} not found"
        
        try:
            from autogen_core import AgentId
            result = await self.runtime.send_message(
                Message(content=message),
                AgentId(agent_name, "default")
            )
            return result.content
            
        except Exception as e:
            return f"Error communicating with {agent_name}: {e}"
    
    async def create_agent_team(self, team_config: List[Dict]) -> List[str]:
        """Create a team of agents for collaborative work"""
        
        team_agents = []
        
        for agent_config in team_config:
            agent_type = agent_config["type"]
            agent_name = agent_config.get("name")
            custom_specs = agent_config.get("custom_specs")
            
            try:
                agent_name = await self.create_agent(agent_type, agent_name, custom_specs)
                team_agents.append(agent_name)
                
            except Exception as e:
                print(f"Failed to create team member {agent_name}: {e}")
        
        print(f"👥 Team created with {len(team_agents)} agents: {', '.join(team_agents)}")
        return team_agents
    
    async def run_collaborative_task(self, team_agents: List[str], task: str) -> Dict:
        """Run a collaborative task across multiple agents"""
        
        results = {}
        
        print(f"🤝 Running collaborative task with {len(team_agents)} agents")
        print(f"Task: {task}")
        
        for agent_name in team_agents:
            print(f"\n📤 Sending task to {agent_name}...")
            
            # Customize task for each agent type
            agent_info = self.created_agents[agent_name]
            agent_type = agent_info["type"]
            
            specialized_task = self._customize_task_for_agent(task, agent_type)
            
            result = await self.send_message_to_agent(agent_name, specialized_task)
            results[agent_name] = {
                "agent_type": agent_type,
                "task": specialized_task,
                "result": result,
                "timestamp": self._get_timestamp()
            }
            
            print(f"✅ Response received from {agent_name}")
        
        return results
    
    def _customize_task_for_agent(self, base_task: str, agent_type: str) -> str:
        """Customize task based on agent specialization"""
        
        customizations = {
            "data_analyst": f"From a data analysis perspective: {base_task}. Focus on data-driven insights and statistical analysis.",
            "web_developer": f"From a web development perspective: {base_task}. Consider technical implementation and user experience.",
            "content_writer": f"From a content creation perspective: {base_task}. Focus on clear communication and audience engagement.",
            "financial_advisor": f"From a financial advisory perspective: {base_task}. Consider financial implications and risk factors."
        }
        
        return customizations.get(agent_type, base_task)
    
    def get_agent_status(self) -> Dict:
        """Get status of all created agents"""
        
        return {
            "total_agents": len(self.created_agents),
            "agents_by_type": self._count_by_type(),
            "agent_details": self.created_agents
        }
    
    def _count_by_type(self) -> Dict:
        """Count agents by type"""
        counts = {}
        for agent_info in self.created_agents.values():
            agent_type = agent_info["type"]
            counts[agent_type] = counts.get(agent_type, 0) + 1
        return counts
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.runtime:
            await self.runtime.stop()

async def agent_factory_example():
    """Example usage of the agent factory"""
    
    factory = AgentFactory()
    await factory.initialize()
    
    try:
        # Example 1: Create individual agents
        print("=" * 60)
        print("CREATING INDIVIDUAL AGENTS")
        print("=" * 60)
        
        # Create different types of agents
        data_agent = await factory.create_agent("data_analyst", "market_analyst")
        web_agent = await factory.create_agent("web_developer", "frontend_dev")
        writer_agent = await factory.create_agent("content_writer", "blog_writer")
        
        # Test individual agents
        print(f"\n💬 Testing individual agents:")
        
        tasks = [
            ("market_analyst", "Analyze the current cryptocurrency market trends"),
            ("frontend_dev", "What are the best practices for responsive web design?"),
            ("blog_writer", "Write an engaging introduction for a blog post about AI")
        ]
        
        for agent_name, task in tasks:
            print(f"\n📤 {agent_name}: {task}")
            response = await factory.send_message_to_agent(agent_name, task)
            print(f"📥 Response: {response[:200]}...")
        
        # Example 2: Create and run a collaborative team
        print("\n" + "=" * 60)
        print("CREATING COLLABORATIVE TEAM")
        print("=" * 60)
        
        team_config = [
            {"type": "data_analyst", "name": "research_analyst"},
            {"type": "content_writer", "name": "report_writer"},
            {"type": "financial_advisor", "name": "investment_advisor"}
        ]
        
        team = await factory.create_agent_team(team_config)
        
        # Run collaborative task
        collaborative_task = "Analyze the potential of investing in renewable energy stocks"
        
        results = await factory.run_collaborative_task(team, collaborative_task)
        
        print(f"\n📊 Collaborative Results:")
        for agent_name, result in results.items():
            print(f"\n{agent_name} ({result['agent_type']}):")
            print(f"Result: {result['result'][:150]}...")
        
        # Show factory status
        status = factory.get_agent_status()
        print(f"\n📈 Factory Status:")
        print(f"Total agents created: {status['total_agents']}")
        print(f"Agents by type: {status['agents_by_type']}")
        
        # Save results
        with open("agent_factory_results.json", "w") as f:
            json.dump({
                "factory_status": status,
                "collaborative_results": results
            }, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: agent_factory_results.json")
        
    finally:
        await factory.cleanup()

if __name__ == "__main__":
    asyncio.run(agent_factory_example())
```

---

## Module 6: MCP Examples

### Advanced Trading Bot

Create a sophisticated trading bot with multiple strategies:

```python
# 6_mcp/example_advanced_trading_bot.py
import asyncio
import json
from typing import Dict, List
from accounts import Account
from traders import Trader, get_model
from database import write_log, read_log

class AdvancedTradingBot:
    """Advanced trading bot with multiple strategies and risk management"""
    
    def __init__(self, name: str, initial_balance: float = 10000):
        self.name = name
        self.account = Account.get(name)
        self.strategies = {}
        self.performance_metrics = {}
        self.risk_limits = {
            "max_position_size": 0.1,  # 10% of portfolio per position
            "max_daily_loss": 0.05,    # 5% max daily loss
            "max_drawdown": 0.15       # 15% max drawdown
        }
        
        # Initialize account if needed
        if self.account.balance == 0:
            self.account.deposit(initial_balance)
    
    def add_strategy(self, strategy_name: str, strategy_config: Dict):
        """Add a trading strategy"""
        self.strategies[strategy_name] = {
            "config": strategy_config,
            "active": True,
            "performance": {"trades": 0, "wins": 0, "losses": 0, "pnl": 0}
        }
        write_log(self.name, "strategy", f"Added strategy: {strategy_name}")
    
    async def analyze_market_sentiment(self) -> Dict:
        """Analyze overall market sentiment"""
        # This would typically connect to news APIs, social media sentiment, etc.
        # For demo purposes, we'll simulate market analysis
        
        sentiment_data = {
            "overall_sentiment": "neutral",
            "fear_greed_index": 45,  # 0-100 scale
            "market_volatility": "medium",
            "news_sentiment": "slightly_positive",
            "technical_outlook": "consolidating"
        }
        
        write_log(self.name, "analysis", f"Market sentiment: {sentiment_data['overall_sentiment']}")
        return sentiment_data
    
    async def screen_stocks(self, criteria: Dict) -> List[str]:
        """Screen stocks based on criteria"""
        # In a real implementation, this would connect to financial data APIs
        # For demo, we'll return some sample stocks
        
        sample_stocks = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA", "AMZN", "META", "NFLX"]
        
        # Simulate filtering based on criteria
        filtered_stocks = sample_stocks[:criteria.get("max_results", 5)]
        
        write_log(self.name, "screening", f"Screened {len(filtered_stocks)} stocks")
        return filtered_stocks
    
    async def calculate_position_size(self, symbol: str, risk_per_trade: float = 0.02) -> int:
        """Calculate appropriate position size based on risk management"""
        
        portfolio_value = self.account.calculate_portfolio_value()
        risk_amount = portfolio_value * risk_per_trade
        
        # For demo, assume $150 per share average price
        estimated_price = 150.0
        max_shares_by_risk = int(risk_amount / estimated_price)
        
        # Apply position size limits
        max_shares_by_limit = int(portfolio_value * self.risk_limits["max_position_size"] / estimated_price)
        
        position_size = min(max_shares_by_risk, max_shares_by_limit, 100)  # Cap at 100 shares
        
        write_log(self.name, "risk", f"Calculated position size for {symbol}: {position_size} shares")
        return max(1, position_size)  # Minimum 1 share
    
    async def execute_momentum_strategy(self) -> Dict:
        """Execute momentum-based trading strategy"""
        
        strategy_name = "momentum"
        if strategy_name not in self.strategies or not self.strategies[strategy_name]["active"]:
            return {"status": "inactive"}
        
        write_log(self.name, "strategy", f"Executing {strategy_name} strategy")
        
        # Screen for momentum stocks
        screening_criteria = {
            "min_volume": 1000000,
            "price_change_5d": 0.05,  # 5% gain in 5 days
            "max_results": 3
        }
        
        candidates = await self.screen_stocks(screening_criteria)
        results = {"strategy": strategy_name, "actions": []}
        
        for symbol in candidates:
            try:
                position_size = await self.calculate_position_size(symbol)
                rationale = f"Momentum strategy: {symbol} showing strong upward trend"
                
                result = self.account.buy_shares(symbol, position_size, rationale)
                results["actions"].append({
                    "action": "buy",
                    "symbol": symbol,
                    "quantity": position_size,
                    "result": "success"
                })
                
                # Update strategy performance
                self.strategies[strategy_name]["performance"]["trades"] += 1
                
            except Exception as e:
                results["actions"].append({
                    "action": "buy",
                    "symbol": symbol,
                    "result": "failed",
                    "error": str(e)
                })
        
        return results
    
    async def execute_mean_reversion_strategy(self) -> Dict:
        """Execute mean reversion trading strategy"""
        
        strategy_name = "mean_reversion"
        if strategy_name not in self.strategies or not self.strategies[strategy_name]["active"]:
            return {"status": "inactive"}
        
        write_log(self.name, "strategy", f"Executing {strategy_name} strategy")
        
        # Look for oversold stocks to buy
        screening_criteria = {
            "price_change_5d": -0.1,  # 10% decline in 5 days
            "rsi": 30,  # Oversold condition
            "max_results": 2
        }
        
        candidates = await self.screen_stocks(screening_criteria)
        results = {"strategy": strategy_name, "actions": []}
        
        for symbol in candidates:
            try:
                position_size = await self.calculate_position_size(symbol, risk_per_trade=0.015)
                rationale = f"Mean reversion: {symbol} oversold, expecting bounce"
                
                result = self.account.buy_shares(symbol, position_size, rationale)
                results["actions"].append({
                    "action": "buy",
                    "symbol": symbol,
                    "quantity": position_size,
                    "result": "success"
                })
                
                self.strategies[strategy_name]["performance"]["trades"] += 1
                
            except Exception as e:
                results["actions"].append({
                    "action": "buy",
                    "symbol": symbol,
                    "result": "failed",
                    "error": str(e)
                })
        
        return results
    
    async def execute_risk_management(self) -> Dict:
        """Execute risk management rules"""
        
        write_log(self.name, "risk", "Executing risk management checks")
        
        portfolio_value = self.account.calculate_portfolio_value()
        holdings = self.account.get_holdings()
        actions = []
        
        # Check position sizes
        for symbol, quantity in holdings.items():
            # Assume $150 average price for demo
            position_value = quantity * 150
            position_percentage = position_value / portfolio_value
            
            if position_percentage > self.risk_limits["max_position_size"] * 1.2:  # 20% buffer
                # Reduce position size
                shares_to_sell = int(quantity * 0.3)  # Sell 30% of position
                rationale = f"Risk management: reducing oversized position in {symbol}"
                
                try:
                    result = self.account.sell_shares(symbol, shares_to_sell, rationale)
                    actions.append({
                        "action": "sell",
                        "symbol": symbol,
                        "quantity": shares_to_sell,
                        "reason": "position_size_limit",
                        "result": "success"
                    })
                except Exception as e:
                    actions.append({
                        "action": "sell",
                        "symbol": symbol,
                        "result": "failed",
                        "error": str(e)
                    })
        
        return {"risk_management": actions}
    
    async def run_trading_cycle(self) -> Dict:
        """Run a complete trading cycle"""
        
        cycle_start = self._get_timestamp()
        write_log(self.name, "cycle", f"Starting trading cycle at {cycle_start}")
        
        results = {
            "timestamp": cycle_start,
            "market_analysis": {},
            "strategy_results": {},
            "risk_management": {},
            "portfolio_summary": {}
        }
        
        try:
            # 1. Market Analysis
            results["market_analysis"] = await self.analyze_market_sentiment()
            
            # 2. Execute Strategies
            if "momentum" in self.strategies:
                results["strategy_results"]["momentum"] = await self.execute_momentum_strategy()
            
            if "mean_reversion" in self.strategies:
                results["strategy_results"]["mean_reversion"] = await self.execute_mean_reversion_strategy()
            
            # 3. Risk Management
            results["risk_management"] = await self.execute_risk_management()
            
            # 4. Portfolio Summary
            results["portfolio_summary"] = {
                "total_value": self.account.calculate_portfolio_value(),
                "cash_balance": self.account.balance,
                "holdings": self.account.get_holdings(),
                "recent_transactions": self.account.list_transactions()[-5:]  # Last 5 transactions
            }
            
            write_log(self.name, "cycle", "Trading cycle completed successfully")
            
        except Exception as e:
            write_log(self.name, "error", f"Trading cycle error: {e}")
            results["error"] = str(e)
        
        return results
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        
        portfolio_value = self.account.calculate_portfolio_value()
        total_pnl = self.account.calculate_profit_loss(portfolio_value)
        transactions = self.account.list_transactions()
        
        # Calculate win/loss ratio
        profitable_trades = len([t for t in transactions if t["quantity"] < 0])  # Sales
        total_trades = len(transactions)
        
        report = {
            "account_name": self.name,
            "current_portfolio_value": portfolio_value,
            "total_pnl": total_pnl,
            "total_trades": total_trades,
            "win_rate": (profitable_trades / max(total_trades, 1)) * 100,
            "active_strategies": len([s for s in self.strategies.values() if s["active"]]),
            "current_holdings": len(self.account.get_holdings()),
            "strategy_performance": self.strategies
        }
        
        return report
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def advanced_trading_example():
    """Example usage of advanced trading bot"""
    
    # Create trading bot
    bot = AdvancedTradingBot("advanced_trader", initial_balance=50000)
    
    # Add trading strategies
    bot.add_strategy("momentum", {
        "lookback_period": 5,
        "min_momentum": 0.05,
        "max_positions": 3
    })
    
    bot.add_strategy("mean_reversion", {
        "oversold_threshold": 30,
        "lookback_period": 10,
        "max_positions": 2
    })
    
    print("🤖 Advanced Trading Bot initialized")
    print(f"Initial portfolio value: ${bot.account.calculate_portfolio_value():,.2f}")
    
    # Run multiple trading cycles
    cycle_results = []
    
    for cycle in range(3):
        print(f"\n{'='*50}")
        print(f"TRADING CYCLE {cycle + 1}")
        print(f"{'='*50}")
        
        result = await bot.run_trading_cycle()
        cycle_results.append(result)
        
        # Print cycle summary
        print(f"\n📊 Cycle {cycle + 1} Summary:")
        print(f"Portfolio Value: ${result['portfolio_summary']['total_value']:,.2f}")
        print(f"Cash Balance: ${result['portfolio_summary']['cash_balance']:,.2f}")
        print(f"Holdings: {len(result['portfolio_summary']['holdings'])} positions")
        
        # Show strategy actions
        for strategy_name, strategy_result in result["strategy_results"].items():
            if "actions" in strategy_result:
                successful_actions = len([a for a in strategy_result["actions"] if a["result"] == "success"])
                print(f"{strategy_name.title()} Strategy: {successful_actions} successful actions")
        
        # Brief pause between cycles
        await asyncio.sleep(1)
    
    # Generate final performance report
    performance_report = bot.get_performance_report()
    
    print(f"\n{'='*50}")
    print("FINAL PERFORMANCE REPORT")
    print(f"{'='*50}")
    
    print(f"Final Portfolio Value: ${performance_report['current_portfolio_value']:,.2f}")
    print(f"Total P&L: ${performance_report['total_pnl']:,.2f}")
    print(f"Total Trades: {performance_report['total_trades']}")
    print(f"Win Rate: {performance_report['win_rate']:.1f}%")
    print(f"Active Holdings: {performance_report['current_holdings']}")
    
    # Save detailed results
    detailed_results = {
        "performance_report": performance_report,
        "cycle_results": cycle_results,
        "final_holdings": bot.account.get_holdings(),
        "transaction_history": bot.account.list_transactions()
    }
    
    with open("advanced_trading_results.json", "w") as f:
        json.dump(detailed_results, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: advanced_trading_results.json")
    
    # Show recent logs
    recent_logs = list(read_log(bot.name, last_n=10))
    print(f"\n📋 Recent Activity Logs:")
    for timestamp, log_type, message in recent_logs[-5:]:
        print(f"{timestamp} [{log_type}] {message}")

if __name__ == "__main__":
    asyncio.run(advanced_trading_example())
```

---

## Advanced Integration Patterns

### Cross-Module Integration

Example of using multiple modules together:

```python
# example_cross_module_integration.py
import asyncio
from typing import Dict, List

# Import from different modules
from foundations.app import Me
from sidekick import Sidekick
from accounts import Account
from creator import Creator

class IntegratedAISystem:
    """System that integrates multiple AI modules"""
    
    def __init__(self):
        self.personal_assistant = None
        self.workflow_agent = None
        self.trading_account = None
        self.agent_creator = None
        self.system_status = {}
    
    async def initialize_all_modules(self):
        """Initialize all AI modules"""
        
        print("🚀 Initializing Integrated AI System...")
        
        # Initialize personal assistant (Module 1)
        try:
            self.personal_assistant = Me()
            self.system_status["personal_assistant"] = "active"
            print("✅ Personal Assistant initialized")
        except Exception as e:
            print(f"❌ Personal Assistant failed: {e}")
            self.system_status["personal_assistant"] = "failed"
        
        # Initialize workflow agent (Module 4)
        try:
            self.workflow_agent = Sidekick()
            await self.workflow_agent.setup()
            self.system_status["workflow_agent"] = "active"
            print("✅ Workflow Agent initialized")
        except Exception as e:
            print(f"❌ Workflow Agent failed: {e}")
            self.system_status["workflow_agent"] = "failed"
        
        # Initialize trading account (Module 6)
        try:
            self.trading_account = Account.get("integrated_system")
            if self.trading_account.balance == 0:
                self.trading_account.deposit(10000)
            self.system_status["trading_account"] = "active"
            print("✅ Trading Account initialized")
        except Exception as e:
            print(f"❌ Trading Account failed: {e}")
            self.system_status["trading_account"] = "failed"
        
        print(f"\n📊 System Status: {self.system_status}")
    
    async def execute_integrated_workflow(self, user_request: str) -> Dict:
        """Execute a workflow that uses multiple modules"""
        
        workflow_result = {
            "user_request": user_request,
            "steps": [],
            "final_result": None
        }
        
        # Step 1: Personal assistant analyzes the request
        if self.system_status.get("personal_assistant") == "active":
            print("\n🤖 Step 1: Personal Assistant Analysis")
            try:
                analysis = self.personal_assistant.chat(
                    f"Analyze this request and suggest an action plan: {user_request}",
                    []
                )
                workflow_result["steps"].append({
                    "step": "personal_analysis",
                    "module": "personal_assistant",
                    "result": analysis,
                    "status": "success"
                })
                print("✅ Personal analysis completed")
            except Exception as e:
                workflow_result["steps"].append({
                    "step": "personal_analysis",
                    "module": "personal_assistant",
                    "error": str(e),
                    "status": "failed"
                })
        
        # Step 2: Workflow agent executes detailed tasks
        if self.system_status.get("workflow_agent") == "active":
            print("\n⚙️ Step 2: Workflow Agent Execution")
            try:
                workflow_history = await self.workflow_agent.run_superstep(
                    message=user_request,
                    success_criteria="Provide comprehensive results for the user request",
                    history=[]
                )
                
                workflow_result["steps"].append({
                    "step": "workflow_execution",
                    "module": "workflow_agent",
                    "result": workflow_history[-2]['content'] if len(workflow_history) >= 2 else "No result",
                    "status": "success"
                })
                print("✅ Workflow execution completed")
            except Exception as e:
                workflow_result["steps"].append({
                    "step": "workflow_execution",
                    "module": "workflow_agent",
                    "error": str(e),
                    "status": "failed"
                })
        
        # Step 3: If request involves trading, use trading module
        if "trade" in user_request.lower() or "invest" in user_request.lower():
            if self.system_status.get("trading_account") == "active":
                print("\n💰 Step 3: Trading Account Action")
                try:
                    # Simple trading logic based on request
                    if "buy" in user_request.lower():
                        # Extract symbol (simplified)
                        symbols = ["AAPL", "GOOGL", "MSFT"]  # Default options
                        symbol = symbols[0]  # Use first as default
                        
                        trade_result = self.trading_account.buy_shares(
                            symbol, 5, f"Integrated system trade based on: {user_request}"
                        )
                        
                        workflow_result["steps"].append({
                            "step": "trading_action",
                            "module": "trading_account",
                            "result": trade_result,
                            "status": "success"
                        })
                        print("✅ Trading action completed")
                    
                except Exception as e:
                    workflow_result["steps"].append({
                        "step": "trading_action",
                        "module": "trading_account",
                        "error": str(e),
                        "status": "failed"
                    })
        
        # Generate final integrated result
        successful_steps = [s for s in workflow_result["steps"] if s["status"] == "success"]
        
        if successful_steps:
            final_result = "Integrated workflow completed successfully:\n\n"
            for step in successful_steps:
                final_result += f"✅ {step['step'].replace('_', ' ').title()}:\n"
                result_text = step["result"]
                if isinstance(result_text, str):
                    final_result += f"{result_text[:200]}...\n\n"
                else:
                    final_result += f"{str(result_text)[:200]}...\n\n"
        else:
            final_result = "Workflow completed with limited success. Check individual step results."
        
        workflow_result["final_result"] = final_result
        return workflow_result
    
    async def cleanup(self):
        """Cleanup all modules"""
        if self.workflow_agent:
            self.workflow_agent.cleanup()

async def integration_example():
    """Example of cross-module integration"""
    
    system = IntegratedAISystem()
    await system.initialize_all_modules()
    
    try:
        # Example requests that use multiple modules
        requests = [
            "Research the best AI stocks and help me invest $1000",
            "Create a comprehensive report on renewable energy trends",
            "Analyze my portfolio and suggest improvements"
        ]
        
        for i, request in enumerate(requests, 1):
            print(f"\n{'='*60}")
            print(f"INTEGRATED WORKFLOW {i}: {request}")
            print(f"{'='*60}")
            
            result = await system.execute_integrated_workflow(request)
            
            print(f"\n📋 Workflow Result:")
            print(f"Steps completed: {len([s for s in result['steps'] if s['status'] == 'success'])}/{len(result['steps'])}")
            print(f"\n📄 Final Result:")
            print(result["final_result"])
            
            # Save individual results
            filename = f"integrated_workflow_{i}.json"
            with open(filename, "w") as f:
                import json
                json.dump(result, f, indent=2, default=str)
            
            print(f"💾 Detailed results saved to: {filename}")
    
    finally:
        await system.cleanup()

if __name__ == "__main__":
    asyncio.run(integration_example())
```

---

## Troubleshooting Common Issues

### Environment Setup Issues

```python
# troubleshooting/environment_check.py
import os
from dotenv import load_dotenv

def check_environment():
    """Check if all required environment variables are set"""
    
    load_dotenv()
    
    required_vars = [
        "OPENAI_API_KEY",
        "PUSHOVER_TOKEN", 
        "PUSHOVER_USER",
        "SENDGRID_API_KEY",
        "SENDGRID_FROM_EMAIL",
        "SERPER_API_KEY"
    ]
    
    optional_vars = [
        "DEEPSEEK_API_KEY",
        "GROK_API_KEY", 
        "GOOGLE_API_KEY",
        "OPENROUTER_API_KEY"
    ]
    
    print("🔍 Environment Variable Check")
    print("=" * 40)
    
    missing_required = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * len(value[:4])}...")
        else:
            print(f"❌ {var}: Not set")
            missing_required.append(var)
    
    print(f"\n📋 Optional Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        status = "✅" if value else "⚪"
        print(f"{status} {var}: {'Set' if value else 'Not set'}")
    
    if missing_required:
        print(f"\n⚠️  Missing required variables: {', '.join(missing_required)}")
        print("Please add these to your .env file")
        return False
    else:
        print(f"\n🎉 All required environment variables are set!")
        return True

if __name__ == "__main__":
    check_environment()
```

### API Connection Testing

```python
# troubleshooting/api_test.py
import asyncio
from openai import AsyncOpenAI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

async def test_apis():
    """Test connections to various APIs"""
    
    print("🔌 API Connection Test")
    print("=" * 30)
    
    # Test OpenAI
    try:
        client = AsyncOpenAI()
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=10
        )
        print("✅ OpenAI API: Connected")
    except Exception as e:
        print(f"❌ OpenAI API: {e}")
    
    # Test Pushover
    try:
        pushover_response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv("PUSHOVER_TOKEN"),
                "user": os.getenv("PUSHOVER_USER"),
                "message": "API Test"
            },
            timeout=10
        )
        if pushover_response.status_code == 200:
            print("✅ Pushover API: Connected")
        else:
            print(f"⚠️  Pushover API: Status {pushover_response.status_code}")
    except Exception as e:
        print(f"❌ Pushover API: {e}")
    
    # Test Serper (Google Search)
    try:
        serper_response = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": os.getenv("SERPER_API_KEY")},
            json={"q": "test query"},
            timeout=10
        )
        if serper_response.status_code == 200:
            print("✅ Serper API: Connected")
        else:
            print(f"⚠️  Serper API: Status {serper_response.status_code}")
    except Exception as e:
        print(f"❌ Serper API: {e}")

if __name__ == "__main__":
    asyncio.run(test_apis())
```

This comprehensive usage examples document provides practical, runnable code for all modules in the Master AI Agentic Engineering course. Each example demonstrates real-world usage patterns and best practices for building sophisticated AI agent systems.