from tkinter import *
from tkinter import ttk
import sqlite3

from click import command

root = Tk()

class Funcs():
    def limpar_tela(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor()
    def desconectar_bd(self):
        self.conn.close(); print("DESCONECTANDO DO BANCO DE DADOS!")
    def montaTabelas(self):
        self.conecta_bd(); print("CONECTANDO AO BANCO DE DADOS!")
        ## CRIAR TABELAS
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            )
        """)
        self.conn.commit();print("BANCO DE DADOS CRIADO!")
        self.desconectar_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cidade = self.cidade_entry.get()
    def add_cliente(self):
        self.conecta_bd()
        self.variaveis()


        self.cursor.execute(""" INSERT INTO clientes (nome_cliente,telefone,cidade) VALUES (?,?,?) """,
                            (self.nome,self.telefone,self.cidade))
        self.conn.commit()

        self.desconectar_bd()
        self.select_lista()
        self.limpar_tela()
    def select_lista(self):
        self.listacli.delete(*self.listacli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listacli.insert("",END, values=i)
        self.desconectar_bd()
    def onDoubleClick(self, event):
        self.limpar_tela()
        self.listacli.selection()

        for n in self.listacli.selection():
            col1, col2,col3,col4 = self.listacli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""",(self.codigo))
        self.conn.commit()

        self.desconectar_bd()
        self.limpar_tela()
        self.select_lista()
    def alterar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.conn.execute(""" UPDATE clientes SET nome_cliente= ?,telefone= ?,cidade= ? WHERE cod = ?""",
                          (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpar_tela()
    def buscar_cliente(self):
        self.conecta_bd()
        self.variaveis()
        if self.codigo:
            self.cursor.execute("""SELECT * FROM clientes WHERE cod= ?""",
                                (self.codigo))
            cliente = self.cursor.fetchone()
            if cliente:
                self.nome_entry.delete(0, "end")
                self.nome_entry.insert(0, cliente[1])

                self.telefone_entry.delete(0, "end")
                self.telefone_entry.insert(0, cliente[2])

                self.cidade_entry.delete(0, "end")
                self.cidade_entry.insert(0, cliente[3])
            else:
                print("CLIENTE NÃO ENCONTRADO")

        self.desconectar_bd()

#criando classse de aplicações
class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        mainloop()
    def tela (self):
        self.root.title("Cadastro de Clientes")  #titulo da janela
        self.root.configure(background='#1e3743')  #define a cor de fundo
        self.root.geometry('788x588') #define o tamanho da janela
        self.root.resizable(True, True)  #permite redimensionamento
        self.root.maxsize(width=988, height=788 ) #tamanho maximo
        self.root.minsize(width=500, height=400 ) #tamanho minimo
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd= 4, bg='#dfe3ee',
                             highlightbackground='#759fe6',highlightthickness= 3)
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46 )

        self.frame_2 = Frame(self.root, bd= 4, bg='#dfe3ee',
                             highlightbackground='#759fe6',highlightthickness= 3)
        self.frame_2.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46 )
    def widgets_frame1(self):
        ### criando o botão de limpar
        ### text= aqui vai o nome do botão, bd= expessura da borda, bg= cor da borda,
        ###fg= cor da letra,font = como ja diz vai detalhes da fonte
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=3, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command= self.limpar_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15, )
        ### criando o botão de buscar
        self.bt_buscar = Button(self.frame_1, text= "Buscar", bd=3, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.buscar_cliente)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        ### criando o botão de novo
        self.bt_novo = Button(self.frame_1, text= "Novo", bd=3, bg='#107db2', fg='white',
                              font=('verdana', 8, 'bold',), command= self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        ### criando o botão de alterar
        self.bt_alterar = Button(self.frame_1, text= "Alterar", bd=3, bg='#107db2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.alterar_cliente)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        ### criando o botão de apagar
        self.bt_apagar = Button(self.frame_1, text= "Apagar", bd=3, bg='#107db2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        ##Criando label e entrada código
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold') )
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.05, rely=0.15, relwidth=0.07)

        ##Criando label e entrada Nome
        self.lb_nome = Label(self.frame_1, text='Nome', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.7)

        ##Criando label e entrada Telefone
        self.lb_telefone = Label(self.frame_1, text='Telefone', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.05, rely=0.7, relwidth=0.4)

        ##Criando label e entrada Cidade
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely=0.7, relwidth=0.4)
    def lista_frame2(self):
        self.listacli = ttk.Treeview(self.frame_2, height=3, columns=('col1', 'col2', 'col3', 'col4'))
        self.listacli.heading('#0', text="")
        self.listacli.heading('#1', text="Código")
        self.listacli.heading('#2', text="Nome")
        self.listacli.heading('#3', text="Telefone")
        self.listacli.heading('#4', text="Cidade")

        self.listacli.column('#0', width=1)
        self.listacli.column('#1', width=50)
        self.listacli.column('#2', width=200)
        self.listacli.column('#3', width=125)
        self.listacli.column('#4', width=125)

        self.listacli.place(relx= 0.01, rely= 0.1, relwidth= 0.95, relheight= 0.85)

        self.escroollista = Scrollbar(self.frame_2, orient='vertical')
        self.listacli.configure(yscrollcommand= self.escroollista.set)
        self.escroollista.place(relx= 0.96, rely= 0.1, relwidth= 0.04, relheight=0.85)
        self.listacli.bind("<Double-1>",self.onDoubleClick)




Application ()