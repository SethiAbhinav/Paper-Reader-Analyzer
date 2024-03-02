from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words
from typing import List
import streamlit as st
import pandas as pd
import requests
import nltk

nltk.download('stopwords')
nltk.download('punkt')

st. set_page_config(layout="wide")

class Paper:
    def __init__(self, paper_id: str):
        self.paper_id = paper_id
        self.data = None

    def fetch_data(self, fields: str = 'title,url,year,abstract,authors,venue,referenceCount,citationCount,influentialCitationCount,isOpenAccess,fieldsOfStudy,s2FieldsOfStudy,publicationTypes,publicationDate,journal,openAccessPdf'):
        response = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/{self.paper_id}?fields={fields}')
        self.data = response.json()

    def __getitem__(self, key: str):
        if self.data is None:
            raise KeyError(f'Data for paper {self.paper_id} has not been fetched yet. Call fetch_data() first.')
        return self.data[key]

    def summarize(self):
        if not self.data['abstract']:
            return 'No Summary Available as this paper is blocked via API calls. Please read it in full from the URL provided above.'
        parser = PlaintextParser.from_string(self.data['abstract'], Tokenizer('english'))
        summarizer = LsaSummarizer()
        summarizer.stop_words = get_stop_words('english')
        return ' '.join([str(sentence) for sentence in summarizer(parser.document, 3)])

    def get_authors_string(self):
        if 'authors' not in self.data:
            return ''
        authors = [author['name'] for author in self.data['authors']]
        return ', '.join(authors)
    
@st.cache_resource(ttl=600)  # cache results for 10 minutes
def search_papers(topic: str, num_papers: int) -> List[Paper]:
    try:
        response = requests.get(f'https://api.semanticscholar.org/graph/v1/paper/search?query={topic}&limit={num_papers}')

        response.raise_for_status()  # raise an exception if the request failed

        data = response.json()
        papers = [Paper(paper['paperId']) for paper in data['data']]

        for paper in papers:
            paper.fetch_data()
        return papers
    
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while searching for papers: {str(e)}")
        return []
    
def parse_data(data) -> List:
    if data is None:
        return ['Info Not Available']
    return data

def extract_paper_data_from_dict(data_dict: dict) -> dict:
    for k in data_dict.keys():
        data_dict[k] = parse_data(data_dict[k])
    return data_dict

def display_papers(papers: List[Paper]):
    cols = st.columns(3)
    for i, paper in enumerate(papers):
        col = cols[i % 3]
        with col:
            st.subheader(f'Paper {i+1}: {paper["title"]}')

            # Display the paper title and URL
            st.markdown(f'[{paper.data["title"]}]({paper.data["url"] if "url" in paper.data else "#"})')

            # Display the authors as a comma-separated string
            st.write(f'**Authors:** {paper.get_authors_string()}')

            # Display the summary with the text "Summary" in bold
            st.write(f'**Summary:** {paper.summarize()}')

            # Create an expander for additional paper information
            with st.expander(f'View additional information for Paper {i+1}'):
                paper_data = extract_paper_data_from_dict(paper.data)

                # Display a table with the paper data
                data = {
                    'Year': paper_data['year'],
                    'Venue': paper_data['venue'],
                    'Open Access PDF': paper_data['openAccessPdf'] if type(paper_data['openAccessPdf']) == list else paper_data['openAccessPdf'].get('url', ''),
                    'Reference Count': paper_data['referenceCount'],
                    'Citation Count': paper_data['citationCount'],
                    'Influential Citation Count': paper_data['influentialCitationCount'],
                    'Is Open Access': paper_data['isOpenAccess'],
                    'Fields of Study': ', '.join(paper_data['fieldsOfStudy']),
                    # 'S2 Fields of Study': ', '.join([field['category'] for field in paper_data.get('s2FieldsOfStudy', [])]), # Not interested in this
                    'Publication Types': ', '.join(paper_data['publicationTypes']),
                    'Publication Date': paper_data['publicationDate'],
                    'Journal': paper_data['journal'].get('name', '') + paper_data['journal'].get('volume', ''),
                }

                data_df = pd.DataFrame(data, index=[0])
                data_df_transposed = data_df.T
                data_df_transposed.index.name = 'Field'

                # print the transposed table
                st.dataframe(data_df_transposed, use_container_width = True, column_config = {"0":"Data"})


def app():
    st.title('Paper Reader & Analyzer')

    with st.sidebar:
        st.sidebar.header('Input Parameters')
        topic = st.text_input('Enter the topic', placeholder = 'chatgpt')
        num_papers = st.number_input('Enter the number of papers to analyze', min_value=1, max_value=10, value = 3)
        submit_button = st.button('Analyze Papers')
        topic = topic.strip().replace(' ', '+')

    if 'papers' not in st.session_state:
        st.session_state.papers = []

    if submit_button:
        # Show a loading spinner while the API request is being made
        with st.spinner('Searching papers...'):
            try:
                papers = search_papers(topic, num_papers)
                st.session_state.papers = papers
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while searching for papers: {str(e)}")
                st.stop()

    if st.session_state.papers:
        display_papers(st.session_state.papers)

        user_question = st.text_input('Enter your question')
        if st.button('Answer Question (this doesn\'t work rn but you can click it for fun)'):
            if user_question:
                # Here, you should implement a function to find the answer in the papers
                st.balloons()
                st.write('Answer to your question...')
            else:
                st.error('Please enter a question.')
                st.stop()



if __name__ == '__main__':
    app()
