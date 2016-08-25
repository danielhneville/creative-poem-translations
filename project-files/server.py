from flask import Flask, request, redirect, render_template, session, flash
import requests
import re
from auth import auth

key = auth()

app = Flask(__name__)
app.secret_key = 'pablonerudawaspoisoned'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/translate/process', methods=['POST'])
def translate_process():
	session['data'] = {}
	if request.form['poem'] != '':
		session['data']['fullpoem'] = request.form['poem']
	else:
		flash('You need to copy/paste a poem in here to translate it!')
		return redirect('/')
	if request.form['title'] != '':
		session['data']['title'] = request.form['title']
		session['data']['titlewords'] = re.findall(r"\w+|[^\w\s]", session['data']['title'], re.UNICODE)
	else:
		session['data']['title'] = ''
	session['data']['lines'] = session['data']['fullpoem'].split('\n')
	session['data']['wordlists'] = []
	for line in session['data']['lines']:
		session['data']['wordlists'].append(re.findall(r"\w+|[^\w\s]", line, re.UNICODE))
	return redirect('/translate')

@app.route('/translate')
def translate():
	return render_template('translate.html', poem=session['data'], length=len(session['data']['wordlists']))

@app.route('/api_call', methods=['POST'])
def api_call():
	word = request.form['word']
	url = 'https://api.collinsdictionary.com/api/v1/dictionaries/spanish-english/search/first/?q=' + word + '&format=html'
	headers = {
		'Host': '127.0.0.1:5000',
		'Accept': 'application/json',
		'accessKey': key.accessKey
	}
	response = requests.get(url, headers=headers).content
	return response

@app.route('/view/process', methods=['POST'])
def view_process():
	session['user_poem'] = request.form
	return redirect('/view')

@app.route('/view')
def view():
	utitle = session['user_poem']['title']
	ulines = []
	for idx in range(len(session['user_poem'])-1):
		ulines.append(session['user_poem'][str(idx)])
	title = session['data']['title']
	lines = session['data']['lines']
	return render_template('view.html', utitle=utitle, ulines=ulines, title=title, lines=lines)

@app.route('/startover', methods=['POST'])
def startover():
	if 'user_poem' in session:
		session.pop('user_poem', None)
	if 'data' in session:
		session.pop('data', None)
	return redirect('/')

if __name__ =="__main__":
	app.run(host='0.0.0.0')
