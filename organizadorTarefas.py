import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os

# Função para conectar ao banco de dados
def conectar_banco():
    return sqlite3.connect('tarefas.db')

# Criar a tabela no banco de dados
def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            professor TEXT,
            materia TEXT,
            data_vencimento DATE,
            prioridade TEXT,
            status TEXT DEFAULT 'pendente',
            arquivo TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Inserir nova tarefa
def adicionar_tarefa(titulo, professor, materia, data_vencimento, prioridade, arquivo):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tarefas (titulo, professor, materia, data_vencimento, prioridade, arquivo)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (titulo, professor, materia, data_vencimento, prioridade, arquivo))
    conn.commit()
    conn.close()

# Buscar todas as tarefas
def buscar_tarefas():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

# Atualizar o status para concluída
def marcar_como_concluida(tarefa_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET status = "Concluída" WHERE id = ?', (tarefa_id,))
    conn.commit()
    conn.close()

# Excluir uma tarefa
def excluir_tarefa(tarefa_id):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
    conn.commit()
    conn.close()

# Selecionar arquivo
def selecionar_arquivo():
    caminho = filedialog.askopenfilename()
    if caminho:
        entry_arquivo.config(state=tk.NORMAL)
        entry_arquivo.delete(0, tk.END)
        entry_arquivo.insert(0, caminho)
        entry_arquivo.config(state='readonly')

# Adicionar nova tarefa
def adicionar():
    titulo = entry_titulo.get()
    professor = entry_professor.get()
    materia = entry_materia.get()
    data_vencimento = entry_data_vencimento.get()
    prioridade = combo_prioridade.get()
    arquivo = entry_arquivo.get()

    if not (titulo and data_vencimento and prioridade):
        messagebox.showwarning("Erro", "Preencha todos os campos obrigatórios!")
        return

    try:
        datetime.strptime(data_vencimento, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
        return

    adicionar_tarefa(titulo, professor, materia, data_vencimento, prioridade, arquivo)
    messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
    atualizar_lista_tarefas()

    entry_titulo.delete(0, tk.END)
    entry_professor.delete(0, tk.END)
    entry_materia.delete(0, tk.END)
    entry_data_vencimento.delete(0, tk.END)
    entry_arquivo.config(state=tk.NORMAL)
    entry_arquivo.delete(0, tk.END)
    entry_arquivo.config(state='readonly')
    combo_prioridade.set("Alta")

# Atualizar a visualização das tarefas
def atualizar_lista_tarefas():
    lista_tarefas.config(state=tk.NORMAL)
    lista_tarefas.delete("1.0", tk.END)
    tarefas = buscar_tarefas()
    for tarefa in tarefas:
        nome_arquivo = os.path.basename(tarefa[7]) if tarefa[7] else "Nenhum"
        tarefa_str = (
            f"ID: {tarefa[0]} | Título: {tarefa[1]} | Professor: {tarefa[2]} | "
            f"Matéria: {tarefa[3]} | Vencimento: {tarefa[4]} | "
            f"Prioridade: {tarefa[5]} | Status: {tarefa[6]} | Arquivo: {nome_arquivo}\n"
        )
        if tarefa[6].lower() == "concluída":
            lista_tarefas.insert(tk.END, tarefa_str, "concluida")
        else:
            lista_tarefas.insert(tk.END, tarefa_str)
    lista_tarefas.config(state=tk.DISABLED)

# Marcar uma tarefa como concluída
def marcar_concluida():
    try:
        linha = lista_tarefas.get(tk.SEL_FIRST, tk.SEL_LAST)
        tarefa_id = int(linha.split("|")[0].split(":")[1].strip())
        marcar_como_concluida(tarefa_id)
        messagebox.showinfo("Sucesso", "Tarefa marcada como concluída!")
        atualizar_lista_tarefas()
    except:
        messagebox.showwarning("Erro", "Selecione uma tarefa para marcar como concluída.")

# Excluir tarefa selecionada
def excluir():
    try:
        linha = lista_tarefas.get(tk.SEL_FIRST, tk.SEL_LAST)
        tarefa_id = int(linha.split("|")[0].split(":")[1].strip())
        excluir_tarefa(tarefa_id)
        messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso!")
        atualizar_lista_tarefas()
    except:
        messagebox.showwarning("Erro", "Selecione uma tarefa para excluir.")

# --- Interface Gráfica ---
root = tk.Tk()
root.title("PlanejAI!")
root.geometry("950x650")
root.resizable(False, False)
root.configure(bg="#315379")

frame_adicionar = tk.Frame(root, bg="#315379")
frame_adicionar.pack(padx=10, pady=10)

def estilo_entry(entry):
    entry.configure(bg="#f0f0f0", fg="#333333", font=("Poppins", 10))

tk.Label(frame_adicionar, text="Título da Tarefa:", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=0, column=0, sticky="w", pady=2, padx=(50, 90))
entry_titulo = tk.Entry(frame_adicionar, width=60, bd=3, relief="sunken")
entry_titulo.grid(row=0, column=1, pady=2, padx=(90, 50))
estilo_entry(entry_titulo)

tk.Label(frame_adicionar, text="Professor(a):", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=1, column=0, sticky="w", pady=2, padx=(50, 90))
entry_professor = tk.Entry(frame_adicionar, width=60, bd=3, relief="sunken")
entry_professor.grid(row=1, column=1, pady=2, padx=(90, 50))
estilo_entry(entry_professor)

tk.Label(frame_adicionar, text="Matéria:", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=2, column=0, sticky="w", pady=2, padx=(50, 90))
entry_materia = tk.Entry(frame_adicionar, width=60, bd=3, relief="sunken")
entry_materia.grid(row=2, column=1, pady=2, padx=(90, 50))
estilo_entry(entry_materia)

tk.Label(frame_adicionar, text="Data de Vencimento:", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=3, column=0, sticky="w", pady=2, padx=(50, 90))
entry_data_vencimento = tk.Entry(frame_adicionar, width=60, bd=3, relief="sunken")
entry_data_vencimento.grid(row=3, column=1, pady=2, padx=(90, 50))
estilo_entry(entry_data_vencimento)

# Frame para Entry + Botão do arquivo
frame_arquivo = tk.Frame(frame_adicionar, bg="#315379")
frame_arquivo.grid(row=4, column=1, pady=2, padx=(90, 50), sticky="w")
tk.Label(frame_adicionar, text="Arquivo:", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=4, column=0, sticky="w", pady=2, padx=(50, 90))
entry_arquivo = tk.Entry(frame_arquivo, width=42, bd=3, relief="sunken", state='readonly')
entry_arquivo.pack(side="left", padx=(0, 10))
estilo_entry(entry_arquivo)

btn_arquivo = tk.Button(frame_arquivo, text="Selecionar Arquivo", command=selecionar_arquivo, bg="white", font=("Poppins", 8, "bold"))
btn_arquivo.pack(side="left")

# # Arquivo
# tk.Label(frame_adicionar, text="Arquivo:", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=4, column=0, sticky="w", pady=2, padx=(50, 90))
# entry_arquivo = tk.Entry(frame_adicionar, width=46, bd=3, relief="sunken", state='readonly')
# entry_arquivo.grid(row=4, column=1, sticky="w", pady=2, padx=(90, 0))
# estilo_entry(entry_arquivo)
# btn_arquivo = tk.Button(frame_adicionar, text="Selecionar Arquivo", command=selecionar_arquivo, bg="white", font=("Poppins", 8, "bold"))
# btn_arquivo.grid(row=4, column=1, sticky="e", padx=(0, 50))

tk.Label(frame_adicionar, text="Prioridade:", bg="#315379", fg="white", font=("Poppins", 11, "bold")).grid(row=5, column=0, sticky="w", pady=3, padx=(50, 90))
combo_prioridade = tk.StringVar()
combo_prioridade.set("Alta")
dropdown_prioridade = tk.OptionMenu(frame_adicionar, combo_prioridade, "Alta", "Média", "Baixa")
dropdown_prioridade.config(bd=3, relief="ridge")
dropdown_prioridade.grid(row=5, column=1, sticky="w", pady=3, padx=(275, 50))

btn_adicionar = tk.Button(
    frame_adicionar, text="Adicionar Tarefa", command=adicionar,
    width=25, height=1, font=("Poppins", 11, "bold"), bg="white", fg="black", bd=5,
    highlightcolor="blue", highlightbackground="blue", highlightthickness=3
)
btn_adicionar.grid(row=6, column=0, columnspan=2, pady=10)

# Lista de tarefas
frame_lista = tk.Frame(root, bg="#315379")
frame_lista.pack(padx=10, pady=10)

lista_tarefas = tk.Text(frame_lista, width=130, height=17, wrap="none", font=("Poppins", 8, "italic"))
lista_tarefas.pack()
lista_tarefas.tag_config("concluida", foreground="green", font=("Poppins", 8, "italic"))

btn_marcar_concluida = tk.Button(
    frame_lista, text="Marcar como Concluída", command=marcar_concluida,
    width=25, height=1, font=("Poppins", 11, "bold"), bg="white", fg="black", bd=5,
    highlightcolor="blue", highlightbackground="blue", highlightthickness=3
)
btn_marcar_concluida.pack(pady=(20, 5))

btn_excluir = tk.Button(
    frame_lista, text="Excluir Tarefa", command=excluir,
    width=25, height=1, font=("Poppins", 11, "bold"), bg="white", fg="black", bd=5,
    highlightcolor="blue", highlightbackground="blue", highlightthickness=3
)
btn_excluir.pack(pady=5)

# Inicialização
criar_tabela()
atualizar_lista_tarefas()
root.mainloop()
