from setuptools import find_packages, setup  # pyright: ignore[reportMissingModuleSource]

setup(
    name="medical-chatbot",
    version="0.1.0",
    description="Medical chatbot project",
    author="ADITHYA UBALE",
    author_email="adithyaubale2006@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy>=2.0.0",
        "sentence-transformers",
        "flask",
        "pypdf",
        "python-dotenv",
        "pinecone",
        "langchain-community",
        "langchain-huggingface",
        "langchain-text-splitters",
        "langchain-core",
        "langchain-nvidia-ai-endpoints",
        "langchain-experimental",
    ],
)