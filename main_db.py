# Gerekli kütüphanelerin içe aktarılması
import os.path  # Dosya yolu işlemleri için
import pickle  # Python nesne yapılarını serileştirmek ve seri durumdan çıkarmak için

import streamlit as st  # Web uygulamaları oluşturmak için Streamlit kütüphanesi

from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma

from langchain.text_splitter import RecursiveCharacterTextSplitter  # Metni parçalara ayırmak için
from langchain.embeddings.openai import OpenAIEmbeddings  # OpenAI modellerini kullanarak gömülüler oluşturmak için

from langchain.llms import OpenAI  # OpenAI'nin dil modelleriyle etkileşim için
from langchain.chains import RetrievalQAWithSourcesChain  # Kaynak tabanlı soru cevaplama için

from langchain.chains.question_answering import load_qa_chain  # Soru cevaplama zincirini yüklemek için fonksiyon
from langchain.callbacks import get_openai_callback  # OpenAI'nin API'sinden gelen geri çağırmaları işlemek için

# pip install langchain openai --upgrade

#  Projede "Prompt Template" koyarsak spesifik konu alalarda daha insicamlı cevaplar üretebiliriz 

api = ''  # Open AI, API anahtarı buraya eklenmeli

def main():

    st.header('Vodafone AI driven chatbot System')  # Uygulamanın başlığını göster
    pdff = st.file_uploader('upload your file', type=['pdf'])  # PDF dosyaları için bir dosya yükleme widget'ı oluştur

    if pdff is not None:  # Bir PDF dosyası yüklendiğinde
        directory = "./"+pdff.name[:-4]
        if os.path.exists(pdff.name[:-4]):
            vectordb= Chroma
        else:
            loaders = PyPDFLoader(pdff.name) # Bir PDF okuyucu nesnesi oluştur

            doc = loaders.load()

            # Çıkarılan metni işlemek için parçalara ayır
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,  # Her bir metin parçasının boyutu
                chunk_overlap=200,  # Parçalar arasındaki bağlamı korumak için örtüşme
            )

            chunks = text_splitter.split_documents(doc)  # Metni parçalara ayır

            embedding = OpenAIEmbeddings(openai_api_key=api)  # OpenAI'nin API'si kullanarak bir gömülü nesnesi oluştur 

            vectordb = Chroma.from_documents(documents=chunks, 
                                            embedding=embedding,
                                            persist_directory= directory)

        query = st.text_input('What is Your Question From this pdf')  # Kullanıcının sorusu için bir metin girişi widget'ı oluştur

        if query:  # Kullanıcı bir soru girdiğinde

            # docs = vectordb.similarity_search(query, k=4)

            docs = vectordb.max_marginal_relevance_search(query, k = 4)

            llm = OpenAI(openai_api_key=api)  # OpenAI'nin API'si kullanarak bir dil modeli nesnesi oluştur
            
            chain = load_qa_chain(llm=llm, chain_type='stuff')  # Bir soru cevaplama zinciri yükle

            with get_openai_callback() as cb:  # OpenAI geri çağrısı kullan
                response = chain.run(input_documents=docs, question=query)  # Soru cevaplama zincirini çalıştır
                print(cb)

            st.markdown(response)  # Uygulamada yanıtı göster

            vectordb.persist()

if __name__ == '__main__':
    main()  # Bu betik ana modül olarak çalıştırıldığında ana fonksiyonu çalıştır
