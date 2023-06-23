import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.llms.openai import OpenAI
from langchain.chains.summarize import load_summarize_chain


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_file_from_data(file_path):
    data_folder = os.path.join(project_root, "data")
    full_path = os.path.join(data_folder, file_path)

    with open(full_path, "r") as file:
        content = file.read()

    return content


def save_file_to_output(file_path, content):
    output_folder = os.path.join(project_root, "output")
    full_path = os.path.join(output_folder, file_path)

    with open(full_path, "w", encoding="utf-8") as file:
        file.write(content)


def summarize_file(file_content, llm):
    # Split the source text
    text_splitter = CharacterTextSplitter()
    texts = text_splitter.split_text(file_content)

    # Create Document objects for the texts (max 3 pages)
    docs = [Document(page_content=t) for t in texts[:3]]

    # Load and run the summarize chain
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)

    return summary


if __name__ == "__main__":
    load_dotenv()  # Load the .env file
    openai_api_key = os.environ["OPENAI_API_KEY"]

    llm = OpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo-16k",
        openai_api_key=openai_api_key,
    )
    print(f"Using model: {llm.model_name} with api key: {llm.openai_api_key}")
    file_content = load_file_from_data("test_for_summary.txt")
    summarized_content = summarize_file(file_content, llm)
    save_file_to_output("summary_test_output.txt", summarized_content)
    print("Done.")
