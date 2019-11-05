from __future__ import absolute_import
from __future__ import division, unicode_literals
import logging
from flask import Flask, render_template, jsonify, request
import sys
import os

# Extrayendo información de pagina web
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Sumy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

LANGUAGE = "spanish"


#Sumy Plain Text
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer(LANGUAGE))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 6)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result
    try:
        sumy_summary(docx)
    except Exception:
        return jsonify("Error al aplicar analisis a texto")



# Obtener texto de vinculo
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text
    try:
        get_text(url)
    except Exception:
        return jsonify("Error al extraer texto desde la pagina web")

#------------Flask Application---------------#

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analisistexto', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        final_summary = sumy_summary(rawtext)
    return render_template('index.html', ctext=rawtext, final_summary=final_summary)
    try:
        analyzer = analyze()
        return Response(next(analyzer))
    except Exception:
        return jsonify("Error al realizar la sitesis de texto")


@app.route('/analisisurl', methods=['GET', 'POST'])
def analyze_url():
    if request.method == 'POST':
        raw_url = request.form['raw_url']
        rawtext = get_text(raw_url)
        final_summary = sumy_summary(rawtext)
    return render_template('index.html', ctext=raw_url, final_summary=final_summary)
    try:
        urlanalyzer = analyze_url()
        return Response(next(urlanalyzer))
    except Exception:
        return jsonify("Error al realizar la sitesis de la pagina WEB")


@app.route('/about')
def about():
    return render_template('index.html')

port = int(os.environ.get('PORT', 8080))

if __name__ == "__main__":
	app.run(host='0.0.0.0, port=port, debug=True)
