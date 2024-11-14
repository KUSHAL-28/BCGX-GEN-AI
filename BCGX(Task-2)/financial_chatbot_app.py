from flask import Flask, render_template, request, jsonify
import pandas as pd

# Load data from CSV
df = pd.read_csv("C:/Users/kusha/OneDrive/Desktop/BCGX(Task-2)/Final_Data.csv")
data = {}

# Process the data for each company and year
for company in df['Company'].unique():
    data[company] = {}
    company_data = df[df['Company'] == company]
    for year in company_data['Year'].unique():
        year_data = company_data[company_data['Year'] == year].iloc[0]
        data[company][year] = year_data.drop(['Company', 'Year']).to_dict()

app = Flask(__name__)

# Define the chatbot function
def financial_chatbot(company, year, metric):
    if company in data and year in data[company]:
        company_year_data = data[company][year]
        metric_value = company_year_data.get(metric)

        if metric_value is not None:
            return f"The {metric} for {company} in {year} is: {metric_value}"
        else:
            return f"Sorry, we don’t have data for '{metric}' for {company} in {year}."
    else:
        return f"Sorry, we don’t have data for {company} in {year}."

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling chatbot queries
@app.route('/query', methods=['POST'])
def query():
    data = request.json
    company = data.get('company')
    year = int(data.get('year'))
    metric = data.get('metric')
    response = financial_chatbot(company, year, metric)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
