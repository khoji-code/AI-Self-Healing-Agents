# **🤖 Self-Healing Multi-Agent System**

**An intelligent, autonomous system where AI agents perform tasks, detect their own failures, and "heal" themselves using Qwen AI.**

## **📖 Overview**

This project demonstrates a robust **Multi-Agent Architecture** designed for stability in production environments. Unlike traditional automation scripts that crash when they encounter an unexpected error, this system features a dedicated **"Healing Agent"** (the Doctor) that actively monitors other worker agents.  
When a worker agent (e.g., a Database Monitor, Stock Tracker, or API Gateway) fails or behaves erratically, the Healing Agent steps in. It diagnoses the root cause using **Large Language Models (LLMs)**, generates a fix, and restores the agent to a healthy state—all without human intervention.

### **✨ Key Features**

* **🧠 Brain:** Powered by **Qwen 2.5** (via Hugging Face) for intelligent reasoning and diagnostics.  
* **⚕️ Self-Healing:** Agents automatically report health status; a "Doctor" agent intervenes to fix crashes using AI-generated strategies.  
* **🛡️ Fault Tolerance:** Includes retry logic, circuit breakers, backoff strategies, and error tracking.  
* **🔌 Modular:** Easily create new agents (e.g., Crypto, Weather, IoT) by simply subclassing the BaseAgent.  
* **💸 Cost-Effective:** Optimized to work with the free tier of the Hugging Face Inference API.

## **🏗️ Architecture**

The system is built on a "Hub and Spoke" model where a central manager orchestrates specialized workers.

1. **Base Agent (src/agents/base\_agent.py):** The skeleton code that every robot shares. It handles performance metrics, logging, error counting, and the safety execution wrapper.  
2. **Specialized Agents (src/agents/specialized\_agents.py):** The workers that perform specific tasks (e.g., processing data, monitoring websites).  
3. **Healing Agent (src/agents/healing\_agent.py):** The "Doctor" that listens for error signals and communicates with the AI to generate recovery plans.  
4. **Healing Graph (src/graph/healing\_graph.py):** The "Manager" (built with LangGraph) that routes tasks and decides when to escalate issues to the doctor.

## **🚀 Getting Started**

### **Prerequisites**

* **Python 3.9** or higher  
* A free [Hugging Face Account](https://huggingface.co/) (for the API Token)

### **1\. Installation**

Clone the repository and enter the directory:  
```
git clone https://github.com/khoji-code/AI-Self-Healing-Agents.git
```

cd AI-Self-Healing-Agents

Create and activate a virtual environment:  
\# macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

\# Windows  
python \-m venv venv  
venv\\Scripts\\activate

Create the requirements.txt file (copy and run this command block):  
cat \<\<EOF \> requirements.txt  
asyncio  
python-dotenv  
huggingface\_hub  
langgraph  
pytest  
numpy  
EOF

Install the dependencies:  
pip install \-r requirements.txt

### **2\. Configuration**

Create a .env file in the root directory to store your API key. This file is ignored by Git to protect your secrets.  
\# Create .env file (Mac/Linux)  
touch .env

Open the .env file and add your configuration (replace hf\_... with your actual token):  
\# .env content  
HF\_TOKEN=hf\_your\_token\_goes\_here  
QWEN\_MODEL=Qwen/Qwen2.5-7B-Instruct  
LOG\_LEVEL=INFO

*(Get your token from [Hugging Face Settings](https://huggingface.co/settings/tokens))*

## **💻 Usage**

### **🧪 Quick Verification**

Run the basic smoke test to ensure your environment and AI connection are set up correctly:  
python examples/quick\_start.py

### **🏭 Run the "Real World" Simulation**

This script launches a full IT monitoring simulation with Website, API, and Database agents running continuously. You will see them occasionally fail (simulated errors) and get "healed" by the doctor.  
python real\_world/run\_complete.py

### **📈 Run Custom Examples**

If you have created custom bots (like a Stock Monitor), you can run them here:  
python my\_stock\_bot.py

## **🛠️ How to Create Your Own Agent**

Creating a new robot is easy. You just need to inherit from BaseAgent and define the process() method.  
Create a file named my\_agent.py:  
from src.agents.base\_agent import BaseAgent  
import asyncio

class MyCustomAgent(BaseAgent):  
    def \_\_init\_\_(self):  
        \# Give your agent a unique ID and type  
        super().\_\_init\_\_(agent\_id="my\_worker", agent\_type="custom")

    async def process(self, task):  
        print(f"Processing task: {task}")  
          
        \# Your custom logic here...  
        \# If you raise an Exception here, the Healing Agent will catch it\!  
          
        return {"status": "done", "result": "success"}

\# Run it  
async def main():  
    agent \= MyCustomAgent()  
    await agent.execute({"data": "hello"})

if \_\_name\_\_ \== "\_\_main\_\_":  
    asyncio.run(main())

## **📂 Project Structure**

├── .env                    \# Secrets (Not uploaded to Git)  
├── .gitignore              \# Files to ignore  
├── README.md               \# This file  
├── requirements.txt        \# Python dependencies  
├── src/  
│   ├── agents/  
│   │   ├── base\_agent.py        \# The Skeleton (Parent Class)  
│   │   ├── healing\_agent.py     \# The Doctor (AI Logic)  
│   │   └── specialized\_agents.py \# The Workers (Data/API/Analytics)  
│   ├── api/  
│   │   └── qwen\_client.py       \# AI Connection Client  
│   ├── graph/  
│   │   └── healing\_graph.py     \# The Logic Manager  
│   └── utils/  
│       └── config.py            \# Configuration loader  
├── examples/               \# Tutorials and learning scripts  
├── real\_world/             \# Production-grade simulations  
└── tests/                  \# Verification tests

## **🤝 Contributing**

Contributions are welcome\! Please feel free to submit a Pull Request.

1. Fork the Project  
2. Create your Feature Branch (git checkout \-b feature/AmazingFeature)  
3. Commit your Changes (git commit \-m 'Add some AmazingFeature')  
4. Push to the Branch (git push origin feature/AmazingFeature)  
5. Open a Pull Request

## **📄 License**

This project is licensed under the MIT License.