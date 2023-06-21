from flask import Flask, render_template, request, make_response
import report
import pandas as pd
from uuid import uuid4
import os

app = Flask(__name__, static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        pdf_file = request.files['file']

        # Create the "inspection_reports" folder if it doesn't exist
        upload_folder = os.path.join(app.root_path, 'inspection_reports')
        os.makedirs(upload_folder, exist_ok=True)
        unique_id = uuid4().hex

        # Generate a unique filename
        pdf_file_name = os.path.join(upload_folder, f"{unique_id}_uploaded_file.pdf")

        pdf_file.save(pdf_file_name)

        key = os.environ.get('OPENAI_API_KEY')
        model = 'gpt-3.5-turbo'

        home_report = report.create_home_report(key, model, pdf_file_name)

        # Save the home report as a CSV file
        csv_file_name = f"{unique_id}_home_report.csv"
        csv_file_path = os.path.join(upload_folder, csv_file_name)
        home_report.to_csv(csv_file_path, index=False)

        return render_template('completed.html', csv_file=csv_file_path)
    else:
        return render_template('upload.html')


@app.route('/completed', methods=['GET'])
def completed():
    # Retrieve the csv_file path from the query parameters
    csv_file_path = request.args.get('csv_file')

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Convert the CSV file to a response object
    response = make_response(df.to_csv(index=False))

    # Set the appropriate headers for CSV download
    response.headers['Content-Disposition'] = 'attachment; filename=home_repair.csv'
    response.headers['Content-Type'] = 'text/csv'

    return response


if __name__ == '__main__':
    app.run()
