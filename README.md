# hopkins-policy-hack-2024


## Setup
1. `pip3 -m venv .env`
1. `source .env/bin/activate` 
1. `pip3 install -r requirements.txt` 
1. `./data.sh` -- this sets up the database with a few example values
1. `flask run --debug`
1. visit localhost:5000


You will need to have [ollama](https://ollama.com/) installed for llm completion to work properly.

You may need to run `ollama pull llama3.2:1b-text-q5_K_M` to get the appropriate model.