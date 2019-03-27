from __future__ import absolute_import
from __future__ import division, unicode_literals
from flask import Flask, render_template, url_for, request

import sys

# Extrayendo información de pagina web
from bs4 import BeautifulSoup
from urllib.request import urlopen
#from text_summarizer import FrequencySummarizer

# Sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

LANGUAGE = "spanish"


#Sumy Plain Text
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer(LANGUAGE))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

# Obtener texto de vinculo
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text


#------------Flask Application---------------#

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analisistexto', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_summary = sumy_summary(rawtext)
    return render_template('index.html', ctext=rawtext, final_summary=final_summary)


@app.route('/analisisurl', methods=['GET', 'POST'])
def analyze_url():
    if request.method == 'POST':
        raw_url = request.form['raw_url']
        rawtext = get_text(raw_url)
        final_summary = sumy_summary(rawtext)
    return render_template('index.html', ctext=raw_url, final_summary=final_summary)


@app.route('/about')
def about():
    return render_template('index.html')


if __name__ == "__main__":
	app.debug = True
	app.run()