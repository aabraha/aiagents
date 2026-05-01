from dotenv import load_dotenv
from openai import OpenAI
import json
import os
from pathlib import Path
import requests
from pypdf import PdfReader
import gradio as gr


BASE_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = BASE_DIR / "resources"

load_dotenv(override=True)


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        },
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}


# create a tool for recording user details
record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user",
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it",
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

# create a tool for recording unknown questions from users
record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered by an agent at current version",
            },
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}
# crate a list of dictionary of tools
tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]


class Career:
    def __init__(self):
        self.openai = OpenAI()  # create an openai client instance
        self.name = "Assefa Abraha"
        # read linkedin profile
        linkedin_reader = PdfReader(RESOURCES_DIR / "my-linkedin-profile.pdf")
        linkedin = ""
        for page in linkedin_reader.pages:
            text = page.extract_text()
            if text:
                linkedin += text
        self.linkedin = linkedin
        # read resume content
        resume_reader = PdfReader(RESOURCES_DIR / "Abraha_Assefa_resume.pdf")
        resume = ""
        for page in resume_reader.pages:
            text = page.extract_text()
            if text:
                resume += text
        self.resume = resume
        # read behavioral content
        behavioral_reader = PdfReader(RESOURCES_DIR / "behavioral.pdf")
        behavioral = ""
        for page in behavioral_reader.pages:
            text = page.extract_text()
            if text:
                behavioral += text
        # read secong behavioral content
        behavioral_reader = PdfReader(RESOURCES_DIR / "behv2.pdf")
        for page in behavioral_reader.pages:
            text = page.extract_text()
            if text:
                behavioral += text
        self.behavioral = behavioral
        # read summary file
        with open(RESOURCES_DIR / "summary.txt", "r", encoding="utf-8") as file:
            self.summary = file.read()

    # This is an elegant way that avoids IF statement with reflection call using the globals()
    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append(
                {
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id,
                }
            )
        return results

    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += (
            f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        )
        system_prompt += (
            f"\n\n## Resume:\n{self.resume}\n\n## Behavioral Questions:\n{self.behavioral}\n\n"
        )
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [
            {"role": "user", "content": message}
        ]
        done = False
        while not done:
            # This is the call to the LLM - see that we pass in the tools json
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini", messages=messages, tools=tools
            )
            # If the LLM wants to call a tool, we do that!
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


if __name__ == "__main__":
    career = Career()
    gr.ChatInterface(career.chat,  title="Assefa Abraha's Career Assistant").launch()#type="messages" is deprecated
