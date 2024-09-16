import os

from flask import (Flask, redirect, render_template, jsonify, request,
                   send_from_directory, url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

# Sample data
companies = [
    {"id": 1, "name": "Company One", "summary": "Summary of Company One"},
    {"id": 2, "name": "Company Two", "summary": "Summary of Company Two"}
]

# Companies endpoint
@app.route('/companies', methods=['GET'])
def get_companies():
    return jsonify(companies)

# Companies/all endpoint
@app.route('/companies/all', methods=['GET'])
def get_all_companies():
    return jsonify(companies)

# Companies/[id] endpoint
@app.route('/companies/<int:id>', methods=['GET'])
def get_company(id):
    company = next((comp for comp in companies if comp["id"] == id), None)
    if company:
        return jsonify(company)
    return jsonify({"error": "Company not found"}), 404

# Companies/[id]/summary endpoint
@app.route('/companies/<int:id>/summary', methods=['GET'])
def get_company_summary(id):
    company = next((comp for comp in companies if comp["id"] == id), None)
    if company:
        return jsonify({"id": company["id"], "summary": company["summary"]})
    return jsonify({"error": "Company not found"}), 404


if __name__ == '__main__':
   app.run()
