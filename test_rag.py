# from query_data import query_database
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.prompts import ChatPromptTemplate

# EVAL_PROMPT = """
# Expected Response: {expected_response}
# Actual Response: {actual_response}
# ---
# (Answer with 'true' or 'false') Does the actual response match the expected response? 
# """


# def test_monopoly_rules():
#     assert query_and_validate(
#         question="How much is the escrow amount?",
#         expected_response="$1,000,000",
#     )


# def test_ticket_to_ride_rules():
#     assert query_and_validate(
#         question="Is any of the Sellers bound by a non-competition covenant after the Closing? ",
#         expected_response="No",
#     )


# def query_and_validate(question: str, expected_response: str):
#     response_text = main(question)
#     prompt = EVAL_PROMPT.format(
#         expected_response=expected_response, actual_response=response_text
#     )

#     model = ChatOpenAI()
#     evaluation_results_str = model.invoke(prompt)
#     evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

#     print(prompt)

#     if "true" in evaluation_results_str_cleaned:
#         # Print response in Green if it is correct.
#         print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
#         return True
#     elif "false" in evaluation_results_str_cleaned:
#         # Print response in Red if it is incorrect.
#         print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
#         return False
#     else:
#         raise ValueError(
#             f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
#         )

import subprocess
import json
from query_data import main
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import subprocess
from langchain_openai import ChatOpenAI

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response?
"""

def test_escrow_amount():
    assert query_and_validate(
        question="How much is the escrow amount?",
        expected_response="The escrow amount is not specified in the provided context.",
    )

def query_and_validate(question: str, expected_response: str):
    # Run the query_data.py script with the question
    process = subprocess.Popen(
        ["python3", "query_data.py", question],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    if stderr:
        raise RuntimeError(f"Error running query_data.py: {stderr.decode()}")

    response_text = stdout.decode()
    actual_response = extract_response_content(response_text)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=actual_response
    )

    model = ChatOpenAI()
    evaluation_results = model.invoke(prompt)
    evaluation_results_str = evaluation_results.content.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str:
        print("\033[92m" + f"Response: {evaluation_results_str}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str:
        print("\033[91m" + f"Response: {evaluation_results_str}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )

def extract_response_content(response_text: str) -> str:
    """Extract the actual response content from the response_text obtained from query_data.py."""
    prefix = "Response: "
    start_index = response_text.find(prefix)
    if (start_index == -1):
        raise ValueError("Response content not found in the response text.")

    start_index += len(prefix)
    end_index = response_text.find("\nSources:", start_index)
    if (end_index == -1):
        raise ValueError("Sources not found in the response text after response content.")

    return response_text[start_index:end_index].strip()

# To run the tests directly from the script
if __name__ == "__main__":
    test_escrow_amount()