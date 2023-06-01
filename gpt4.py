from decouple import config
import openai
import pyperclip
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

OPENAI_API_KEY = config('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

console = Console()

def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=message_log,
        stop=None,
        temperature=0.7,
    )

    choices = response.choices # type: ignore

    for choice in choices:
        if "text" in choice:
            return choice.text

    return choices[0].message.content

def message_box(message, role):
    if role == "assistant":
        style = "green"
    else:
        style = "cyan"

    panel = Panel(message, style=style, title="", border_style=style)
    console.print(panel)


def main():
    message_log = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    first_request = True

    while True:
        if first_request:
            user_input = Prompt.ask(f"[bold yellow]Write or Copy your prompt and press enter[/bold yellow]")
            if user_input.lower().isspace() or user_input == "":
                user_input = pyperclip.paste()

            if user_input.lower().isspace():
                panel = Panel("Goodbye!", style="yellow", title="", border_style="yellow")
                console.print(panel)
                break

            message_log.append({"role": "user", "content": user_input})

            response = send_message(message_log)
            message_log.append({"role": "assistant", "content": response})

            message_box(f"User: {user_input}", "user")
            message_box(f"AI assistant: {response}", "assistant")
            pyperclip.copy(response)

            first_request = False
        else:
            user_input = Prompt.ask(f"[bold yellow]Write or Copy your prompt and press enter[/bold yellow]")
            if user_input.lower().isspace() or user_input == "":
                user_input = pyperclip.paste()

            if user_input.lower().isspace():
                panel = Panel("Goodbye!", style="yellow", title="", border_style="yellow")
                console.print(panel)
                break

            message_log.append({"role": "user", "content": user_input})

            response = send_message(message_log)

            message_log.append({"role": "assistant", "content": response})

            message_box(f"User: {user_input}", "user")
            message_box(f"AI assistant: {response}", "assistant")
            pyperclip.copy(response)

if __name__ == "__main__":
    main()
