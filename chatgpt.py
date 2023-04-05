#! /usr/bin/python3
import os
import sys
import platform
import signal

try:
    import openai
except ImportError:
    print("please install openai")
    print("pip3 install openai")
    exit(0)


def print_prompt(prompt=">"):
    print(prompt, end=" ", flush=True)


class Command:
    def __init__(self) -> None:
        self.interactive = False
        self.content = None
        self.first = True
        self.setup()

    def setup(self):
        if sys.stdin.isatty():
            data_pipe = None
        else:
            # 管道模式
            data_pipe = sys.stdin.read()
            reset_stdin()

        self.interactive = "-i" in sys.argv
        args = sys.argv[1:]
        if self.interactive:
            args.remove("-i")

        self.content = data_pipe + "\n" + "".join(args) if data_pipe else "".join(args)
        # print(f"self.content <{repr(self.content)}>")

    def get_content(self):
        if self.first and self.content:
            self.first = False
            print(f"\nQuestion: {self.content}")
            return self.content

        print_prompt()
        content = sys.stdin.read()
        print(f"\nQuestion: {content}")
        return content


class chatGPT:
    def __init__(self) -> None:
        # https://platform.openai.com/account/api-keys
        self.openai_api_key = "sk-xxxxxxxxxx"
        self.setup()
        self.cmd = Command()
        # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
        self.messages = [
                 {"role": "system", "content": "You are a friendly and helpful teaching assistant. You explain concepts in great depth using simple terms, and you give examples to help people learn."},
                ]

    def setup(self):
        # openai.organization = "org-"
        openai.api_key = self.openai_api_key

    def run(self):
        if self.cmd.interactive:
            self.openai_interaction()
        else:
            self.openai_ask()

    def openai_ask(self):
        content = self.cmd.get_content()
        self.messages_add(content=content)
        self.call_openai()

    def openai_interaction(self):
        while True:
            self.openai_ask()

    def call_openai(self):
        # return self.mock()

        # https://platform.openai.com/docs/models/overview
        model = "gpt-3.5-turbo"

        # https://platform.openai.com/docs/api-reference/chat/create
        # One-off collection
        # message = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages).choices[0].message
        # self.messages.append(message)
        # self.log(message.content)

        # stream
        response = openai.ChatCompletion.create(
            model=model,
            messages=self.messages,
            # temperature=0,
            stream=True,
        )

        contents = []
        print("\033[33m\n")
        for chunk in response:
            c = chunk['choices'][0]['delta'].get('content', '')
            contents.append(c)
            print(c, end="", flush=True)
        print("\033[0m\n")

        self.messages_add("".join(contents), role="assistant")

    def mock(self):
        print(f"\n<{repr(self.messages)}>")
        return

    def messages_add(self, content, role="user"):
        # https://platform.openai.com/docs/guides/chat/chat-vs-completions

        m = {
            "role": role,
            "content": content,
        }
        self.messages.append(m)
        return self.messages


def reset_stdin():
    if platform.system() == "Windows":
        console = "CONIN$"
    else:
        # todo
        # may be error in MacOS
        # unix has function: os.ttyname()
        # console = "/dev/tty"
        console = os.ttyname(1)

    sys.stdin.close()
    sys.stdin = open(console, 'r')


def signal_quit(signum, frame):
    print("\n")
    print_prompt("Do you want to exit? ([y]/n)")
    # https://stackoverflow.com/questions/75367828/runtimeerror-reentrant-call-inside-io-bufferedwriter-name-stdout
    # cause RuntimeError: reentrant call inside <_io.BufferedReader name='<stdin>'>stdin
    # c = input().lower()
    c = os.read(sys.stdin.fileno(), 10).decode().strip().lower()
    if c in ("y", "\n", "yes"):
        print("\033[0m\n")
        exit(0)
    else:
        print_prompt()


def run_help():
    h = """
    chatgpt "ask your question"
    chatgpt -i  # 进入交互模式 使用 Ctrl-Z(win) 或 Ctrl-D(unix) 结束输入, Ctrl-C 退出
    echo "question" | chatgpt [-i] "translate chinese"
    """

    print(h)
    exit(0)


def main():
    if len(sys.argv) > 1 or (not sys.stdin.isatty()):
        signal.signal(signal.SIGINT, signal_quit)
        chatGPT().run()
    else:
        run_help()


if __name__ == '__main__':
    main()