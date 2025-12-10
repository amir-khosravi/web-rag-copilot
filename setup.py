from setuptools import setup, find_packages

def read_requirements():
    with open("requirements.txt") as f:
        return f.read().splitlines()

setup(
    name="enterprise_rag_copilot",
    version="1.0.0",
    author="Engineering Team",
    description="Enterprise-grade RAG Copilot with Jenkins/AWS MLOps pipeline",
    packages=find_packages(),
    install_requires=read_requirements(),
    python_requires=">=3.10",
)