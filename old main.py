import customtkinter
from tkinter import Listbox
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import PyPDF2 as PdfReader
import os
import os
import json
from time import strftime

print(strftime("%a %b %d %H:%M:%S %Y"))

class app :
	def __init__(self):
		self.janela = customtkinter.CTk()
		self.janela.title("Organizador Diretorios")
		self.janela.resizable(False, False)

		#Frames Janelas	
		'''self.frame_MnCadastro = customtkinter.CTkFrame(self.janela)
		
		
		self.frame_MnCadastro.grid(row=0)'''

		#Frame Menu Historico
		##frame

		self.Menu_principal()
		self.Historico()
		self.Cadastro()

		##Abrindo Banco de Dados

		####Verificando se existe o diretorio
		
		if os.path.isfile('Clientes.json'):
			with open('Clientes.json','r',encoding='utf-8') as arq:
				self.Clientes = json.load(arq)
				print(self.Clientes)
				arq.close()
		else:
			with open('Clientes.json','w',encoding='utf-8') as arq:
				json.dump(arq,{'CNPJ Exemplo':"Cliente Exemplo"})
				self.Clientes = {"CNPJ Exemplo":"Cliente Exemplo"}
				arq.close()

		self.janela.mainloop()

	def Cadastro(self):
		self.frame_MnCadastro = customtkinter.CTkFrame(self.janela)

			##Comnpontentes criação
		self.leftFrameCadastro = customtkinter.CTkFrame(self.frame_MnCadastro,corner_radius=0,fg_color='transparent')
		self.rightFrameCadastro = customtkinter.CTkScrollableFrame(self.frame_MnCadastro,width=450,height=300)

		self.EntryFrameCadastro = customtkinter.CTkFrame(self.leftFrameCadastro,fg_color='#6B6B6B')#
		self.LabelRS = customtkinter.CTkLabel(self.EntryFrameCadastro, text='Razão social')
		self.EntryRSaCadastro = customtkinter.CTkEntry(self.EntryFrameCadastro,width=300)
		self.LabelCNPJ = customtkinter.CTkLabel(self.EntryFrameCadastro, text='CNPJ-CPF')
		self.EntryCNPJCadastro = customtkinter.CTkEntry(self.EntryFrameCadastro,width=300,validate='key',validatecommand=(self.janela.register(self.ValidEntrys), '%P'))
		self.Bt_AddAlterar = customtkinter.CTkButton(self.EntryFrameCadastro, text="Adicionar",command=self.ModfCadastCliente,fg_color='green')

		self.EntryCNPJCadastro.bind("<KeyRelease>",self.AplicarCracteresESpeciaisEntry)

		self.Bt_voltar_Cadastro = customtkinter.CTkButton(self.leftFrameCadastro, text="voltar",command=self.Voltar)
		

			##Layout
		self.leftFrameCadastro.pack(fill='y',side='left',expand=1,padx=(10,0),pady=(10,10))
		self.rightFrameCadastro.pack(padx=(0,10),pady=(10,10))
		self.EntryFrameCadastro.pack(side='top',fill='x',padx=(5,5),pady=(5,5))##
		
		self.LabelRS.grid(row=0 , column =0, padx=(5,5),pady=(10,2.5),sticky="w")
		self.EntryRSaCadastro.grid(row=0, column =1)
		self.LabelCNPJ.grid(row=1, column =0,padx=(5,5),sticky="w")
		self.EntryCNPJCadastro.grid(row=1, column=1)
		self.Bt_AddAlterar.grid(row=2 , column=3, pady=(5,5),padx=(50,5))

		self.Bt_voltar_Cadastro.pack(anchor="w",side="bottom",padx=(10,10),pady=(10,10))
		self.listbox_Historico.pack()

	def Historico(self):
		self.frame_MnHistorico = customtkinter.CTkFrame(self.janela)

			##Comnpontentes criação
		self.leftFrameHisto = customtkinter.CTkFrame(self.frame_MnHistorico,corner_radius=0,fg_color='transparent')
		self.rightFrameHisto = customtkinter.CTkFrame(self.frame_MnHistorico)

		self.EntryFrameHisto = customtkinter.CTkFrame(self.leftFrameHisto,fg_color='#6B6B6B')##
		self.LabelDt = customtkinter.CTkLabel(self.EntryFrameHisto, text='Data', anchor='center')
		self.LabelDia = customtkinter.CTkLabel(self.EntryFrameHisto, text='Dia')
		self.EntryDiaHistorico = customtkinter.CTkEntry(self.EntryFrameHisto,width=45,validate='key',validatecommand=(self.janela.register(self.ValidEntrys), '%P'))
		self.LabelMes = customtkinter.CTkLabel(self.EntryFrameHisto, text='Mês')
		self.EntryMesHistorico = customtkinter.CTkEntry(self.EntryFrameHisto,width=45,validate='key',validatecommand=(self.janela.register(self.ValidEntrys), '%P'))
		self.LabelAno = customtkinter.CTkLabel(self.EntryFrameHisto, text='Ano')
		self.EntryAnoHistorico = customtkinter.CTkEntry(self.EntryFrameHisto,width=45,validate='key',validatecommand=(self.janela.register(self.ValidEntrys), '%P'))
		self.Bt_Pesquisar = customtkinter.CTkButton(self.EntryFrameHisto,text="pesquisar")

		
		self.listbox_Historico = Listbox(self.rightFrameHisto,width=60,height=15)
		self.Bt_voltar_Historico = customtkinter.CTkButton(self.leftFrameHisto, text="voltar",command=self.Voltar)
		

			##Layout
		self.leftFrameHisto.pack(fill='y',side='left',expand=1,padx=(10,0),pady=(10,10))
		self.rightFrameHisto.pack(padx=(0,10),pady=(10,10))
		self.EntryFrameHisto.pack(side='top',fill='x',padx=(5,5),pady=(5,5),ipadx=5)##
		
		self.LabelDt.pack()
		self.Bt_Pesquisar.pack(pady=(5,5),side='bottom')
		self.LabelDia.pack(padx=(5,2),side="left")
		self.EntryDiaHistorico.pack(side="left")
		self.LabelMes.pack(padx=(5,2),side="left")
		self.EntryMesHistorico.pack(side="left")
		self.LabelAno.pack(padx=(5,2),side="left")
		self.EntryAnoHistorico.pack(side="left")

		self.Bt_voltar_Historico.pack(side="bottom",padx=(10,10),pady=(10,10))
		self.listbox_Historico.pack()

	def Menu_principal(self):

		#Frame Menu Principal
		self.frameMenu = customtkinter.CTkFrame(self.janela,corner_radius=0)
		self.frameMenu.pack()
		##Frame
		self.leftFrameMenu = customtkinter.CTkFrame(self.frameMenu,corner_radius=0)
		self.rightFrameMenu = customtkinter.CTkFrame(self.frameMenu)		
		self.leftFrameMenu.grid(row=0,sticky="N")
		self.rightFrameMenu.grid(row=0,column=1)
		##Comnpontentes criação
		self.Bt_cadsatro = customtkinter.CTkButton(self.leftFrameMenu, text="Cadastro",command=self.AbrirCadastro)
		self.Bt_historico = customtkinter.CTkButton(self.leftFrameMenu, text='Historico',command=self.AbrirHistorico)
		self.Bt_Organizar = customtkinter.CTkButton(self.leftFrameMenu, text='Organizar',command=self.Organizar)
		self.progressbar = customtkinter.CTkProgressBar(self.rightFrameMenu,progress_color="#0ACF00", orientation='horizontal',width=350)
		self.listbox = Listbox(self.rightFrameMenu,width=60,height=15)
		##Layout
		self.Bt_cadsatro.grid(row=0,padx=(10,10),pady=(10,10))
		self.Bt_historico.grid(row=1,padx=(10,10),pady=(10,10))
		self.Bt_Organizar.grid(row=2,padx=(10,10),pady=(10,10))
		self.progressbar.pack(padx=(10,10),pady=(10,10),expand=1)
		self.listbox.pack(padx=(10,10),pady=(10,10))

	def Organizar(self):
		self.Diretorio = askdirectory()

		if self.Diretorio == '':
			return

	def SalvarEmBancoClientes(self):
		#Salvando permanentemente em Banco de dados de Clientes
		with open('Clientes.json','w',encoding='utf-8') as arq:
			json.dump(self.Clientes,arq)
			arq.close()

	def ModfCadastCliente(self):
		TmpNome = (self.EntryRSaCadastro.get()).upper().strip()
		TmpNumeroIdentificacao = (self.EntryCNPJCadastro.get()).strip()


		if TmpNumeroIdentificacao not in self.Clientes.keys():
			self.EntryRSaCadastro.delete(0,"end")
			self.EntryCNPJCadastro.delete(0,"end")
			#criando label na lista
			self.Client_Label(self,self.rightFrameCadastro,TmpNome,TmpNumeroIdentificacao)
			#Escrevendo no banco temporario
			self.Clientes[TmpNumeroIdentificacao] = TmpNome

			#Escrevendo no banco permanente
			self.SalvarEmBancoClientes()
		else:
			messagebox.showwarning("Alerta","Este Cnpj ja esta cadastrado")

	def Voltar(self):
		self.janela.pack_slaves()[0].pack_forget()
		self.frameMenu.pack()

	def AbrirHistorico(self):
		self.frameMenu.pack_forget()
		self.frame_MnHistorico.pack()
	
	def AbrirCadastro(self):
		self.frameMenu.pack_forget()
		self.frame_MnCadastro.pack()

		

	def AplicarCracteresESpeciaisEntry(self,event):
		new_value = self.EntryCNPJCadastro.get().replace(".", "").replace("-", "").replace("/", "")

		if new_value.__len__() == 14: 
			self.EntryCNPJCadastro.delete(0,self.EntryCNPJCadastro.get().__len__())
			self.EntryCNPJCadastro.insert(0,f"{new_value[0:2]}.{new_value[2:5]}.{new_value[5:8]}/{new_value[8:12]}-{new_value[12:15]}")
		elif new_value.__len__() == 11:
			self.EntryCNPJCadastro.delete(0,self.EntryCNPJCadastro.get().__len__())
			self.EntryCNPJCadastro.insert(0,f"{new_value[0:3]}.{new_value[3:6]}.{new_value[6:9]}-{new_value[9:11]}")

		elif new_value.__len__() == 9 or new_value.__len__() == 12 or new_value.__len__() == 13 :
			self.EntryCNPJCadastro.delete(0,self.EntryCNPJCadastro.get().__len__())
			self.EntryCNPJCadastro.insert(0,new_value)
		else:
			pass

	def ValidEntrys(self,new_value):##Validando entrada de numeros no entry do historico
		if self.janela.focus_get().master == self.EntryCNPJCadastro:
			new_value = new_value.replace(".", "").replace("-", "").replace("/", "")
			if new_value.isdigit() or new_value == '':
				#Caso esteja na entry do CNPJ-CPF 
				if new_value.__len__() <= 14:
					return True
				else:
					return False

			return False
			
		elif new_value.isdigit():
			match (self.janela.focus_get().master):
				#switch em python 
				case self.EntryDiaHistorico:
					#Caso esteja na entry do Dia 
					if int(new_value) <= 31:
						return True
					else:
						return False
					
				case self.EntryMesHistorico:
					#Caso esteja na entry do Mes 
					if int(new_value) <= 12:
						return True
					else:
						return False
					
				case self.EntryAnoHistorico:
					#Caso esteja na entry do Ano 
					if int(new_value) <= int(strftime("%Y")):
						return True
					else:
						return False
					
				case _:
					return True
				
		elif new_value == '':
			return True
		else:
			return False
	
	class Client_Label:
		def __init__(self ,Class_Pai,frame , Nome, CadPessoa):
			self.Class_Pai = Class_Pai
			self.Nome = Nome
			self.CadPessoa = CadPessoa
			self.FramePai = frame
			self._Fundo = customtkinter.CTkFrame(frame,fg_color='gray')
			self._Lixeira = customtkinter.CTkButton(self._Fundo,text='X',width=25,command=self.Deletar)
			self._Editar = customtkinter.CTkButton(self._Fundo,text='Editar',width=50,command=self.Editar)
			self._Label = customtkinter.CTkLabel(self._Fundo, text=f'{CadPessoa} - {Nome}',wraplength=350, fg_color='transparent')

			self._Fundo.pack(side='top',fill='x',pady=(2,2),padx=(5,5))
			self._Lixeira.pack(side="left",pady=(4,4),padx=(5,1))
			self._Editar.pack(side="left",pady=(4,4),padx=(1,5))
			self._Label.pack(side="left",fill="x")
		
		def Deletar(self):
			#Apagando da lista do frameword
			self._Fundo.pack_forget()
			#Apagando da lista de clientes do banco temporario
			self.Class_Pai.Clientes.pop(self.CadPessoa)

			#Salvando em banco permanente
			self.Class_Pai.SalvarEmBancoClientes()

		def Editar(self):
			self.Class_Pai.Bt_voltar_Cadastro.configure(state='disabled')
			self.Class_Pai.Bt_AddAlterar.configure(text="Alterar",fg_color='red')

			self.Class_Pai.EntryRSaCadastro.delete(0,"end")
			self.Class_Pai.EntryRSaCadastro.insert(0,self.Nome)
			self.Class_Pai.EntryCNPJCadastro.delete(0,"end")
			self.Class_Pai.EntryCNPJCadastro.insert(0,self.CadPessoa)
			self.Deletar()
			pass






if __name__ == "__main__":
	App = app()
	App.janela.mainloop()
	
	
	pass