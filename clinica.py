import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

DATA_DIR = "clinica_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def save_data(filename, data):
    with open(os.path.join(DATA_DIR, filename), "w") as f:
        json.dump(data, f, indent=4)

def load_data(filename):
    try:
        with open(os.path.join(DATA_DIR, filename), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

pacientes = load_data("pacientes.json")
medicos = load_data("medicos.json")
consultas = load_data("consultas.json")

def gerar_id(dicionario):
    return str(max([int(i) for i in dicionario.keys()], default=0) + 1)

def cadastrar_paciente():
    def salvar():
        nome = nome_entry.get()
        cpf = cpf_entry.get()
        tel = tel_entry.get()
        if nome and cpf and tel:
            pid = gerar_id(pacientes)
            pacientes[pid] = {"nome": nome, "cpf": cpf, "telefone": tel}
            save_data("pacientes.json", pacientes)
            messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
            win.destroy()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos.")

    win = tk.Toplevel(root)
    win.title("Cadastrar Paciente")
    tk.Label(win, text="Nome:").grid(row=0, column=0)
    tk.Label(win, text="CPF:").grid(row=1, column=0)
    tk.Label(win, text="Telefone:").grid(row=2, column=0)
    nome_entry = tk.Entry(win)
    cpf_entry = tk.Entry(win)
    tel_entry = tk.Entry(win)
    nome_entry.grid(row=0, column=1)
    cpf_entry.grid(row=1, column=1)
    tel_entry.grid(row=2, column=1)
    tk.Button(win, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2)

def excluir_paciente():
    def excluir():
        pid = entry_id.get()
        if pid in pacientes:
            del pacientes[pid]
            save_data("pacientes.json", pacientes)
            messagebox.showinfo("Sucesso", "Paciente excluído.")
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title("Excluir Paciente")
    tk.Label(win, text="ID do Paciente:").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Excluir", command=excluir).pack()

def ver_pacientes():
    win = tk.Toplevel(root)
    win.title("Lista de Pacientes")
    text = tk.Text(win, width=60, height=20)
    text.pack()
    for pid, p in pacientes.items():
        text.insert(tk.END, f"ID: {pid}\nNome: {p['nome']}\nCPF: {p['cpf']}\nTelefone: {p['telefone']}\n\n")

def cadastrar_medico():
    def salvar():
        nome = nome_entry.get()
        esp = esp_entry.get()
        crm = crm_entry.get()
        if nome and esp and crm:
            mid = gerar_id(medicos)
            medicos[mid] = {"nome": nome, "especialidade": esp, "crm": crm}
            save_data("medicos.json", medicos)
            messagebox.showinfo("Sucesso", "Médico cadastrado com sucesso!")
            win.destroy()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos.")

    win = tk.Toplevel(root)
    win.title("Cadastrar Médico")
    tk.Label(win, text="Nome:").grid(row=0, column=0)
    tk.Label(win, text="Especialidade:").grid(row=1, column=0)
    tk.Label(win, text="CRM:").grid(row=2, column=0)
    nome_entry = tk.Entry(win)
    esp_entry = tk.Entry(win)
    crm_entry = tk.Entry(win)
    nome_entry.grid(row=0, column=1)
    esp_entry.grid(row=1, column=1)
    crm_entry.grid(row=2, column=1)
    tk.Button(win, text="Salvar", command=salvar).grid(row=3, column=0, columnspan=2)

def excluir_medico():
    def excluir():
        mid = entry_id.get()
        if mid in medicos:
            del medicos[mid]
            save_data("medicos.json", medicos)
            messagebox.showinfo("Sucesso", "Médico excluído.")
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title("Excluir Médico")
    tk.Label(win, text="ID do Médico:").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Excluir", command=excluir).pack()

def ver_medicos():
    win = tk.Toplevel(root)
    win.title("Lista de Médicos")
    text = tk.Text(win, width=60, height=20)
    text.pack()
    for mid, m in medicos.items():
        text.insert(tk.END, f"ID: {mid}\nNome: {m['nome']}\nEspecialidade: {m['especialidade']}\nCRM: {m['crm']}\n\n")

def marcar_consulta():
    def salvar():
        pid = paciente_var.get().split(" - ")[0]
        mid = medico_var.get().split(" - ")[0]
        data = data_entry.get()
        hora = hora_entry.get()
        obs = obs_entry.get()

        if pid and mid and data and hora:
            for c in consultas.values():
                if c["medico"] == mid and c["data"] == data and c["hora"] == hora:
                    messagebox.showerror("Erro", "Médico já possui consulta neste horário.")
                    return
            cid = gerar_id(consultas)
            consultas[cid] = {
                "paciente": pid,
                "medico": mid,
                "data": data,
                "hora": hora,
                "observacoes": obs
            }
            save_data("consultas.json", consultas)
            messagebox.showinfo("Sucesso", "Consulta marcada com sucesso!")
            win.destroy()
        else:
            messagebox.showwarning("Erro", "Preencha todos os campos obrigatórios.")

    win = tk.Toplevel(root)
    win.title("Marcar Consulta")

    tk.Label(win, text="Paciente:").grid(row=0, column=0)
    tk.Label(win, text="Médico:").grid(row=1, column=0)
    tk.Label(win, text="Data (DD/MM/AAAA):").grid(row=2, column=0)
    tk.Label(win, text="Hora (HH:MM):").grid(row=3, column=0)
    tk.Label(win, text="Observações:").grid(row=4, column=0)

    paciente_var = tk.StringVar(win)
    medico_var = tk.StringVar(win)

    paciente_menu = ttk.Combobox(win, textvariable=paciente_var, values=[
        f"{k} - {v['nome']}" for k, v in pacientes.items()
    ])
    medico_menu = ttk.Combobox(win, textvariable=medico_var, values=[
        f"{k} - {v['nome']} ({v['especialidade']})" for k, v in medicos.items()
    ])
    data_entry = tk.Entry(win)
    hora_entry = tk.Entry(win)
    obs_entry = tk.Entry(win)

    paciente_menu.grid(row=0, column=1)
    medico_menu.grid(row=1, column=1)
    data_entry.grid(row=2, column=1)
    hora_entry.grid(row=3, column=1)
    obs_entry.grid(row=4, column=1)

    tk.Button(win, text="Salvar", command=salvar).grid(row=5, column=0, columnspan=2)

def consultar_consultas():
    win = tk.Toplevel(root)
    win.title("Consultas Marcadas")
    text = tk.Text(win, width=80, height=20)
    text.pack()
    for cid, c in consultas.items():
        paciente = pacientes.get(c["paciente"], {}).get("nome", "Desconhecido")
        medico = medicos.get(c["medico"], {}).get("nome", "Desconhecido")
        text.insert(tk.END, f"ID: {cid}\nPaciente: {paciente}\nMédico: {medico}\nData: {c['data']} {c['hora']}\nObs: {c['observacoes']}\n\n")

def excluir_consulta():
    def excluir():
        cid = entry_id.get()
        if cid in consultas:
            del consultas[cid]
            save_data("consultas.json", consultas)
            messagebox.showinfo("Sucesso", "Consulta excluída.")
            win.destroy()
        else:
            messagebox.showerror("Erro", "ID não encontrado.")

    win = tk.Toplevel(root)
    win.title("Excluir Consulta")
    tk.Label(win, text="ID da Consulta:").pack()
    entry_id = tk.Entry(win)
    entry_id.pack()
    tk.Button(win, text="Excluir", command=excluir).pack()

root = tk.Tk()
root.title("Sistema da Clínica Médica")

tk.Button(root, text="Cadastrar Paciente", width=30, command=cadastrar_paciente).pack(pady=5)
tk.Button(root, text="Excluir Paciente", width=30, command=excluir_paciente).pack(pady=5)
tk.Button(root, text="Ver Pacientes", width=30, command=ver_pacientes).pack(pady=5)
tk.Button(root, text="Cadastrar Médico", width=30, command=cadastrar_medico).pack(pady=5)
tk.Button(root, text="Excluir Médico", width=30, command=excluir_medico).pack(pady=5)
tk.Button(root, text="Ver Médicos", width=30, command=ver_medicos).pack(pady=5)
tk.Button(root, text="Marcar Consulta", width=30, command=marcar_consulta).pack(pady=5)
tk.Button(root, text="Consultar Consultas", width=30, command=consultar_consultas).pack(pady=5)
tk.Button(root, text="Excluir Consulta", width=30, command=excluir_consulta).pack(pady=5)
tk.Button(root, text="Sair", width=30, command=root.quit).pack(pady=20)

root.mainloop()