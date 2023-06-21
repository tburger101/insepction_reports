# Home Inspection Report to CSV Converter
This Flask application allows you to convert a home inspection report in PDF format into a CSV file. The generated CSV file contains a list of all the home issues along with cost estimates.

## Prerequisites
* numpy
* pandas
* flask
* uuid
* os
* openai
* time
* PyPDF2
* tiktoken
* re
* scipy
* OpenAI API key

## Installation
1. Clone the repository to your local machine:
2. Install the required Python packages using pip: pip install -r requirements.txt
3. Set up your OpenAI API key:
   1. Visit the OpenAI website and create an account.
   2. Obtain an API key
   3. Set the environment variable OPENAI_API_KEY to your API key.

## Usage
1. Run the Flask application: app.py.run()
2. Access the application in your web browser at http://localhost:5000.
3. Click the "Choose File" button and select the home inspection report in PDF format.
4. Submit the form to initiate the conversion process
5. Once the conversion is complete, you will be redirected to the completion page.
6. On the completion page, click the "Download CSV" button to download the generated CSV file containing the home issues and cost estimates.

## Python Files
* core_chat.py- Sends responses to openAI.
* embedder.py - Used to break up the uploaded PDF into smaller text chunks to be analyzed.
* report.py - Leverages the core_chat and the embedder to create the CSV report.

## License
This project is licensed under the MIT License.

