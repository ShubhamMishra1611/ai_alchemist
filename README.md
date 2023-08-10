# ai_alchemist

Work in progress.

This repository contains a Python script that utilizes the **Palm** and **Aspose.Words** libraries for text generation and document processing. The script analyzes a candidate's resume for the position of given job description, performs skill matching, and conducts a question-answering session to evaluate the candidate's suitability for the job.

## Dependencies

List of all libraries and dependencies used in this project:
**Palm** -
**Aspose.Words** -
**PyPDF2** -
**docx2txt** -
**pyttsx3** -


## Usage

1. Install the required libraries and dependencies mentioned above.
2. Create a `config.json` file with the following structure:
   ```json
   {
       "user_name": "YOUR_USERNAME",
       "API": "YOUR_PALM_API_KEY"
   }

    ```
3. Run the `main.py` script.
4. Enter the job description and the candidate's resume file path when prompted.
