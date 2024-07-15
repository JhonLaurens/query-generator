import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import pyperclip
from ttkthemes import ThemedStyle

class GeneradorQueries(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Generador de Queries")
        self.geometry("800x600")
        self.minsize(600, 400)

        style = ThemedStyle(self)
        style.set_theme("clam")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        self.crear_widgets()

    def crear_widgets(self):
        frame_predefinidos = ttk.LabelFrame(self, text="Queries Predefinidos", padding=10)
        frame_predefinidos.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame_predefinidos.columnconfigure((0, 1), weight=1)

        labels = ["Usuarios Privilegiados", "Jobs Habilitados", "Conteo de Jobs Habilitados"]
        queries = [
            """select a.username, b.granted_role from dba_users a, dba_role_privs b
where a.username=b.grantee
and granted_role='DBA';""",
            """select * from dba_scheduler_jobs
Where owner not in ('SYS','SYSTEM','ORACLE_OCM')
AND enabled='TRUE';""",
            """select count (*) from dba_scheduler_jobs
Where owner not in ('SYS','SYSTEM','ORACLE_OCM')
AND enabled='TRUE';"""
        ]

        for i, (label, query) in enumerate(zip(labels, queries)):
            frame = ttk.Frame(frame_predefinidos)
            frame.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
            frame.columnconfigure(0, weight=1)

            ttk.Label(frame, text=label).grid(row=0, column=0, sticky="w")
            ttk.Button(frame, text="Copiar", command=lambda q=query: self.copiar_query_predefinida(q)).grid(row=0, column=1, padx=(5, 0))

            text = tk.Text(frame_predefinidos, height=5, width=40, wrap=tk.WORD)
            text.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")
            text.insert(tk.END, query)
            text.config(state=tk.DISABLED)

        frame_datos = ttk.LabelFrame(self, text="Entrada de Datos", padding=10)
        frame_datos.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        frame_datos.columnconfigure(1, weight=1)

        ttk.Label(frame_datos, text="Fecha de inicio:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.fecha_inicio_cal = DateEntry(frame_datos, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_inicio_cal.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame_datos, text="Fecha de fin:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.fecha_fin_cal = DateEntry(frame_datos, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_fin_cal.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame_datos, text="Fecha de inicio (CREACIÓN DE USUARIO BD):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.fecha_inicio_creacion = DateEntry(frame_datos, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_inicio_creacion.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame_datos, text="Fecha de fin (CREACIÓN DE USUARIO BD):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.fecha_fin_creacion = DateEntry(frame_datos, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.fecha_fin_creacion.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(frame_datos, text="Lista de usuarios:").grid(row=4, column=0, sticky="ne", padx=5, pady=5)
        self.usuarios_text = tk.Text(frame_datos, height=5, width=40)
        self.usuarios_text.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")
        self.usuarios_text.bind('<KeyRelease>', self.contar_usuarios)

        self.contador_usuarios = ttk.Label(frame_datos, text="Usuarios: 0")
        self.contador_usuarios.grid(row=4, column=2, sticky="nw", padx=5, pady=5)

        frame_botones = ttk.Frame(self, padding=10)
        frame_botones.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Button(frame_botones, text="Generar Queries", command=self.generar_query).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="Generar queries de BD", command=self.generar_query_creacion).pack(side=tk.LEFT, padx=5)

        frame_resultados = ttk.LabelFrame(self, text="Resultados", padding=10)
        frame_resultados.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        frame_resultados.columnconfigure(1, weight=1)
        frame_resultados.rowconfigure((0, 1, 2, 3), weight=1)

        ttk.Label(frame_resultados, text="Query 1:").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.resultado1 = tk.Text(frame_resultados, height=10, width=80)
        self.resultado1.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame_resultados, text="Copiar Query 1", command=lambda: self.copiar_query(1)).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(frame_resultados, text="Query 2:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.resultado2 = tk.Text(frame_resultados, height=10, width=80)
        self.resultado2.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame_resultados, text="Copiar Query 2", command=lambda: self.copiar_query(2)).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(frame_resultados, text="Query 3:").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.resultado3 = tk.Text(frame_resultados, height=10, width=80)
        self.resultado3.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame_resultados, text="Copiar Query 3", command=lambda: self.copiar_query(3)).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(frame_resultados, text="Query 4:").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        self.resultado4 = tk.Text(frame_resultados, height=10, width=80)
        self.resultado4.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame_resultados, text="Copiar Query 4", command=lambda: self.copiar_query(4)).grid(row=3, column=2, padx=5, pady=5)

    def contar_usuarios(self, event=None):
        usuarios = [user.strip() for user in self.usuarios_text.get(1.0, tk.END).split('\n') if user.strip()]
        self.contador_usuarios.config(text=f"Usuarios: {len(usuarios)}")

    def generar_query(self):
        fecha_inicio = self.fecha_inicio_cal.get_date().strftime('%d/%m/%Y')
        fecha_fin = self.fecha_fin_cal.get_date().strftime('%d/%m/%Y')

        db_users = [user.strip() for user in self.usuarios_text.get(1.0, tk.END).split('\n') if user.strip()]

        if not db_users:
            messagebox.showerror("Error", "La lista de usuarios está vacía")
            return

        query1 = f"""select * from dba_fga_audit_trail
where 
SQL_TEXT NOT LIKE 'SELECT%' AND SQL_TEXT NOT LIKE 'select%' 
AND
STATEMENT_TYPE NOT LIKE 'SELECT%'
AND 
TIMESTAMP BETWEEN TO_DATE('{fecha_inicio}', 'DD/MM/YYYY')   
AND TO_DATE('{fecha_fin}', 'DD/MM/YYYY')
AND DB_USER IN ({','.join([f"'{user}'" for user in db_users])})"""

        query2 = f"""select count (*) from dba_fga_audit_trail
where 
SQL_TEXT NOT LIKE 'SELECT%' AND SQL_TEXT NOT LIKE 'select%' 
AND
STATEMENT_TYPE NOT LIKE 'SELECT%'
AND 
TIMESTAMP BETWEEN TO_DATE('{fecha_inicio}', 'DD/MM/YYYY')   
AND TO_DATE('{fecha_fin}', 'DD/MM/YYYY')
AND DB_USER IN ({','.join([f"'{user}'" for user in db_users])})"""

        self.resultado1.delete(1.0, tk.END)
        self.resultado1.insert(tk.END, query1)
        self.resultado2.delete(1.0, tk.END)
        self.resultado2.insert(tk.END, query2)

    def generar_query_creacion(self):
        fecha_inicio = self.fecha_inicio_creacion.get_date().strftime('%d/%m/%Y')
        fecha_fin = self.fecha_fin_creacion.get_date().strftime('%d/%m/%Y')

        query3 = f"""SELECT * FROM DBADMON.ADM_TBLOGUSERS 
WHERE 
FECHA_CREA BETWEEN TO_DATE('{fecha_inicio}', 'DD/MM/YYYY') 
AND TO_DATE('{fecha_fin}', 'DD/MM/YYYY')"""

        query4 = f"""SELECT count (*) FROM DBADMON.ADM_TBLOGUSERS 
WHERE 
FECHA_CREA BETWEEN TO_DATE('{fecha_inicio}', 'DD/MM/YYYY') 
AND TO_DATE('{fecha_fin}', 'DD/MM/YYYY')"""

        self.resultado3.delete(1.0, tk.END)
        self.resultado3.insert(tk.END, query3)
        self.resultado4.delete(1.0, tk.END)
        self.resultado4.insert(tk.END, query4)

    def copiar_query(self, query_num):
        if query_num == 1:
            pyperclip.copy(self.resultado1.get(1.0, tk.END).strip())
        elif query_num == 2:
            pyperclip.copy(self.resultado2.get(1.0, tk.END).strip())
        elif query_num == 3:
            pyperclip.copy(self.resultado3.get(1.0, tk.END).strip())
        else:
            pyperclip.copy(self.resultado4.get(1.0, tk.END).strip())
        messagebox.showinfo("Copiado", f"Query {query_num} copiado al portapapeles")

    def copiar_query_predefinida(self, query):
        pyperclip.copy(query)
        messagebox.showinfo("Copiado", "Query copiado al portapapeles")

if __name__ == "__main__":
    app = GeneradorQueries()
    app.mainloop()
