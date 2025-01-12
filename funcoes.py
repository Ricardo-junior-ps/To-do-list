import tkinter as tk
from tkinter import messagebox  # módulo para alertar na hora de preecher os campos
from tkinter import font  # módulo para modificar o checkbox
import os  # módulo para salvar o dicionário do arquivo
import json  # formato para salvar o dicionário


def interface_tkinter():  # Função de layout do programa
    verificar_arquivo()
    tarefas = carregar_tarefas()

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

    janela.mainloop()

    # ==========================================#

    # frame para exibir as tarefas
    frame_tarefas = tk.Frame(janela, bg="#001F3F")
    frame_tarefas.pack(pady=10)

    atualizar_visualizacao(frame_tarefas, tarefas)

# ====================================================#


# declaração de variáveis para ser usada com o OS no salvamento de arquivos
caminho_pasta = "pasta_tarefas"
nome_arquivo = "tarefas.json"
caminho = os.path.join(caminho_pasta, nome_arquivo)

# ====================================================#

# Função para verificar se o caminho existe, caso não exista, ele cria


def verificar_arquivo():
    os.makedirs(caminho_pasta, exist_ok=True)

# ====================================================#

# Função para salvar o dicionário no arquivo ".txt"


def salvar_tarefas(tarefas):
    verificar_arquivo()  # Garante que o caminho existe
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)

# ====================================================#

# Função para carregar o dicionário, caso não exista, retorna um dicionário vazio


def carregar_tarefas():
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return {}

# ====================================================#

# Função para criar uma tarefa, a partir do campo de entrada da interface


def criar_tarefa(tarefas, entrada, frame_tarefas):
    tarefa = entrada.get()
    if not tarefa:  # verifica se o campo de entrada está vazio
        messagebox.showwarning("Aviso", "O campo de texto está vazio!")
    elif tarefa in tarefas:  # verifica se a tarefa digitada já existe
        messagebox.showwarning("Aviso", "Esta tarefa já existe!")
    else:  # cadastra a tarefa no dicionário
        tarefas[tarefa] = False
        entrada.delete(0, tk.END)
        salvar_tarefas(tarefas)
        atualizar_visualizacao(frame_tarefas, tarefas)


# ====================================================#

# Função para mostrar na interface as tarefas cadastradas
def atualizar_visualizacao(frame_tarefas, tarefas):
    for widget in frame_tarefas.winfo_children():  # Destroi o contedudo anterior
        widget.destroy()
    for tarefa, status in tarefas.items():  # cria o novo conteúdo atualizado
        criar_item(tarefas, tarefa, status, frame_tarefas)

# ====================================================#

# Função para criar cada tarefa, com o checkbox, texto e botão de editar e excluir a tarefa.


def criar_item(tarefas, tarefa, status, frame_tarefas):
    texto_cortado = font.Font(overstrike=1)
    texto_normal = font.Font(overstrike=0)

    frame_item = tk.Frame(frame_tarefas, bg="#001F3F")
    frame_item.pack(fill="x", pady=5)

    val_checkbox = tk.BooleanVar(value=status)
    check = tk.Checkbutton(frame_item, text=tarefa, variable=val_checkbox, bg="#001F3F", command=lambda: alterar_valor(
        tarefas, tarefa, val_checkbox, check), font=("Arial", 10, "bold"))
    check.pack(side="left", padx=5)
    if val_checkbox.get():  # Verifica se a tarefa já foi concluida para aplicar a formatação
        check.config(fg="red", font=texto_cortado)
    else:  # Verifica se a tarefa não foi concluida para aplicar a formatação
        check.config(fg="#FFF", font=texto_normal)

    botao_excluir = tk.Button(frame_item, text="Excluir", bg="lightcoral", font=(
        "Arial", 10, "bold"), command=lambda: excluir_tarefa(tarefas, tarefa, frame_tarefas))
    botao_excluir.pack(side="right", padx=5)

    botao_editar = tk.Button(frame_item, text="Editar", bg="#0D6EFD", fg="#FFFFFF", font=(
        "Arial", 10, "bold"), command=lambda: editar_tarefa(tarefas, tarefa, frame_tarefas))
    botao_editar.pack(side="right", padx=5)

# ====================================================#

# Função que cria uma nova janela para editar a tarefa, com um novo campo de entrada com a tarefa para ser atualizada
# um botão de para salvar as alterações e um botão de cancelar


def editar_tarefa(tarefas, tarefa, frame_tarefas):
    nova_janela = tk.Toplevel(frame_tarefas)
    nova_janela.title("Editar Tarefa")
    nova_janela.configure(bg="#001F3F")

    frame_editar = tk.Frame(nova_janela, bg="#001F3F")
    frame_editar.pack(padx=10, pady=10)

    label_editar = tk.Label(frame_editar, text="Nova descrição",
                            bg="#001F3F", fg="#FFF", font=("Arial", 10, "bold"))
    label_editar.pack()
    entrada_editar = tk.Entry(frame_editar, width=20, bg="#1F4E78", fg="#FFF")
    entrada_editar.insert(0, tarefa)
    entrada_editar.pack()

    botao_salvar = tk.Button(frame_editar, text="Salvar", bg="lightgreen", command=lambda: salvar_edicao(
        tarefas, tarefa, entrada_editar, nova_janela, frame_tarefas))
    botao_salvar.pack(padx=7, pady=7)

    botao_cancelar = tk.Button(frame_editar, text="Cancelar",
                               bg="lightcoral", fg="#FFFFFF", command=nova_janela.destroy)
    botao_cancelar.pack(padx=7, pady=7)

# ====================================================#

# Função do botão de salvar a edição da tarefa


def salvar_edicao(tarefas, tarefa, entry_editar, nova_janela, frame_tarefas):
    nova_tarefa = entry_editar.get()
    if nova_tarefa:  # Salva no dicionário, salva o dicionário e atualiza a visualização na janela principal
        tarefas[nova_tarefa] = tarefas.pop(tarefa)
        salvar_tarefas(tarefas)
        atualizar_visualizacao(frame_tarefas, tarefas)
        nova_janela.destroy()
    else:  # verifica se o campo de entrada está vazio
        messagebox.showwarning("Aviso", "O campo de texto está vazio!")

# ====================================================#

# Função do checkbox para, assim que alterar o valor, alterar a formatação do texto


def alterar_valor(tarefas, tarefa, val_checkbox, check):
    texto_cortado = font.Font(overstrike=1)
    texto_normal = font.Font(overstrike=0)
    tarefas[tarefa] = val_checkbox.get()
    salvar_tarefas(tarefas)
    if val_checkbox.get():
        check.config(fg="red", font=texto_cortado)
    else:
        check.config(fg="#FFF", font=texto_normal)

# ====================================================#

# função do botão de excluir,


def excluir_tarefa(tarefas, tarefa, frame_tarefas):
    if tarefa in tarefas:
        del tarefas[tarefa]
        salvar_tarefas(tarefas)
        atualizar_visualizacao(frame_tarefas, tarefas)
