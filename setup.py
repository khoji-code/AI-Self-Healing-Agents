
from setuptools import setup, find_packages

setup(
    name="self-healing-agents",
    version="1.0.0",
    author="Abolfazl Khojasteh",
    author_email="khoji2001social@gmail.com",
    description="Self-healing multi-agent system with free Qwen AI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "langgraph>=0.0.32",
        "langchain>=0.1.0",
        "huggingface-hub>=0.20.0",
        "httpx>=0.24.0",
        "python-dotenv>=1.0.0",
    ],
)