from langchain_community.document_loaders import WebBaseLoader

url = "https://es.wikipedia.org/wiki/Granollers"

loader = WebBaseLoader(url)
documents = loader.load()

print(documents)