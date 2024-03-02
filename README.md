# Paper-Reader-Analyzer

The Paper-Reader-Analyzer is a web-based application that allows users to quickly find and analyze research papers on topics of interest. The app uses the Semantic Scholar API to search for papers and extract relevant information such as title, authors, abstract, publication venue, and citation count. The app also provides a summary of the paper and an option to view additional information such as fields of study, publication types, and open access PDFs. [Try it out here](https://analyzepaper.streamlit.app/)

## Features

* Search for research papers on a specific topic.
* View paper title, authors, abstract, and summary.
* View additional paper information such as fields of study, publication types, and other metadata.
* Ask and answer questions related to the papers. (TODO)

## Getting Started

### Prerequisites

* Python 3.6 or higher
* Python Libraries:
```Python
requests: to make API calls
sumy: for NLP
nltk: to download stop words
streamlit: for deployment of web-app
```


### Installation

1. Clone the repository to your local machine
```bash
git clone https://github.com/your-username/Paper-Reader-Analyzer.git
```
2. Install the required libraries using pip
```bash
pip install streamlit requests sumy nltk pandas
```
3. Run the app using Streamlit
```bash
streamlit run app.py
```

## Usage

1. Enter a topic of interest in the search bar
2. Select the number of papers to analyze
3. Click the "Analyze Papers" button
4. Browse through the list of papers and view their summaries
5. Click the "View additional information" expander to view more details about the paper
6. Enter a question related to the papers and click the "Answer Question" button

## Built With

* [Streamlit](https://streamlit.io/) - The web framework used
* [Semantic Scholar API](https://api.semanticscholar.org/) - The API used to search for research papers
* [Sumy](https://github.com/miso-belica/sumy) - The library used to generate paper summaries
* [NLTK](https://www.nltk.org/) - The library used for natural language processing tasks
* [Pandas](https://pandas.pydata.org/) - The library used for data manipulation and analysis

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments

* Inspiration for this project came from the need to quickly find and analyze research papers for academic purposes.
* The Semantic Scholar API provided a convenient way to search for and extract information from research papers.
* The Sumy library provided a simple and effective way to generate paper summaries.
* The Streamlit library made it easy to create a user-friendly web interface for the app.

## Disclaimer

This is a prototype and is not intended for production use. The accuracy of the paper summaries and answers to questions cannot be guaranteed. Use at your own risk.
