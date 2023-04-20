from flask import Flask, render_template, request, send_file
from scripts import transformations
import os

app = Flask(__name__)
app.secret_key = '20112020DontBeHasty06012022'

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		file = request.files['file']
		option = request.form['option']

		if option == 'SUP':
			json_file = transformations.convert_sup(file)
			response = send_file(json_file, as_attachment=True, mimetype='application/json', download_name='SUP-metadata.json')
			
			os.unlink(json_file)

			return response

		else:
			return None


	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)