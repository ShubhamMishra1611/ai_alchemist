import re
import json
import time
import pprint
import aspose.words as aw
import google.generativeai as palm
from datetime import datetime
from helper.colors import bcolors
from helper.interpret_markup import MarkupInterpreter
from pdf2txt import PDFProcessor



with open("config.json", "r") as f:
    file = json.load(f)
    name = file["user_name"]
    API = file["API"]


def login():
    print("Initiating model...")
    palm.configure(api_key=API)
    models = [m for m in palm.list_models(
    ) if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    print(model)
    return model

def get_combined(prompt, model, get_content=False):
    try:
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            max_output_tokens=800,
        )
        response = interpret_markup(completion.result)
        print(response)  # Always print the response if get_content is False
        if get_content:
            return response
        else:
            print(response)
            return 1
    except:
        if get_content:
            return False
        animated_print("Looks like I am not good enough to understand it 😔, try something else")
        return 0



def get(prompt, model):
    try:
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
        )
        response = interpret_markup(completion.result)
        print(response)
        # animated_print(response)
        return 1
    except:
        animated_print(
            "Looks like I am not good enough to understand it 😔, try something else")
        return 0


def get_content(prompt, model):
    try:
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            # The maximum length of the response
            max_output_tokens=800,
        )
        response = interpret_markup(completion.result)
        return response
    except:
        return False


def interpret_markup(text):

    # Interpret **text** markup
    text = re.sub(r'\*\*(.*?)\*\*', r'\033[1m\1\033[0m', text)

    # Interpret *text* markup
    text = re.sub(r'\*(.*?)\*', r'\n• \1', text)

    # Interpret `text` markup
    text = re.sub(r'`(.*?)`', r'\033[4m\1\033[0m', text)

    return text


def animated_print(text, animation=True):
    print(f"{bcolors.OKGREEN}Palm>>>", end='')
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print("\n")


def main():
    model = None
    if model is None:
        model = login()
        get(f" Greet the user with a friendly tone. Username is {name}.", model)
    exit_status = False
    while not exit_status:
        user_prompt = "start"#input(f"{bcolors.OKCYAN}User type>>>")
        if user_prompt == "exit":
            exit_status = True
            get("Say bye to user in enjoying and friendly tone depicting how much you enjoy helping user", model)
            continue
        if user_prompt == "start":
            file_name = "resume.txt"#input("Please provide us the resume path: ")
            
            if file_name.split('.')[-1] == 'pdf': # if the extension of file is pdf then convert it to text
                pdf_processor = PDFProcessor(file_name)
                num_pages = pdf_processor.get_num_pages()
                page_number = 0
                page_text = pdf_processor.get_text_from_page(page_number)
                if page_text!= 0:
                    # save it to resume.txt
                    with open("resume.txt", 'w', encoding="utf-8") as f:
                        f.write(page_text)
                    file_name = "resume.txt"
            # if file is a docx file then convert it to text
            elif file_name.split('.')[-1] == 'docx':
                doc = aw.Document(file_name)
                doc.save("resume.txt", aw.SaveFormat.TEXT)
                # remove the last line from the file
                with open("resume.txt", 'r') as f:
                    lines = f.readlines()
                    lines = lines[:-1]
                with open("resume.txt", 'w') as f:
                    f.writelines(lines)
                file_name = "resume.txt"
            with open(file_name, 'r') as f:
                content = f.read()
                content = re.sub(r'[^\x00-\x7F]+', ' ', content)

            # print(
            #     f"Imagine you are a hiring manager in a company. A candidate has submitted a resume for the position of Machine Learning Engineer. Your task is to thoroughly and deeply analyze the resume and provide an evaluation of whether the candidate deserves the given position or not. Also assign a score out of 10 to the candidate based on your assessment for the job. Here is the candidate's resume: {content}", model)
            get(
                f"Imagine you are a hiring manager in a company. A candidate has submitted a resume for the position of Machine Learning Engineer. Your task is to thoroughly and deeply analyze the resume and provide an evaluation of whether the candidate deserves the given position or not. Also assign a score out of 10 to the candidate based on your assessment for the job. Here is the candidate's resume: {content}", model)
            print("*"*100)
            print("------------- The stuff related to reading resume is done-------------")
            print("*"*100)
            projects = get_content(
                f" Here is the resume of a candidate. Analyse the resume deeply and list out all the projects that he has mention in his/ her resume. This is resume : {content}", model)
            with open("project.txt", 'w') as f:
                f.write(projects)
            print("*"*100)
            print("-------------The stuff related to projects is done-------------")

            print("*"*100)
            # get all the skills related to the job description
            job_description = "Machine learning engineer"
            skills = get_content(
                "Here is the job description of the job. Analyse the job description deeply and list out all the skills that are required for the job. Here is the job description: " + job_description, model)
            # save the skills in text file name skills.txt
            with open("skills.txt", 'w') as f:
                f.write(skills)
            # look at skills that candidate has mention in his/her resume
            candidate_skills = get_content(
                "Here is the resume of the candidate. Analyse the resume deeply and list out all the skills that he/she has mention in his/her resume. Here is the resume: " + content, model)
            # save the skills in text file name candidate_skills.txt
            with open("candidate_skills.txt", 'w') as f:
                f.write(candidate_skills)
            # compare the skills of the candidate with the skills required for the job 
            get("Here is the list of skills that are required for the job: " + skills + "Here is the list of skills that the candidate has mention in his/her resume: " + candidate_skills + "Compare the skills of the candidate with the skills required for the job and tell me the score out of 10", model)
            print("-------------The stuff related to skills is done-------------")
            # question answering part
            # So here LLM will analyse the projects and skills of the candidate and will ask questions related to the projects and skills. All the questions will be asked from the candidate and the answers will be saved in a text file name answers.txt along with the questions.
            # later this question_answer.txt file will be used to analyse the candidate.

            questions = get_content(
                "Here is the list of projects that the candidate has done.Deeply look at the projects. Ask him/her tough quality only questions related to the project to analyse him/ her.Do not provide any answer. Only questions. Here is the list of projects: " + projects, model)
            # save the questions in text file name questions.txt
            with open("questions.txt", 'w') as f:
                f.write(questions)
            scores = []
            with open("questions.txt", 'r') as f:
                questions = f.read()
            for question in questions.split('\n'):
                # check if question ends with ?
                if question:
                        
                    if question[-1] == '?':
                        answer = input(question)
                        with open("answers.txt", 'a') as f:
                            f.write(answer)
                        # score = get(
                        #     f"Here is the answer of the candidate for the question: {question}. The candidate has given answer: {answer}. Analyse the answer deeply and provide score out of 10 in the following format.[FEEDBACK: EXCELLENT, GOOD, BAD, WORST] [Score: x/10]", model)
                        score = get(
                            f"Here is the answer of the candidate for the question: {question}. The candidate has given answer: {answer}. Analyse the answer deeply. If the answer is not sufficient, ask another question what exaclty the candidate misses to introduce in the answer. If the answer is detailed and statisfies the question, give a score of higher than 8. If the given answer is quite general and obvious, give a score of 5. provide score out of 10 in the following format.[FEEDBACK: EXCELLENT, GOOD, BAD, WORST] [Score: x/10]", model)
                        scores.append(score)
            # get the overall score of the candidate
            overall_score = sum(scores)/len(scores)
            print(
                f"Here is the overall score of the candidate: {overall_score}")

        else:
            get(user_prompt, model)


if __name__ == '__main__':
    main()