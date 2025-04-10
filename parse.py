from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Template remains the same
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** From the DOM content, extract the actual descriptive text (not just section titles) that matches: {parse_description}.\n"
    "2. **No Extra Content:** Do not include additional commentary.\n"
    "3. **Empty Response:** If no matching content is found, return ''.\n"
    "4. **Only Output Matching Text.**"
)

model = OllamaLLM(model="gemma2")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Skip empty or useless chunks
        if not chunk.strip() or chunk.strip().lower().startswith("world health organization world health organization"):
            print(f"Skipped batch {i} due to repetitive or empty content.")
            continue

        # Optional: truncate overly long or short chunks to improve accuracy
        if len(chunk.strip()) < 50:
            print(f"Skipped batch {i} due to too little content.")
            continue

        response = chain.invoke({
            "dom_content": chunk,
            "parse_description": parse_description
        })

        print(f"Parsed batch {i} of {len(dom_chunks)}")

        # Avoid duplicate lines like "World Health Organization..." repeated
        if response and response.strip() and response.strip() not in parsed_results:
            parsed_results.append(response.strip())

    # Final deduplicated and cleaned-up result
    final_output = "\n".join(parsed_results).strip()
    return final_output
