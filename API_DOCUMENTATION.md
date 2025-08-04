# Master AI Agentic Engineering - API Documentation

## Overview

This documentation covers all public APIs, functions, and components in the Master AI Agentic Engineering course codebase. The project is structured into 6 main modules, each focusing on different AI agent frameworks and technologies.

## Project Structure

```
├── 1_foundations/     # Basic AI agent foundations with OpenAI
├── 2_openai/         # OpenAI Agents SDK implementations
├── 3_crew/           # CrewAI multi-agent systems
├── 4_langgraph/      # LangGraph workflow agents
├── 5_autogen/        # AutoGen distributed agents
├── 6_mcp/            # Model Context Protocol (MCP) implementations
├── guides/           # Learning guides and tutorials
└── setup/            # Environment setup utilities
```

## Dependencies

Key dependencies include:
- `openai>=1.68.2` - OpenAI API client
- `crewai` - Multi-agent framework
- `langgraph>=0.3.18` - Graph-based workflows
- `autogen-agentchat>=0.4.9.2` - AutoGen framework
- `gradio>=5.22.0` - Web UI framework
- `mcp>=1.5.0` - Model Context Protocol

---

# Module 1: Foundations

## Overview
The foundations module provides basic AI agent implementations using OpenAI's API with tool calling capabilities.

## Core Components

### `Me` Class

**Location**: `1_foundations/app.py`

A personal AI assistant that represents a specific person's background and can handle inquiries.

#### Constructor
```python
Me()
```

**Description**: Initializes the assistant with personal information from PDF and text files.

**Dependencies**:
- Requires `me/linkedin.pdf` - LinkedIn profile export
- Requires `me/summary.txt` - Personal summary text

#### Methods

##### `chat(message: str, history: List[Dict]) -> str`
**Description**: Main chat interface that processes user messages and returns responses.

**Parameters**:
- `message` (str): User's input message
- `history` (List[Dict]): Conversation history in message format

**Returns**: 
- `str`: AI assistant's response

**Example**:
```python
me = Me()
response = me.chat("Tell me about your experience", [])
print(response)
```

##### `handle_tool_call(tool_calls) -> List[Dict]`
**Description**: Processes tool calls from the OpenAI API.

**Parameters**:
- `tool_calls`: Tool call objects from OpenAI response

**Returns**:
- `List[Dict]`: Tool call results in OpenAI format

##### `system_prompt() -> str`
**Description**: Generates the system prompt with personal context.

**Returns**:
- `str`: Complete system prompt with background information

## Utility Functions

### `push(text: str)`
**Description**: Sends push notifications via Pushover API.

**Parameters**:
- `text` (str): Message to send

**Environment Variables Required**:
- `PUSHOVER_TOKEN`: Pushover application token
- `PUSHOVER_USER`: Pushover user key

### `record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided") -> Dict`
**Description**: Records user contact information via push notification.

**Parameters**:
- `email` (str): User's email address (required)
- `name` (str): User's name (optional)
- `notes` (str): Additional context (optional)

**Returns**:
- `Dict`: Status confirmation

### `record_unknown_question(question: str) -> Dict`
**Description**: Records questions that couldn't be answered.

**Parameters**:
- `question` (str): The unanswered question

**Returns**:
- `Dict`: Status confirmation

## Tool Definitions

The module includes JSON schema definitions for:
- `record_user_details_json`: Schema for recording user details
- `record_unknown_question_json`: Schema for recording unknown questions

---

# Module 2: OpenAI Agents SDK

## Overview
This module demonstrates advanced OpenAI agent implementations with specialized research capabilities.

## Deep Research System

### `run(query: str)`
**Location**: `2_openai/deep_research/deep_research.py`

**Description**: Executes a comprehensive research workflow using multiple specialized agents.

**Parameters**:
- `query` (str): Research topic or question

**Example**:
```python
import asyncio
from deep_research import run

result = asyncio.run(run("Impact of AI on healthcare"))
```

### Research Manager

#### `ResearchManager` Class
**Location**: `2_openai/deep_research/research_manager.py`

Coordinates the research process across multiple agents.

##### Methods

###### `__init__()`
**Description**: Initializes the research manager with OpenAI client.

###### `research(query: str) -> str`
**Description**: Executes the complete research workflow.

**Parameters**:
- `query` (str): Research query

**Returns**:
- `str`: Comprehensive research report

### Email Integration

#### `send_email(subject: str, html_body: str) -> Dict[str, str]`
**Location**: `2_openai/deep_research/email_agent.py`

**Description**: Sends research reports via email using SendGrid.

**Parameters**:
- `subject` (str): Email subject line
- `html_body` (str): HTML formatted email body

**Returns**:
- `Dict[str, str]`: Delivery status

**Environment Variables Required**:
- `SENDGRID_API_KEY`: SendGrid API key
- `SENDGRID_FROM_EMAIL`: Sender email address

## Data Models

### `WebSearchItem`
```python
class WebSearchItem(BaseModel):
    search_term: str
    search_reason: str
```

### `WebSearchPlan`
```python
class WebSearchPlan(BaseModel):
    search_items: List[WebSearchItem]
```

### `ReportData`
```python
class ReportData(BaseModel):
    title: str
    content: str
```

---

# Module 3: CrewAI

## Overview
CrewAI implementations for multi-agent collaboration systems.

## Debate System

### `Debate` Class
**Location**: `3_crew/debate/src/debate/crew.py`

**Description**: Orchestrates a debate between multiple AI agents.

#### Methods

##### `crew() -> Crew`
**Description**: Creates and configures the debate crew.

**Returns**:
- `Crew`: Configured CrewAI crew instance

##### `run()`
**Location**: `3_crew/debate/src/debate/main.py`

**Description**: Executes a debate on a given motion.

**Example**:
```python
from debate.main import run

# Runs debate with default motion
run()
```

**Default Input**:
```python
inputs = {
    'motion': 'There needs to be strict laws to regulate LLMs'
}
```

## Financial Research System

### `ResearchCrew` Class
**Location**: `3_crew/financial_researcher/src/financial_researcher/crew.py`

**Description**: Coordinates financial research and analysis.

#### Methods

##### `crew() -> Crew`
**Description**: Creates and configures the research crew.

##### `run()`
**Location**: `3_crew/financial_researcher/src/financial_researcher/main.py`

**Description**: Executes financial research for a company.

**Example**:
```python
from financial_researcher.main import run

# Analyzes Apple by default
run()
```

**Default Input**:
```python
inputs = {
    'company': 'Apple'
}
```

**Output**: Saves report to `output/report.md`

---

# Module 4: LangGraph

## Overview
LangGraph-based workflow agents with tool integration and state management.

## Sidekick Agent System

### `Sidekick` Class
**Location**: `4_langgraph/sidekick.py`

**Description**: An autonomous AI assistant that can browse the web, execute code, and complete complex tasks.

#### Constructor
```python
Sidekick()
```

#### Methods

##### `async setup()`
**Description**: Initializes the sidekick with tools and builds the workflow graph.

**Must be called before using the sidekick.**

##### `async run_superstep(message: str, success_criteria: str, history: List) -> List`
**Description**: Executes a complete task workflow.

**Parameters**:
- `message` (str): Task description or user message
- `success_criteria` (str): Criteria for task completion
- `history` (List): Conversation history

**Returns**:
- `List`: Updated conversation history with results

**Example**:
```python
import asyncio

async def main():
    sidekick = Sidekick()
    await sidekick.setup()
    
    history = await sidekick.run_superstep(
        message="Research the latest AI developments",
        success_criteria="Provide a comprehensive summary with sources",
        history=[]
    )
    
    print(history[-2]['content'])  # Assistant's response
    sidekick.cleanup()

asyncio.run(main())
```

##### `cleanup()`
**Description**: Closes browser and cleans up resources.

#### Internal Methods

##### `worker(state: State) -> Dict[str, Any]`
**Description**: Main worker node that processes tasks and uses tools.

##### `evaluator(state: State) -> State`
**Description**: Evaluates if task completion criteria have been met.

##### `worker_router(state: State) -> str`
**Description**: Routes between worker and tools based on response type.

### State Management

#### `State` TypedDict
```python
class State(TypedDict):
    messages: Annotated[List[Any], add_messages]
    success_criteria: str
    feedback_on_work: Optional[str]
    success_criteria_met: bool
    user_input_needed: bool
```

#### `EvaluatorOutput` Model
```python
class EvaluatorOutput(BaseModel):
    feedback: str
    success_criteria_met: bool
    user_input_needed: bool
```

## Tool Integration

### `playwright_tools()`
**Location**: `4_langgraph/sidekick_tools.py`

**Description**: Initializes Playwright browser tools for web interaction.

**Returns**:
- `Tuple[List[Tool], Browser, Playwright]`: Tools, browser instance, and playwright instance

### `other_tools()`
**Description**: Provides additional tools including file management, search, and Python execution.

**Returns**:
- `List[Tool]`: Collection of utility tools

#### Available Tools:
- **File Management**: Read, write, create, delete files in sandbox
- **Web Search**: Google search via Serper API
- **Wikipedia**: Wikipedia article lookup
- **Python REPL**: Execute Python code
- **Push Notifications**: Send notifications via Pushover

### Utility Functions

#### `push(text: str) -> str`
**Description**: Sends push notification.

**Parameters**:
- `text` (str): Notification message

**Environment Variables Required**:
- `PUSHOVER_TOKEN`: Pushover app token
- `PUSHOVER_USER`: Pushover user key

---

# Module 5: AutoGen

## Overview
AutoGen-based distributed agent systems with dynamic agent creation.

## Creator Agent System

### `Creator` Class
**Location**: `5_autogen/creator.py`

**Description**: A meta-agent that can create new AI agents dynamically.

#### Constructor
```python
Creator(name: str)
```

**Parameters**:
- `name` (str): Name identifier for the creator agent

#### Methods

##### `get_user_prompt() -> str`
**Description**: Generates prompt for creating new agents based on template.

**Returns**:
- `str`: Complete prompt with agent template

##### `async handle_my_message_type(message: messages.Message, ctx: MessageContext) -> messages.Message`
**Description**: Message handler that creates new agents and registers them with the runtime.

**Parameters**:
- `message` (messages.Message): Message containing filename for new agent
- `ctx` (MessageContext): Message context

**Returns**:
- `messages.Message`: Response from newly created agent

**Process**:
1. Generates new agent code based on template
2. Saves code to specified filename
3. Imports and registers agent with runtime
4. Sends initial message to new agent

### Message Types

#### `Message` Class
**Location**: `5_autogen/messages.py`

```python
class Message:
    content: str
```

### Agent Template System

The creator uses `agent.py` as a template for generating new agents. New agents must:
- Inherit from `RoutedAgent`
- Have class name `Agent`
- Include `__init__` method accepting `name` parameter
- Implement required message handlers

---

# Module 6: Model Context Protocol (MCP)

## Overview
Comprehensive trading simulation system using MCP for tool integration and agent communication.

## Trading Application

### `create_ui()`
**Location**: `6_mcp/app.py`

**Description**: Creates the main Gradio interface for the trading simulation.

**Returns**:
- `gr.Blocks`: Configured Gradio interface

**Example**:
```python
from app import create_ui

ui = create_ui()
ui.launch(inbrowser=True)
```

### `Trader` Class (UI)
**Location**: `6_mcp/app.py`

**Description**: UI representation of a trader with portfolio visualization.

#### Constructor
```python
Trader(name: str, lastname: str, model_name: str)
```

#### Methods

##### `get_portfolio_value() -> str`
**Description**: Returns formatted portfolio value with P&L.

##### `get_portfolio_value_chart()`
**Description**: Generates Plotly chart of portfolio performance.

##### `get_holdings_df() -> pd.DataFrame`
**Description**: Returns current holdings as DataFrame.

##### `get_transactions_df() -> pd.DataFrame`
**Description**: Returns transaction history as DataFrame.

##### `get_logs(previous=None) -> str`
**Description**: Returns formatted log entries with color coding.

## Account Management

### `Account` Class
**Location**: `6_mcp/accounts.py`

**Description**: Core account management with trading capabilities.

#### Class Methods

##### `Account.get(name: str) -> Account`
**Description**: Retrieves or creates account for given name.

**Parameters**:
- `name` (str): Account holder name

**Returns**:
- `Account`: Account instance

#### Instance Methods

##### `deposit(amount: float)`
**Description**: Deposits funds into account.

**Parameters**:
- `amount` (float): Deposit amount (must be positive)

**Raises**:
- `ValueError`: If amount is not positive

##### `withdraw(amount: float)`
**Description**: Withdraws funds from account.

**Parameters**:
- `amount` (float): Withdrawal amount

**Raises**:
- `ValueError`: If insufficient funds

##### `buy_shares(symbol: str, quantity: int, rationale: str) -> str`
**Description**: Purchases shares of specified stock.

**Parameters**:
- `symbol` (str): Stock symbol
- `quantity` (int): Number of shares
- `rationale` (str): Reason for purchase

**Returns**:
- `str`: Transaction confirmation with account details

**Raises**:
- `ValueError`: If insufficient funds or invalid symbol

##### `sell_shares(symbol: str, quantity: int, rationale: str) -> str`
**Description**: Sells shares of specified stock.

**Parameters**:
- `symbol` (str): Stock symbol
- `quantity` (int): Number of shares
- `rationale` (str): Reason for sale

**Returns**:
- `str`: Transaction confirmation with account details

**Raises**:
- `ValueError`: If insufficient shares

##### `calculate_portfolio_value() -> float`
**Description**: Calculates total portfolio value including cash and holdings.

**Returns**:
- `float`: Total portfolio value

##### `calculate_profit_loss(portfolio_value: float) -> float`
**Description**: Calculates profit/loss from initial investment.

**Parameters**:
- `portfolio_value` (float): Current portfolio value

**Returns**:
- `float`: Profit (positive) or loss (negative)

##### `get_holdings() -> Dict[str, int]`
**Description**: Returns current stock holdings.

**Returns**:
- `Dict[str, int]`: Symbol to quantity mapping

##### `list_transactions() -> List[Dict]`
**Description**: Returns transaction history.

**Returns**:
- `List[Dict]`: List of transaction dictionaries

##### `report() -> str`
**Description**: Generates comprehensive account report in JSON format.

**Returns**:
- `str`: JSON formatted account report

##### `get_strategy() -> str`
**Description**: Returns current investment strategy.

##### `change_strategy(strategy: str) -> str`
**Description**: Updates investment strategy.

**Parameters**:
- `strategy` (str): New investment strategy

**Returns**:
- `str`: Confirmation message

### `Transaction` Model
```python
class Transaction(BaseModel):
    symbol: str
    quantity: int
    price: float
    timestamp: str
    rationale: str
```

#### Methods

##### `total() -> float`
**Description**: Calculates total transaction value.

**Returns**:
- `float`: quantity × price

## Trading Agent System

### `Trader` Class (Agent)
**Location**: `6_mcp/traders.py`

**Description**: AI trading agent with research capabilities.

#### Constructor
```python
Trader(name: str, lastname: str = "Trader", model_name: str = "gpt-4o-mini")
```

#### Methods

##### `async create_agent(trader_mcp_servers, researcher_mcp_servers) -> Agent`
**Description**: Creates trading agent with MCP server connections.

**Parameters**:
- `trader_mcp_servers`: List of MCP servers for trading tools
- `researcher_mcp_servers`: List of MCP servers for research tools

**Returns**:
- `Agent`: Configured trading agent

##### `async run()`
**Description**: Executes one trading cycle (trade or rebalance).

##### `async get_account_report() -> str`
**Description**: Retrieves current account status.

**Returns**:
- `str`: JSON formatted account report

### Model Integration

#### `get_model(model_name: str)`
**Description**: Returns appropriate model client based on model name.

**Supported Models**:
- OpenRouter models (contain "/")
- DeepSeek models (contain "deepseek")
- Grok models (contain "grok")
- Gemini models (contain "gemini")
- Default OpenAI models

## Database Operations

### Account Storage

#### `write_account(name: str, account_dict: Dict)`
**Location**: `6_mcp/database.py`

**Description**: Persists account data to SQLite database.

**Parameters**:
- `name` (str): Account name
- `account_dict` (Dict): Account data dictionary

#### `read_account(name: str) -> Dict | None`
**Description**: Retrieves account data from database.

**Parameters**:
- `name` (str): Account name

**Returns**:
- `Dict | None`: Account data or None if not found

### Logging System

#### `write_log(name: str, type: str, message: str)`
**Description**: Writes log entry to database.

**Parameters**:
- `name` (str): Entity name
- `type` (str): Log type (trace, agent, function, generation, response, account)
- `message` (str): Log message

#### `read_log(name: str, last_n: int = 10) -> List[Tuple]`
**Description**: Retrieves recent log entries.

**Parameters**:
- `name` (str): Entity name
- `last_n` (int): Number of recent entries

**Returns**:
- `List[Tuple]`: List of (datetime, type, message) tuples

### Market Data

#### `write_market(date: str, data: Dict)`
**Description**: Stores market data for specific date.

#### `read_market(date: str) -> Dict | None`
**Description**: Retrieves market data for specific date.

## MCP Client Integration

### Account Client

#### `async read_accounts_resource(name: str) -> str`
**Location**: `6_mcp/accounts_client.py`

**Description**: Reads account data via MCP protocol.

#### `async read_strategy_resource(name: str) -> str`
**Description**: Reads trading strategy via MCP protocol.

#### `async call_accounts_tool(tool_name: str, tool_args: Dict) -> str`
**Description**: Executes account operations via MCP tools.

---

# Common Patterns and Best Practices

## Environment Variables

Most modules require environment variables for API access:

```bash
# OpenAI
OPENAI_API_KEY=your_openai_key

# Pushover (notifications)
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user

# SendGrid (email)
SENDGRID_API_KEY=your_sendgrid_key
SENDGRID_FROM_EMAIL=your_email@domain.com

# Search
SERPER_API_KEY=your_serper_key

# Alternative Models
DEEPSEEK_API_KEY=your_deepseek_key
GROK_API_KEY=your_grok_key
GOOGLE_API_KEY=your_google_key
OPENROUTER_API_KEY=your_openrouter_key
```

## Error Handling

All modules implement comprehensive error handling:

```python
try:
    result = await agent.run()
except Exception as e:
    print(f"Error: {e}")
    # Handle gracefully
```

## Async/Await Pattern

Most advanced features use async/await:

```python
import asyncio

async def main():
    # Async operations
    result = await some_async_function()
    
asyncio.run(main())
```

## Resource Cleanup

Always clean up resources:

```python
try:
    # Use resources
    pass
finally:
    # Cleanup
    if hasattr(obj, 'cleanup'):
        obj.cleanup()
```

---

# Examples and Tutorials

## Quick Start Examples

### Basic Chat Agent
```python
from foundations.app import Me

# Initialize and use
me = Me()
response = me.chat("Hello!", [])
print(response)
```

### Research Agent
```python
import asyncio
from deep_research import run

async def research_example():
    result = await run("Future of renewable energy")
    print(result)

asyncio.run(research_example())
```

### Trading Simulation
```python
from accounts import Account

# Create account and trade
account = Account.get("trader1")
account.deposit(10000)
result = account.buy_shares("AAPL", 10, "Strong earnings report")
print(result)
```

### LangGraph Workflow
```python
import asyncio
from sidekick import Sidekick

async def workflow_example():
    sidekick = Sidekick()
    await sidekick.setup()
    
    history = await sidekick.run_superstep(
        message="Create a Python script that analyzes stock data",
        success_criteria="Script should be saved and functional",
        history=[]
    )
    
    sidekick.cleanup()

asyncio.run(workflow_example())
```

## Advanced Integration

### Multi-Agent Collaboration
```python
# CrewAI example
from debate.main import run as debate_run
from financial_researcher.main import run as research_run

# Run debate
debate_run()

# Run research
research_run()
```

### Custom Agent Creation
```python
# AutoGen example
from creator import Creator
import asyncio

async def create_custom_agent():
    creator = Creator("agent_creator")
    # Creator will generate new agent code
    result = await creator.handle_my_message_type(
        Message(content="custom_agent.py"),
        context
    )

asyncio.run(create_custom_agent())
```

---

# Support and Troubleshooting

## Common Issues

1. **API Key Errors**: Ensure all required environment variables are set
2. **Import Errors**: Check Python path and virtual environment
3. **Async Errors**: Use `asyncio.run()` for async functions
4. **Resource Leaks**: Always call cleanup methods

## Getting Help

- Check the `guides/` directory for detailed tutorials
- Review `setup/troubleshooting.ipynb` for common solutions
- Contact: ed@edwarddonner.com
- LinkedIn: https://www.linkedin.com/in/eddonner/

## Contributing

When extending the codebase:
1. Follow existing patterns and conventions
2. Add comprehensive error handling
3. Include docstrings and type hints
4. Update this documentation
5. Add tests where appropriate

---

*This documentation covers the complete public API surface of the Master AI Agentic Engineering course codebase. For implementation details and private methods, refer to the source code directly.*