import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_DIR = "clinica_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def salvar_json(nome, dados):
    with open(os.path.join(DATA_DIR, nome), "w") as f:
        json.dump(dados, f, indent=4)

def carregar_json(nome):
    caminho = os.path.join(DATA_DIR, nome)
    if os.path.exists(caminho):
        with open(caminho, "r") as f:
            return json.load(f)
    return {}

pacientes = carregar_json("pacientes.json")
medicos = carregar_json("medicos.json")
consultas = carregar_json("consultas.json")

def gerar_id(dic):
    return str(max([int(k) for k in dic.keys()], default=0) + 1)

def interface_crud(titulo, campos, salvar_callback, dados_iniciais=None):
    win = tk.Toplevel(root)
    win.title(titulo)
    entradas = {}

    for i, campo in enumerate(campos):
        tk.Label(win, text=campo).grid(row=i, column=0)
        ent = tk.Entry(win)
        ent.grid(row=i, column=1)
        if dados_iniciais and campo in dados_iniciais:
            ent.insert(0, dados_iniciais[campo])
        entradas[campo] = ent

    def salvar():
        valores = {k: v.get() for k, v in entradas.items()}
        salvar_callback(valores)
        win.destroy()

    tk.Button(win, text="Salvar", command=salvar).grid(row=len(campos), column=0, columnspan=2)

def cadastrar_paciente():
    def salvar(dados):
        pid = gerar_id(pacientes)
        pacientes[pid] = dados
        salvar_json("pacientes.json", pacientes)
        messagebox.showinfo("Pronto", "Paciente cadastrado com sucesso!")

    interface_crud("Cadastrar Paciente", ["nome", "cpf", "telefone"], salvar)

def editar_paciente():
    def buscar():
        pid = entry_id.get()
        if pid in pacientes:
            interface_crud("Editar Paciente", ["nome", "cpf", "telefone"], lambda d: atualizar("pacientes", pacientes, "pacientes.json", pid, d), pacientes[pid])
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title("Editar Paciente")
    tk.Label(win, text="ID do Paciente").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Buscar", command=buscar).pack()

def excluir_paciente():
    excluir("pacientes", pacientes, "pacientes.json")

def ver_pacientes():
    listar("Pacientes", pacientes)

def cadastrar_medico():
    def salvar(dados):
        mid = gerar_id(medicos)
        medicos[mid] = dados
        salvar_json("medicos.json", medicos)
        messagebox.showinfo("Pronto", "Médico cadastrado com sucesso!")

    interface_crud("Cadastrar Médico", ["nome", "especialidade", "crm"], salvar)

def editar_medico():
    def buscar():
        mid = entry_id.get()
        if mid in medicos:
            interface_crud("Editar Médico", ["nome", "especialidade", "crm"], lambda d: atualizar("medicos", medicos, "medicos.json", mid, d), medicos[mid])
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title("Editar Médico")
    tk.Label(win, text="ID do Médico").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Buscar", command=buscar).pack()

def excluir_medico():
    excluir("medicos", medicos, "medicos.json")

def ver_medicos():
    listar("Médicos", medicos)

def marcar_consulta():
    def salvar(dados):
        if dados["paciente_id"] in pacientes and dados["medico_id"] in medicos:
            cid = gerar_id(consultas)
            consultas[cid] = dados
            salvar_json("consultas.json", consultas)
            messagebox.showinfo("Pronto", "Consulta marcada com sucesso!")
        else:
            messagebox.showerror("Erro", "ID do paciente ou médico inválido.")

    interface_crud("Marcar Consulta", ["paciente_id", "medico_id", "data", "hora", "observacoes"], salvar)

def editar_consulta():
    def buscar():
        cid = entry_id.get()
        if cid in consultas:
            interface_crud("Editar Consulta", ["paciente_id", "medico_id", "data", "hora", "observacoes"], lambda d: atualizar("consultas", consultas, "consultas.json", cid, d), consultas[cid])
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title("Editar Consulta")
    tk.Label(win, text="ID da Consulta").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Buscar", command=buscar).pack()

def excluir_consulta():
    excluir("consultas", consultas, "consultas.json")

def consultar_consultas():
    listar("Consultas", consultas)

def listar(titulo, dicionario):
    win = tk.Toplevel(root)
    win.title(titulo)
    for k, v in dicionario.items():
        linha = f"ID: {k}, " + ", ".join([f"{key}: {val}" for key, val in v.items()])
        tk.Label(win, text=linha).pack()

def excluir(tipo, dic, arquivo):
    def deletar():
        rid = entry_id.get()
        if rid in dic:
            del dic[rid]
            salvar_json(arquivo, dic)
            messagebox.showinfo("Sucesso", f"{tipo[:-1].capitalize()} excluído!")
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title(f"Excluir {tipo[:-1].capitalize()}")
    tk.Label(win, text=f"ID do {tipo[:-1].capitalize()}").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Excluir", command=deletar).pack()

def atualizar(tipo, dic, arquivo, id_, novos_dados):
    dic[id_] = novos_dados
    salvar_json(arquivo, dic)
    messagebox.showinfo("Sucesso", f"{tipo[:-1].capitalize()} atualizado com sucesso!")

root = tk.Tk()
root.title("Sistema da Clínica Médica")

botoes = [
    ("Cadastrar Paciente", cadastrar_paciente),
    ("Editar Paciente", editar_paciente),
    ("Excluir Paciente", excluir_paciente),
    ("Ver Pacientes", ver_pacientes),
    ("Cadastrar Médico", cadastrar_medico),
    ("Editar Médico", editar_medico),
    ("Excluir Médico", excluir_medico),
    ("Ver Médicos", ver_medicos),
    ("Marcar Consulta", marcar_consulta),
    ("Editar Consulta", editar_consulta),
    ("Excluir Consulta", excluir_consulta),
    ("Ver Consultas", consultar_consultas),
    ("Sair", root.quit),
]

for texto, funcao in botoes:
    tk.Button(root, text=texto, width=40, command=funcao).pack(pady=3)

root.mainloop()
