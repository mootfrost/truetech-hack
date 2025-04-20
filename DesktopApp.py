from tkinter import Tk,StringVar,Variable,messagebox,Listbox,Scrollbar
from tkinter import ttk
from tkinter import font
import json

tk = Tk()
message = StringVar(tk, name="message")
logs = Variable(tk, name="logs", value=())
CHAT_WND_WIDTH = 73

def putmsg(*args):
  l = []
  for i in args:
    while len(i) > CHAT_WND_WIDTH - 1:
      l.append(i[:CHAT_WND_WIDTH])
      i = i[CHAT_WND_WIDTH:]
    l.append(i)
  log = logs.get()
  logs.set((*log, *l))

def onclick():
  st = message.get()
  putmsg("Пользователь", st, '')
  payload = json.dumps(st)
  # try:
  #   response = requests.post("https://api.guvolution.com", data=payload)
  #   msg = json.loads(response.json())
  #   putmsg(msg)
  # except Exception as e:
  #   messagebox.showerror(title="Ошибка", message="Произошла ошибка при обработке сообщения.\n\n" + str(e))
  response = "Your Sound Card Works Perfectly" # Пока что тестовый ответ
  putmsg("Помощник", response, "")

tk["width"] = 640
tk["height"] = 480
tk.resizable(False, False)
tk.title("GuVolution Chat Client")

msglogs = Listbox(tk, height=17, width=CHAT_WND_WIDTH, listvariable=logs)
msglogs.place(x=30, y=30)

scroll = Scrollbar(tk, orient="vertical", command=msglogs.yview)
scroll.place(x=620, y=30)
msglogs["yscrollcommand"] = scroll.set

inpt = ttk.Entry(tk, name="msgText", width=37, font=font.Font(size=14), textvariable=message)
inpt.place(x=30,y=400)

btn = ttk.Button(tk, name="sendBtn", text="Отправить", width=20, command=onclick)
btn.place(x=450, y=400)

tk.mainloop()
