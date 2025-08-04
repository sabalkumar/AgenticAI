# Master AI Agentic Engineering - Getting Started Guide

Welcome to the Master AI Agentic Engineering course! This guide will help you quickly get up and running with all the AI agent frameworks and tools in this comprehensive codebase.

## 🎯 Quick Start (5 Minutes)

### 1. Environment Setup

```bash
# Clone or navigate to the project directory
cd /path/to/master-ai-agentic-engineering

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
uv sync  # Preferred method
# OR: pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Core API Keys (Required)
OPENAI_API_KEY=your_openai_api_key_here
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_sender_email
SERPER_API_KEY=your_serper_api_key

# Optional: Alternative AI Models
DEEPSEEK_API_KEY=your_deepseek_api_key
GROK_API_KEY=your_grok_api_key
GOOGLE_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 3. Test Your Setup

```bash
# Run environment check
python troubleshooting/environment_check.py

# Test API connections
python troubleshooting/api_test.py
```

### 4. Try Your First Agent

```bash
# Start with the foundations module
cd 1_foundations
python app.py
```

🎉 **You're ready to go!** Open your browser to interact with your first AI agent.

---

## 📚 What's In This Course

This course teaches you to build AI agents using 6 different frameworks:

| Module | Framework | What You'll Build | Key Features |
|--------|-----------|-------------------|--------------|
| **1_foundations** | OpenAI API | Personal AI Assistant | Tool calling, custom functions |
| **2_openai** | OpenAI Agents SDK | Research System | Multi-agent workflows, email integration |
| **3_crew** | CrewAI | Collaborative Teams | Agent crews, structured tasks |
| **4_langgraph** | LangGraph | Workflow Agents | State management, complex workflows |
| **5_autogen** | AutoGen | Dynamic Agents | Agent creation, distributed systems |
| **6_mcp** | MCP Protocol | Trading Bots | Real-time data, financial analysis |

---

## 🚀 Learning Path

### Beginner Path (Start Here)

1. **Module 1: Foundations** - Learn basic AI agent concepts
2. **Module 2: OpenAI SDK** - Build research agents
3. **Module 3: CrewAI** - Create agent teams

### Intermediate Path

4. **Module 4: LangGraph** - Advanced workflows
5. **Module 6: MCP** - Real-world applications

### Advanced Path

6. **Module 5: AutoGen** - Dynamic agent systems
7. **Cross-Module Integration** - Combine multiple frameworks

---

## 🛠️ Module Deep Dives

### Module 1: Foundations (Start Here!)

**What you'll learn**: Basic AI agent concepts, tool integration, OpenAI API

**Quick Start**:
```bash
cd 1_foundations
python app.py
```

**Key Examples**:
- Personal AI assistant that knows about you
- Custom tool integration (weather, calculations)
- Push notifications and user tracking

**Time to complete**: 30 minutes

---

### Module 2: OpenAI Agents SDK

**What you'll learn**: Advanced research agents, multi-step workflows, email integration

**Quick Start**:
```bash
cd 2_openai/deep_research
python deep_research.py
```

**Key Examples**:
- Automated research system
- Multi-agent research pipeline
- Email report delivery

**Time to complete**: 1 hour

---

### Module 3: CrewAI

**What you'll learn**: Multi-agent collaboration, structured task management

**Quick Start**:
```bash
cd 3_crew/debate
crewai run
```

**Key Examples**:
- AI debate system
- Financial analysis crew
- Custom agent roles and tasks

**Time to complete**: 45 minutes

---

### Module 4: LangGraph

**What you'll learn**: State-based workflows, complex task orchestration

**Quick Start**:
```bash
cd 4_langgraph
python -c "
import asyncio
from sidekick import Sidekick

async def demo():
    sidekick = Sidekick()
    await sidekick.setup()
    result = await sidekick.run_superstep(
        'Create a simple Python script that prints Hello World',
        'Script should be saved and functional',
        []
    )
    print(result[-2]['content'])
    sidekick.cleanup()

asyncio.run(demo())
"
```

**Key Examples**:
- Advanced workflow agent
- Interactive task manager
- Dependency-based task execution

**Time to complete**: 1.5 hours

---

### Module 5: AutoGen

**What you'll learn**: Dynamic agent creation, distributed systems

**Quick Start**:
```bash
cd 5_autogen
python creator.py
```

**Key Examples**:
- Agent factory system
- Dynamic agent generation
- Multi-agent collaboration

**Time to complete**: 1 hour

---

### Module 6: MCP (Model Context Protocol)

**What you'll learn**: Real-world applications, trading systems, data persistence

**Quick Start**:
```bash
cd 6_mcp
python app.py  # Launch trading dashboard
```

**Key Examples**:
- Advanced trading bot
- Real-time portfolio management
- Risk management systems

**Time to complete**: 2 hours

---

## 🎨 Example Projects

### Project 1: Personal Research Assistant (Beginner)

Combine modules 1 and 2 to create a personal research assistant:

```python
# personal_research_assistant.py
from foundations.app import Me
from deep_research.deep_research import run
import asyncio

class PersonalResearcher:
    def __init__(self):
        self.assistant = Me()
    
    async def research_and_chat(self, topic):
        # Research the topic
        research = await run(topic)
        
        # Chat about the results
        response = self.assistant.chat(
            f"I researched '{topic}' and found: {research[:500]}... "
            f"Can you summarize the key insights?",
            []
        )
        return response

# Usage
async def main():
    researcher = PersonalResearcher()
    result = await researcher.research_and_chat("AI trends 2024")
    print(result)

asyncio.run(main())
```

### Project 2: Investment Analysis Team (Intermediate)

Use CrewAI and MCP for comprehensive investment analysis:

```python
# investment_analyzer.py
from crew.financial_researcher.main import run as analyze_company
from accounts import Account
import json

class InvestmentAnalyzer:
    def __init__(self):
        self.account = Account.get("investor")
        
    def analyze_and_invest(self, company, investment_amount):
        # Analyze company using CrewAI
        analysis = analyze_company()  # Configure for specific company
        
        # Make investment decision
        if "buy" in analysis.lower():
            shares = investment_amount // 150  # Assume $150/share
            result = self.account.buy_shares(
                company, shares, f"Based on analysis: {analysis[:100]}..."
            )
            return result
        
        return "Analysis suggests not to invest at this time"

# Usage
analyzer = InvestmentAnalyzer()
result = analyzer.analyze_and_invest("AAPL", 1000)
print(result)
```

### Project 3: Automated Content Pipeline (Advanced)

Integrate multiple modules for automated content creation:

```python
# content_pipeline.py
import asyncio
from sidekick import Sidekick
from creator import Creator
from deep_research.deep_research import run

class ContentPipeline:
    def __init__(self):
        self.workflow_agent = None
        self.content_creator = None
    
    async def initialize(self):
        self.workflow_agent = Sidekick()
        await self.workflow_agent.setup()
        
        self.content_creator = Creator("content_creator")
    
    async def create_content_series(self, topics):
        results = []
        
        for topic in topics:
            # Research the topic
            research = await run(topic)
            
            # Create content using workflow agent
            content = await self.workflow_agent.run_superstep(
                f"Create a blog post about {topic} based on this research: {research}",
                "Create engaging, well-structured blog post with SEO optimization",
                []
            )
            
            results.append({
                "topic": topic,
                "content": content[-2]['content'],
                "research": research
            })
        
        return results

# Usage
async def main():
    pipeline = ContentPipeline()
    await pipeline.initialize()
    
    topics = ["AI in Healthcare", "Future of Work", "Sustainable Technology"]
    content_series = await pipeline.create_content_series(topics)
    
    for item in content_series:
        print(f"Topic: {item['topic']}")
        print(f"Content: {item['content'][:200]}...")
        print("-" * 50)

asyncio.run(main())
```

---

## 🔧 Customization Guide

### Adding Custom Tools

1. **For Foundations Module**:
```python
# Add to 1_foundations/app.py
def my_custom_tool(param: str) -> dict:
    """Your custom function"""
    return {"result": f"Processed {param}"}

# Add tool definition
my_tool_json = {
    "name": "my_custom_tool",
    "description": "Description of what it does",
    "parameters": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
}

# Add to tools list
tools.append({"type": "function", "function": my_tool_json})
```

2. **For LangGraph Module**:
```python
# Add to 4_langgraph/sidekick_tools.py
from langchain.agents import Tool

def my_custom_function(input_text: str) -> str:
    """Your custom function"""
    return f"Processed: {input_text}"

my_tool = Tool(
    name="my_custom_tool",
    func=my_custom_function,
    description="Description of what it does"
)

# Add to other_tools function return
return file_tools + [push_tool, tool_search, python_repl, wiki_tool, my_tool]
```

### Creating Custom Agents

1. **CrewAI Custom Agent**:
```python
from crewai import Agent
from crewai_tools import SerperDevTool

custom_agent = Agent(
    role='Your Custom Role',
    goal='What the agent should achieve',
    backstory='Agent background and expertise',
    verbose=True,
    allow_delegation=False,
    tools=[SerperDevTool()]
)
```

2. **AutoGen Custom Agent**:
```python
# Create agent template file
agent_template = """
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages

class Agent(RoutedAgent):
    system_message = "Your custom system message here"
    
    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)
    
    @message_handler
    async def handle_my_message_type(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        return messages.Message(content=response.chat_message.content)
"""

# Save as custom_agent.py and use with Creator
```

---

## 📊 Performance Tips

### 1. API Rate Limiting
```python
import asyncio
from asyncio import Semaphore

# Limit concurrent API calls
semaphore = Semaphore(5)  # Max 5 concurrent calls

async def rate_limited_call(func, *args, **kwargs):
    async with semaphore:
        return await func(*args, **kwargs)
```

### 2. Caching Results
```python
import json
import os
from datetime import datetime, timedelta

class ResultCache:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, key, max_age_hours=24):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
                cache_time = datetime.fromisoformat(data['timestamp'])
                if datetime.now() - cache_time < timedelta(hours=max_age_hours):
                    return data['result']
        return None
    
    def set(self, key, result):
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w') as f:
            json.dump({
                'result': result,
                'timestamp': datetime.now().isoformat()
            }, f)

# Usage
cache = ResultCache()
cached_result = cache.get("research_ai_trends")
if not cached_result:
    cached_result = await run("AI trends 2024")
    cache.set("research_ai_trends", cached_result)
```

### 3. Error Handling Best Practices
```python
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def robust_agent_call(agent_func, *args, max_retries=3, **kwargs) -> Optional[str]:
    """Robust agent call with retries and error handling"""
    
    for attempt in range(max_retries):
        try:
            result = await agent_func(*args, **kwargs)
            logger.info(f"Agent call successful on attempt {attempt + 1}")
            return result
            
        except Exception as e:
            logger.warning(f"Agent call failed on attempt {attempt + 1}: {e}")
            
            if attempt == max_retries - 1:
                logger.error(f"Agent call failed after {max_retries} attempts")
                return None
            
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    return None
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "OpenAI API key not found"
**Solution**: 
```bash
# Check your .env file
cat .env | grep OPENAI_API_KEY

# If missing, add it:
echo "OPENAI_API_KEY=your_key_here" >> .env
```

### Issue 2: "Module not found" errors
**Solution**:
```bash
# Make sure you're in the right directory
pwd

# Install dependencies
uv sync
# OR
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

### Issue 3: CrewAI installation issues (Windows)
**Solution**:
```bash
# Install Microsoft Build Tools first
# Then:
uv tool install crewai
uv tool upgrade crewai
```

### Issue 4: Async/await errors
**Solution**:
```python
# Always use asyncio.run() for top-level async functions
import asyncio

async def my_async_function():
    # Your async code here
    pass

# Correct way to run
asyncio.run(my_async_function())

# Not: await my_async_function()  # This will fail outside async context
```

### Issue 5: Memory issues with large workflows
**Solution**:
```python
# Clean up resources properly
try:
    # Your agent code
    pass
finally:
    if hasattr(agent, 'cleanup'):
        agent.cleanup()
    
    # Force garbage collection for large objects
    import gc
    gc.collect()
```

---

## 🎓 Next Steps

### Immediate Next Steps (This Week)
1. ✅ Complete the quick start setup
2. ✅ Try one example from each module
3. ✅ Build your first custom agent
4. ✅ Join the community (LinkedIn: [@eddonner](https://www.linkedin.com/in/eddonner/))

### Short Term Goals (This Month)
1. 🎯 Complete all 6 modules
2. 🎯 Build a cross-module integration project
3. 🎯 Customize agents for your specific use case
4. 🎯 Share your creations with the community

### Long Term Goals (Next 3 Months)
1. 🚀 Deploy agents to production
2. 🚀 Build a commercial AI agent application
3. 🚀 Contribute to the open-source community
4. 🚀 Teach others what you've learned

---

## 📖 Additional Resources

### Documentation
- [API Documentation](API_DOCUMENTATION.md) - Complete API reference
- [Usage Examples](USAGE_EXAMPLES.md) - Practical code examples
- [Troubleshooting Guide](setup/troubleshooting.ipynb) - Common issues and solutions

### Course Materials
- [Video Tutorials](https://edwarddonner.com/2025/04/21/the-complete-agentic-ai-engineering-course/)
- [Learning Guides](guides/) - Step-by-step tutorials
- [Community Contributions](*/community_contributions/) - Examples from other students

### External Resources
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [CrewAI Documentation](https://docs.crewai.com)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)

---

## 🤝 Getting Help

### Community Support
- **LinkedIn**: Connect with [@eddonner](https://www.linkedin.com/in/eddonner/)
- **Email**: ed@edwarddonner.com
- **X/Twitter**: [@edwarddonner](https://x.com/edwarddonner)

### Self-Help Resources
1. Check the [troubleshooting guide](setup/troubleshooting.ipynb)
2. Review the [usage examples](USAGE_EXAMPLES.md)
3. Run the environment checker: `python troubleshooting/environment_check.py`
4. Test API connections: `python troubleshooting/api_test.py`

### Reporting Issues
When reporting issues, include:
1. Your operating system
2. Python version (`python --version`)
3. Error message (full stack trace)
4. Steps to reproduce
5. Your environment variables (without the actual keys)

---

## 🎉 Welcome to the Future of AI!

You're now equipped with everything you need to build sophisticated AI agent systems. This course will take you from beginner to expert in AI agent development.

**Remember**: The best way to learn is by doing. Start with the quick start guide, then dive into the modules that interest you most. Don't be afraid to experiment and break things - that's how you learn!

**Most importantly**: Have fun! You're learning cutting-edge technology that will shape the future. Enjoy the journey!

---

*Happy coding! 🚀*

**Edward Donner**  
*Creator, Master AI Agentic Engineering Course*