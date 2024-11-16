import os
from langchain_community.llms import Ollama
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from operator import itemgetter
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser




MODEL = 'llama3'


loader = PyPDFLoader('mlschool.pdf')
pages = loader.load_and_split()

embeddings = OllamaEmbeddings()
vectorstore = DocArrayInMemorySearch.from_documents(pages, embedding=embeddings)

retrivier = vectorstore.as_retriever()



template = '''
Answer the question based on the context below, dont mention the context in the answer. If you can't
answer the question, reply 'I don't know'.

context: {context}

Question: {question}
'''

prompt = PromptTemplate.from_template(template=template)
# print(prompt.format(context = 'Here is some context', question='Here is a question'))

model = Ollama(model = MODEL)


parser = StrOutputParser()


chain = (
    {
        'context' : itemgetter("question") | retrivier, 
        'question':itemgetter("question")
    }
    | prompt 
    | model 
    | parser
)

print(chain.invoke({'question': "What is the purpose of the course?"}))


