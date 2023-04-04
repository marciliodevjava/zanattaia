import requests
import webbrowser
import tkinter as tk
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class ChatGUI:
    def __init__(self):
        self.chatbot = ChatBot('Meu Assistente')
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.trainer.train("chatterbot.corpus.portuguese")
        self.create_widgets()

    def create_widgets(self):
        self.root = tk.Tk()
        self.root.title("Chatbot")
        self.root.geometry("800x800")
        self.root.configure(bg="#BFEFFF")

        self.chat_box = tk.Text(self.root, bd=0, bg="#FFFFFF", fg="#000000", height=40, width=100, font=("Verdana", 14))
        self.chat_box.config(state=tk.DISABLED)

        self.scrollbar = tk.Scrollbar(self.root, command=self.chat_box.yview, cursor="heart")
        self.chat_box['yscrollcommand'] = self.scrollbar.set

        self.entry_box = tk.Entry(self.root, bd=0, bg="#FFFFFF", fg="#000000", width=70, font=("Verdana", 14))
        self.entry_box.bind('<Return>', self.send_message)

        self.send_button = tk.Button(self.root, text="Enviar", width=12, height=5,
                                     bd=0, bg="#000000", fg="#BFEFFF", activebackground="#006600",
                                     font=("Verdana", 14), command=self.send_message)

        self.search_button = tk.Button(self.root, text="Pesquisar", width=12, height=5,
                                       bd=0, bg="#000000", fg="#BFEFFF", activebackground="#006600",
                                       font=("Verdana", 14), command=self.search)

        self.chat_box.place(x=20, y=20, width=760, height=600)
        self.scrollbar.place(x=780, y=20, height=600)
        self.entry_box.place(x=20, y=640, width=700, height=80)
        self.send_button.place(x=730, y=640, width=60, height=80)
        self.search_button.place(x=20, y=740, width=760, height=40)

    def run(self):
        self.root.mainloop()

    def get_response(self, user_input):
        return str(self.chatbot.get_response(user_input))

    def send_message(self, event=None):
        user_input = self.entry_box.get().strip()
        if not user_input:
            return

        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, "Você: " + user_input + "\n")
        self.chat_box.config(foreground="#000000", font=("Verdana", 14))

        response = self.get_response(user_input)
        self.chat_box.insert(tk.END, "Chatbot: " + response + "\n\n")
        self.chat_box.config(state=tk.DISABLED)
        self.chat_box.yview(tk.END)

        self.entry_box.delete(0, tk.END)
        self.entry_box.focus()

    def search(self):
        query = self.entry_box.get().strip()
        if not query:
            return

        if "chatgpt" in query.lower():
            # abre uma nova guia no navegador para pesquisar no ChatGPT
            search_url = f"https://chatgpt.com/search?q={query}"
            webbrowser.open_new(search_url)
        else:
            # faz uma solicitação GET para o DuckDuckGo API com a consulta
            api_url = f"https://api.duckduckgo.com/?q={query}&format=json"
            response = requests.get(api_url).json()

            # extrai a resposta e exibe-a na caixa de chat
            if response['Abstract']:
                self.chat_box.config(state=tk.NORMAL)
                self.chat_box.insert(tk.END, f"Chatbot: {response['Abstract']}\n\n")
                self.chat_box.config(state=tk.DISABLED)
            else:
                self.chat_box.config(state=tk.NORMAL)
                self.chat_box.insert(tk.END, f"Chatbot: Desculpe, eu não sei a resposta para '{query}'.\n\n")
                self.chat_box.config(state=tk.DISABLED)

        self.entry_box.delete(0, tk.END)
        self.entry_box.focus()


if __name__ == '__main__':
    chat = ChatGUI()
    chat.run()
