import json
from difflib import get_close_matches

# takes json filepath as parameter
# returns a dictionary with the knowledge base data
def load_knowledge_base(file_path: str):
    with open(file_path, 'r') as file:
        data_dict: dict = json.load(file)
    return data_dict

# takes json filepath and data as dictionary as parameters
# dumps the dictionary, data, into the json file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# takes the user's question and returns the best answer from the knoweldge base if it exists
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    # finds the single closest match that is 60% accurate based on the user's question and the knowledge base
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    else:
        return None
    
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions list"]:
        if q["question"] == question:
            return q["answer"]
    
    return None

# chatbot function allows the user to ask the chatbot questions and teach it responses to questions
def chat_bot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "quit":
            break

        # finds the best match for the user's question in knowledge base
        # second parameter creates a list of all values for the keys "question" in the list of dictionaries, knowledge_base["questions"]
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions list"]])

        if best_match:
            answer = get_answer_for_question(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer to that question. Can you teach me? ")
            new_answer = input("Type the answer or \"skip\" to skip: ")

            if new_answer != "skip":
                knowledge_base["questions list"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Bot: Thank you! I learned a new response!")

if __name__ == '__main__':
    chat_bot()
            
