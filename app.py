from flask import Flask, render_template, request
import google.generativeai as genai
import requests

# Replace with your actual API key
genai.configure(api_key="AIzaSyAQ0Ri8QJAtFaUNRUUWwaFBkxZXkaolQiI")

# Choose a Gemini model
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

app = Flask(__name__)

# Your SQL dataset API URL
SQL_API_URL = "https://retoolapi.dev/w78zY6/data"

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""

    if request.method == "POST":
        user_input = request.form.get("prompt", "")

        if user_input:
            try:
                # Fetch data from SQL API
                sql_data = requests.get(SQL_API_URL).json()

                # Send dataset + user question to Gemini
                prompt = f"""
                You are an AI assistant analyzing a dataset.

                Dataset:
                {sql_data}

                User Question:
                {user_input}

                Answer based on the dataset.
                """

                response = model.generate_content(prompt)
                response_text = response.text

            except Exception as e:
                response_text = f"Error: {str(e)}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
