import tkinter as tk
from funcoes import *

tarefas = {}
janela = tk.Tk()
janela.title("To Do List")  # Título da janela
janela.geometry("400x300")  # Tamannho da jánela
janela.configure(bg="#001F3F")  # Cor da janela

# Frame para adicionar as tarefas
frame_add_tarefa = tk.Frame(janela,  bg="#001F3F", bd=2)
frame_add_tarefa.pack(pady=10)

label = tk.Label(frame_add_tarefa, text="Digite a tarefa:",
                 bg="#001F3F", fg="#FFF", font=("Arial", 10, "bold"))
label.pack(side="left", padx=5)

entrada = tk.Entry(frame_add_tarefa, width=20,
                   bg="#1F4E78", fg="#FFF", bd=2, relief="groove")
entrada.pack(side="left", padx=5)  # caixa de texto


botao = tk.Button(frame_add_tarefa, bg="lightgreen", text="Adicionar Tarefa", font=(
    "Arial", 10, "bold"), command=lambda: criar_tarefa(tarefas, entrada, frame_tarefas))
botao.pack(side="left", padx=5)  # Botão Adicionar tarefa

# ==========================================#

# frame para exibir as tarefas
frame_tarefas = tk.Frame(janela, bg="#001F3F")
frame_tarefas.pack(pady=10)

atualizar_visualizacao(frame_tarefas, tarefas)

janela.mainloop()
