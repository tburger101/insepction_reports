import time
import json
import pandas as pd
import embedder
import core_chat as cc
import multiprocessing


def read_file_contents(file_name):
    with open(file_name, encoding='utf-8') as file:
        contents = file.read()
    return contents


def get_content_instruction():
    content_message = "You use the section of each home report to give a JSON response back with the appropriate " \
                      "details. "
    instruction_response = "Analyze the text and return details back in a JSON format like the above examples."
    return content_message, instruction_response


def find_home_repairs(chunk_text, examples, content, instruction, gpt_model, api_key):
    pool = multiprocessing.Pool()  # Create a pool of worker processes
    num_processes = multiprocessing.cpu_count()  # Get the number of available CPU cores
    chunk_size = max(len(chunk_text) // num_processes, 1)  # Calculate the chunk size for each process

    # Split the chunk_text into smaller chunks for parallel processing
    chunks = [chunk_text[i:i + chunk_size] for i in range(0, len(chunk_text), chunk_size)]

    # Process each chunk in parallel using the worker pool
    results = pool.starmap(repair_details,
                           [(chunk, examples, content, instruction, gpt_model, api_key) for chunk in chunks])

    # Merge the results from all the processes
    data_list = [item for sublist in results for item in sublist]
    repair_df = pd.DataFrame(data_list, columns=['text', 'cost_details'])

    return repair_df


def repair_details(chunk_text, examples, content, instruction, gpt_model, api_key):
    data_list = []
    for analyze_content in chunk_text:
        gpt_message = examples + "\n" + analyze_content + "\n" + instruction
        answer = cc.ask_chat(api_key, gpt_message, content, 0, gpt_model)
        data_list.append([analyze_content, answer])
        time.sleep(1)

    return data_list


def string_to_json(input_string):
    # Remove newlines and spaces from input string
    input_string = input_string.replace('\n', '').replace(' ', '')

    output = "[" + input_string + "]"
    # Return the JSON object
    return json.loads(output)


def format_inspection(df):
    repairs = []
    for index, row in df.iterrows():
        cost_details = row['cost_details']

        try:
            cost_json = json.loads(cost_details)
        except:
            try:
                cost_json = string_to_json(cost_details)
            except:
                print(index)
                continue
        if isinstance(cost_json, list):
            for x in cost_json:
                repairs.append(x)
        else:
            repairs.append(cost_json)

    repair_df = pd.DataFrame(repairs)
    repair_df.drop_duplicates(inplace=True)
    return repair_df[~repair_df.apply(lambda row: row.str.contains('informational')).any(axis=1)]


def create_home_report(key, model, pdf_link):
    prompt_examples = read_file_contents("static/prompt_intro.txt")
    content_message, instruction_response = get_content_instruction()

    emd = embedder.PDFEmbeddings(pdf_path=pdf_link, openai_key=key,
                                 max_tokens=1600)

    text_chunks = emd.create_text_chunks()
    json_repairs_df = find_home_repairs(text_chunks, prompt_examples, content_message, instruction_response, model, key)
    inspection_report = format_inspection(json_repairs_df)
    return inspection_report
