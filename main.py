#TODO colocar nome de arquivo para "OrganizePDF"

import customtkinter
from tkinter import END, Listbox
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import PyPDF2
import os
import json
from time import strftime

class Client_Label:
	def __init__(self ,master,frame , Nome, CadPessoa):
		self.master = master
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
		self.master.Clientes.pop(self.CadPessoa)

		#Salvando em banco permanente
		self.master.SalvarEmBancoClientes()

	def Editar(self):
		self.master.Bt_voltar_Cadastro.configure(state='disabled')
		self.master.Bt_AddAlterar.configure(text="Alterar",fg_color='red')

		self.master.EntryRSaCadastro.delete(0,"end")
		self.master.EntryRSaCadastro.insert(0,self.Nome)
		self.master.EntryCNPJCadastro.delete(0,"end")
		self.master.EntryCNPJCadastro.insert(0,self.CadPessoa)
		self.Deletar()

class GerenciadorCategorias(customtkinter.CTkFrame):
	def __init__(self, parent, voltarMenu_callback):
		super().__init__(parent)
		
		self.voltar_menu = voltarMenu_callback
		self.create_widgets()

	def create_widgets(self):
		# Componentes principais
		self.titulo = customtkinter.CTkLabel(self, text="Gerenciar Categorias e Subcategorias")  # Título
		self.label_categoria = customtkinter.CTkLabel(self, text="Categoria (Pasta):")  # LABEL CATEGORIA
		self.entrada_categoria = customtkinter.CTkEntry(self)  # ENTRY CATEGORIA
		self.label_subcategoria = customtkinter.CTkLabel(self, text="Subcategoria (PDF):")  # LABEL SUBCATEGORIA
		self.entrada_subcategoria = customtkinter.CTkEntry(self)  # ENTRY SUBCATEGORIA
		self.btn_add_categoria = customtkinter.CTkButton(self, text="+", command=self.adicionar_categoria, width=40)  # BT ADICIONAR CATEGORIA
		self.btn_add_subcategoria = customtkinter.CTkButton(self, text="+", command=self.adicionar_subcategoria, width=40)  # BT ADICIONAR SUBCATEGORIA
		self.btn_remover_categoria = customtkinter.CTkButton(self, text="-", command=self.remover_categoria, width=40)  # BT REMOVER CATEGORIA
		self.btn_remover_subcategoria = customtkinter.CTkButton(self, text="-", command=self.remover_subcategoria, width=40)  # BT REMOVER SUBCATEGORIA
		self.lista_categorias = Listbox(self, height=10, fg="black")  # LISTA DE CATEGORIAS
		self.lista_categorias.bind("<<ListboxSelect>>", self.mostrar_detalhes)  # Binding para exibir detalhes
		
		self.alerta = customtkinter.CTkLabel(self, text="FAVOR NÃO VOLTAR OU FECHAR A JANELA SEM SALVAR", text_color='red')  #ALERTA
		self.btn_voltar = customtkinter.CTkButton(self, text="Voltar", command=self.retornar_menu, width=40)#BT PRA SALVAR AND VOLTAR 
		
		self.Diretorio_Principal = ''
		self.Diretorio_Principal_label = customtkinter.CTkLabel(self,text=self.Diretorio_Principal ,textvariable=self.Diretorio_Principal)  # LABEL SUBCATEGORIA
		self.Selecionar_diretorio = customtkinter.CTkButton(self, text="Alterar Diretorio Padrão", command=self.Select_Diretorio)#BT PRA SALVAR AND VOLTAR 


		# Layout
		self.titulo.grid(row=0, column=1, columnspan=5, pady=10)  # TÍTULO
		self.label_categoria.grid(row=1, column=1, padx=10, pady=5)  # LABEL CATEGORIA
		self.entrada_categoria.grid(row=1, column=2, padx=10, pady=5, sticky="we")  # ENTRY CATEGORIA
		self.label_subcategoria.grid(row=2, column=1, padx=10, pady=5)  # LABEL SUBCATEGORIA
		self.entrada_subcategoria.grid(row=2, column=2, padx=10, pady=5,sticky="we")  # ENTRY SUBCATEGORIA
		self.btn_add_categoria.grid(row=1, column=5, padx=10, pady=10)  # BT ADICIONAR CATEGORIA
		self.btn_add_subcategoria.grid(row=2, column=5, padx=10, pady=10)  # BT ADICIONAR SUBCATEGORIA
		self.btn_remover_categoria.grid(row=1, column=6, padx=10, pady=10)  # BT REMOVER CATEGORIA
		self.btn_remover_subcategoria.grid(row=2, column=6, padx=10, pady=10)  # BT REMOVER SUBCATEGORIA
		self.lista_categorias.grid(row=3, column=1, columnspan=2, pady=10, sticky="nsew")  # LISTA CATEGORIAS
		self.alerta.grid(row=4, column=1,columnspan=4, padx=5,pady=5, sticky="nsew")  #ALERTA
		self.btn_voltar.grid(row=5, column=5, columnspan=6,sticky="ew",padx=5,pady=5)
		# Frame adicional à direita
		self.frame_detalhes = FrameDetalhes(self)
		self.frame_detalhes.grid(row=0, rowspan=4, column=0, padx=20, pady=10, sticky="nsew")

		self.Diretorio_Principal_label.grid(row=5, column=0, padx=20, pady=10, sticky="nsew")
		self.Selecionar_diretorio.grid(row=5, column=1, padx=20, pady=10, sticky="nsew")
		
		# Dicionário para armazenar as categorias e subcategorias
		self.categorias = {}
		self.carregar_dados()

	def Select_Diretorio(self):
		self.Diretorio_Principal = askdirectory()
		self.Diretorio_Principal_label.configure(text=self.Diretorio_Principal.split("/")[-1])
		self.salvar_dados()

	def retornar_menu(self):
		self.salvar_dados()
		self.voltar_menu()

	def carregar_dados(self):
		if os.path.exists('estrutura.json'):
			with open('estrutura.json', 'r') as file:
				self.categorias,self.Diretorio_Principal = json.load(file)
			self.Diretorio_Principal_label.configure(text=self.Diretorio_Principal.split("/")[-1])
			self.atualizar_lista()

	def salvar_dados(self):
		"""Salva as categorias e subcategorias em um arquivo JSON."""
		with open('estrutura.json', 'w') as file:
			json.dump([self.categorias,self.Diretorio_Principal], file, indent=4)

	def adicionar_categoria(self):
		nome_categoria = self.entrada_categoria.get()
		if nome_categoria:
			if nome_categoria not in self.categorias:
				self.categorias[nome_categoria] = {}  # Cada categoria contém um dicionário
				self.atualizar_lista()
				self.salvar_dados()
				self.carregar_dados()
			else:
				messagebox.showwarning("Aviso", "Essa categoria já existe.")
		else:
			messagebox.showerror("Erro", "O nome da categoria não pode estar vazio.")

	def adicionar_subcategoria(self):
		nome_categoria = self.entrada_categoria.get()
		nome_subcategoria = self.entrada_subcategoria.get()
		if nome_categoria and nome_subcategoria:
			if nome_categoria in self.categorias:
				if nome_subcategoria not in self.categorias[nome_categoria]:
					self.categorias[nome_categoria][nome_subcategoria] = []
					self.atualizar_lista()
					self.salvar_dados()
					self.carregar_dados()
					self.entrada_subcategoria.delete(0, "end")
				else:
					messagebox.showerror("Erro", "Essa SubCategoria Ja existe.")
			else:
				messagebox.showerror("Erro", "A categoria especificada não existe.")
		else:
			messagebox.showerror("Erro", "Os campos de categoria e subcategoria não podem estar vazios.")

	def remover_categoria(self):
		nome_categoria = self.entrada_categoria.get()
		if nome_categoria in self.categorias:
			del self.categorias[nome_categoria]
			self.atualizar_lista()
			self.salvar_dados()
			self.entrada_categoria.delete(0, "end")
			self.entrada_subcategoria.delete(0, "end")
		else:
			messagebox.showwarning("Aviso", "Categoria não encontrada.")

	def remover_subcategoria(self):
		nome_categoria = self.entrada_categoria.get()
		nome_subcategoria = self.entrada_subcategoria.get()
		if nome_categoria in self.categorias:
			if nome_subcategoria in self.categorias[nome_categoria]:
				del self.categorias[nome_categoria][nome_subcategoria]
				self.atualizar_lista()
				self.salvar_dados()
				self.entrada_subcategoria.delete(0, "end")
			else:
				messagebox.showwarning("Aviso", "Subcategoria não encontrada.")
		else:
			messagebox.showerror("Erro", "A categoria especificada não existe.")

	def atualizar_lista(self):
		"""Atualiza a exibição de categorias e subcategorias na listbox."""
		self.lista_categorias.delete(0, "end")
		for categoria, subcategorias in self.categorias.items():
			self.lista_categorias.insert("end", f"Categoria -- {categoria}")
			for sub, palavras_chave in subcategorias.items():
				self.lista_categorias.insert("end", f"  - {sub} ({len(palavras_chave)} palavras-chave)")

	def mostrar_detalhes(self, event):
		"""Exibe detalhes da subcategoria selecionada no FrameDetalhes."""
		selection = self.lista_categorias.curselection()
		if selection:
			texto_selecionado = self.lista_categorias.get(selection[0])
			if "Categoria -- " in texto_selecionado:
				categoria = texto_selecionado.split(" -- ")[1]
				self.frame_detalhes.mostrar_detalhes(categoria, None, self.categorias)
			
				self.entrada_categoria.delete(0,"end")
				self.entrada_categoria.insert("end",categoria)
				self.entrada_subcategoria.delete(0,"end")

			elif " - " in texto_selecionado:
				subcategoria = texto_selecionado.replace(" - ","").split("(")[0].strip()
				for key in self.categorias.keys():
					#obtendo categoria referente
					if subcategoria in self.categorias[key].keys():
						categoria = key
						break
				
				self.entrada_categoria.delete(0,"end")
				self.entrada_categoria.insert("end",categoria)
				
				self.entrada_subcategoria.delete(0,"end")
				self.entrada_subcategoria.insert("end",subcategoria)

				self.frame_detalhes.mostrar_detalhes(categoria, subcategoria, self.categorias)

class FrameDetalhes(customtkinter.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent)

		self.create_widgets()

	def create_widgets(self):
		self.label_detalhes = customtkinter.CTkLabel(self, text="Detalhes da Subcategoria")
		self.lista_palavras_chave = Listbox(self)
		self.label_Palavra = customtkinter.CTkLabel(self, text='Palavra-chave',fg_color='transparent')
		self.entrada_palavra_chave = customtkinter.CTkEntry(self, width=180)
		self.btn_add_palavra = customtkinter.CTkButton(self, text="Adicionar", command=self.adicionar_palavra_chave,width=70)
		self.btn_remover_palavra = customtkinter.CTkButton(self, text="Remover", command=self.
		remover_palavra_chave,width=70)
		
		self.lista_palavras_chave.bind("<<ListboxSelect>>", self.editar_palavra)
		
		self.label_detalhes.grid(row=0,column=0,columnspan=2,padx=10, pady=2)
		self.lista_palavras_chave.grid(row=1,column=0,columnspan=2,padx=5,sticky='nswe')
		self.label_Palavra.grid(row=2,column=0,columnspan=2)
		self.entrada_palavra_chave.grid(row=3,column=0,columnspan=2,pady=5,padx=4)
		self.btn_add_palavra.grid(row=4,column=0,pady=2)
		self.btn_remover_palavra.grid(row=4,column=1,pady=2)

	def mostrar_detalhes(self, categoria, subcategoria, categorias_dict):
		self.categoria = categoria
		self.subcategoria = subcategoria
		self.categorias_dict = categorias_dict

		# Limpa a lista de palavras-chave antes de exibir novas
		self.lista_palavras_chave.delete(0, "end")
		if subcategoria:
			palavras_chave = categorias_dict[categoria][subcategoria]
			for palavra in palavras_chave:
				self.lista_palavras_chave.insert("end", palavra)

	def editar_palavra(self,event):
		selecao_cursor = self.lista_palavras_chave.curselection()

		if len(selecao_cursor) >0:
			self.entrada_palavra_chave.delete(0, "end")

			self.entrada_palavra_chave.insert("end",self.lista_palavras_chave.get(selecao_cursor[0]))

	def adicionar_palavra_chave(self):
		palavra_chave = self.entrada_palavra_chave.get().upper()
		if palavra_chave and self.subcategoria:
			if palavra_chave not in self.categorias_dict[self.categoria][self.subcategoria]:
				self.categorias_dict[self.categoria][self.subcategoria].append(palavra_chave)
				
				self.lista_palavras_chave.insert("end", palavra_chave)
				self.master.salvar_dados()
				self.entrada_palavra_chave.delete(0, "end")
			else:
				messagebox.showwarning("Aviso", "Essa palavra-chave já existe.")
			self.master.atualizar_lista()

	def remover_palavra_chave(self):
		selecionado = self.lista_palavras_chave.curselection()
		if selecionado and self.subcategoria:
			palavra = self.lista_palavras_chave.get(selecionado)
			self.categorias_dict[self.categoria][self.subcategoria].remove(palavra)
			self.lista_palavras_chave.delete(selecionado)
			self.master.salvar_dados()
			self.master.atualizar_lista()

class MenuPrincipal(customtkinter.CTkFrame):
	def __init__(self, master, abrir_cadastro_callback, abrir_historico_callback, abrir_estruturacao_callback):
		super().__init__(master)
		self.abrir_cadastro_callback = abrir_cadastro_callback
		self.abrir_historico_callback = abrir_historico_callback
		self.abrir_Estruturacao_callback = abrir_estruturacao_callback
		'''if os.path.isfile('Historico.json'):
			with open('Historico.json', 'r', encoding='utf-8') as arq:
				self.Historico = json.load(arq)
				arq.close()
		else:
			self.Historico = {f"{strftime("%d/%m/%Y")}": ["Exemplo Historico"]}
			with open('Historico.json', 'w', encoding='utf-8') as arq:
				json.dump("{}", arq)'''
		

		self.create_widgets()

	def create_widgets(self):
	
		self.leftFrameMenu = customtkinter.CTkFrame(self, corner_radius=0)
		self.rightFrameMenu = customtkinter.CTkFrame(self)
		
		self.leftFrameMenu.grid(row=0, sticky="N")
		self.rightFrameMenu.grid(row=0, column=1)
		
		# Botões do menu
		self.Bt_cadastro = customtkinter.CTkButton(self.leftFrameMenu, text="Cadastro", command=self.abrir_cadastro_callback)
		self.Bt_historico = customtkinter.CTkButton(self.leftFrameMenu, text="Histórico", command=self.abrir_historico_callback)
		self.Bt_Estruturacao = customtkinter.CTkButton(self.leftFrameMenu, text="Estruturação", command=self.abrir_Estruturacao_callback,fg_color="red")
		self.Bt_organizar = customtkinter.CTkButton(self.leftFrameMenu, text="Organizar", command=self.organizar,fg_color="green")
		
		self.Bt_cadastro.grid(row=0, padx=10, pady=10)
		self.Bt_historico.grid(row=1, padx=10, pady=10)
		self.Bt_Estruturacao.grid(row=2, padx=10, pady=10)
		self.Bt_organizar.grid(row=3, padx=10, pady=10)

		# Listbox e barra de progresso
		self.progressbar = customtkinter.CTkProgressBar(self.rightFrameMenu, progress_color="#0ACF00", orientation='horizontal')
		self.listbox = Listbox(self.rightFrameMenu, width=150, height=15)
		
		self.progressbar.pack(padx=10, pady=10,fill='x', expand=1)
		self.listbox.pack(padx=10, pady=10)

	def organizar(self):
		self.Diretorio = askdirectory()
		self.PdfProcessados = {}
		self.PdfNaoReconhecidos = {}		

		tipos_documento = {
					"BOLETO BENEFICIO SOCIAL": ["Beneficio Social Familiar"],
					"FGTS Digital": ["GFD", "Guia do FGTS Digital"],
					"Simples Nacional": ["Simples Nacional"],
					"RECEITA FEDERAIS": ["Receitas Federais"],
					"ICMS": ["ICMS", "ICMS - ANTECIPACAO PARCIAL"],

					# Adicione mais tipos e palavras-chave conforme necessário
				}

		if self.Diretorio != "":
			tmparquivos = [f for f in os.listdir(self.Diretorio) if os.path.isfile(os.path.join(self.Diretorio, f))]
			arquivos = [f for f in tmparquivos if ".pdf" in f]
			print(arquivos)
			if len(arquivos) != 0:
				# Loop para percorrer diretórios e subdiretórios
				if os.path.exists('estrutura.json'):
					with open('estrutura.json', 'r') as file:
						self.estrutura,self.Diretorio_Principal = json.load(file)	
				else:
					messagebox.showwarning("Alerta","Antes de prosseguir crie a estrutura")
					return

				if os.path.isfile('Clientes.json'):
					with open('Clientes.json', 'r', encoding='utf-8') as arq:
						self.clientes = json.load(arq)
				else:
					messagebox.showwarning("Alerta","Antes de prosseguir cadastre os clientes")
					return

				for arq in arquivos:
					tmpDiretorio = self.Diretorio + "/" + arq
					print(f"Analisando PDF: {tmpDiretorio}")
					# Tentar abrir e ler o PDF
					try:
						with open(tmpDiretorio, "rb") as pdf_file:
							pdf_reader = PyPDF2.PdfReader(pdf_file)
							texto = pdf_reader.pages[0].extract_text()
							pdf_file.close()
					except Exception as e:
						self.PdfNaoReconhecidos[arq] = {"Cliente":"","Doc Type":""}
						print(f"Erro ao processar o arquivo {arq}: {e}")
						continue
							
								
						# Identificar o cliente baseado no nome e cadastro unico
					cliente_identificado = ''
					for cad_pessoa, nome in self.clientes.items():
						if cad_pessoa in texto or nome in texto:
							cliente_identificado = nome
							print(f"Cliente identificado: {nome}")
							break
						elif cad_pessoa[0:10] in texto:
							cliente_identificado = nome
							print(f"Cliente identificado: {nome}")
							break

					# Identificar o tipo de documento com base nas palavras-chave
					tipo_documento_identificado = ''
					for tipo, keywords in tipos_documento.items():
						if any(keyword.lower() in texto.lower() for keyword in keywords):
							tipo_documento_identificado = tipo
							print(f"Tipo de documento identificado: {tipo}")
							break
					
					# Exibir o resultado da análise
					if cliente_identificado != '' and tipo_documento_identificado != '':
						print(f"Arquivo '{arq}' pertence ao cliente '{cliente_identificado}' e é do tipo '{tipo_documento_identificado}'")
						self.PdfProcessados[arq] = {"Cliente":cliente_identificado,"Doc Type":tipo_documento_identificado}
					elif tipo_documento_identificado == '':
						print(f"Arquivo '{arq}' pertence ao cliente '{cliente_identificado}', mas tipo de documento não identificado.")
						self.PdfNaoReconhecidos[arq] = {"Cliente":cliente_identificado,"Doc Type":""}
					else:
						print(f"Cliente não identificado para o arquivo '{arq}'.")
						self.PdfNaoReconhecidos[arq] = {"Cliente":"","Doc Type":tipo_documento_identificado}


				print("\033[H\033[2J")
				for chave in self.PdfProcessados:
					print(chave)
					print(self.PdfProcessados[chave])
				## Leitura Feita arquivos marcados

				if len(self.PdfNaoReconhecidos.keys()) >= 1:
					TextoTmp = "Os Seguintes Arquivos não foram reconhecidos devido a não reconhecimento de: "
					for arq in self.PdfNaoReconhecidos.keys():
						if self.PdfNaoReconhecidos[arq]["Cliente"] == "" and self.PdfNaoReconhecidos[arq]["Doc Type"] == "":
							TextoTmp = TextoTmp + f"\n{arq} - Tipo do arquivo , Cliente"

						elif self.PdfNaoReconhecidos[arq]["Cliente"] == "":
							TextoTmp = TextoTmp + f"\n{arq} - Cliente"

						elif self.PdfNaoReconhecidos[arq]["Doc Type"] == "":
							TextoTmp = TextoTmp + f"\n{arq} - Tipo do arquivo"

						else:
							TextoTmp = TextoTmp + f"\n{arq} - Erro no sistema"

					TextoTmp = TextoTmp+"\n\n\nDeseja Continuar?"
					Resposta = messagebox.askquestion("Atenção",TextoTmp)
					print(Resposta)

					if Resposta == "no":
						return
					

				for arq in self.PdfProcessados.keys():
					dirTypeDoc = self.PdfProcessados[arq]["Doc Type"]
					dirClient = self.PdfProcessados[arq]["Cliente"]
					tmpdirreferente = "".join(x for x in self.estrutura.keys() if self.PdfProcessados[arq]["Doc Type"] in self.estrutura[x])
					if os.path.exists(f"{self.Diretorio_Principal}/{tmpdirreferente}/{dirTypeDoc}/{dirClient}"):
							os.rename(self.Diretorio + "/" + arq,f"{self.Diretorio_Principal}/{tmpdirreferente}/{dirTypeDoc}/{dirClient}/{arq}")
					else:
						os.makedirs(f"{self.Diretorio_Principal}/{tmpdirreferente}/{dirTypeDoc}/{dirClient}")
						os.rename(self.Diretorio + "/" + arq,f"{self.Diretorio_Principal}/{tmpdirreferente}/{dirTypeDoc}/{dirClient}/{arq}")
						
					self.listbox.insert(END,f"{arq} Transferido para {self.Diretorio_Principal + "/" + arq}")
					self.master.update()
					self.master.update_idletasks()
				
				self.progressbar
				
			else:
				messagebox.showerror("Erro","Não há pdf's no diretorio selecionado")

class Cadastro(customtkinter.CTkFrame):
	def __init__(self, master, voltar_callback):
		super().__init__(master)
		self.voltar_callback = voltar_callback
		self.create_widgets()
		self.carregar_dados()
	
	def carregar_dados(self):
		if os.path.isfile('Clientes.json'):
			with open('Clientes.json', 'r', encoding='utf-8') as arq:
				self.Clientes = json.load(arq)
		else:
			with open('Clientes.json', 'w', encoding='utf-8') as arq:
				self.Clientes = {"12.345.678/0001-23": "CLIENTE EXEMPLO"}
				json.dump(self.Clientes,arq)
			return

	def create_widgets(self):
		self.leftFrameCadastro = customtkinter.CTkFrame(self, corner_radius=0, fg_color='transparent')
		self.rightFrameCadastro = customtkinter.CTkScrollableFrame(self, width=450, height=300)

		self.EntryFrameCadastro = customtkinter.CTkFrame(self.leftFrameCadastro, fg_color='#6B6B6B')
		self.LabelRS = customtkinter.CTkLabel(self.EntryFrameCadastro, text='Razão social')
		self.EntryRSaCadastro = customtkinter.CTkEntry(self.EntryFrameCadastro, width=300)
		self.LabelCNPJ = customtkinter.CTkLabel(self.EntryFrameCadastro, text='CNPJ-CPF')
		self.EntryCNPJCadastro = customtkinter.CTkEntry(self.EntryFrameCadastro, width=300,validate='key',validatecommand=(self.master.register(self.ValidEntrys), '%P'))
		self.Bt_AddAlterar = customtkinter.CTkButton(self.EntryFrameCadastro, text="Cadastrar", command=self.ModfCadastCliente, fg_color='green')
		self.Bt_voltar_Cadastro = customtkinter.CTkButton(self.leftFrameCadastro, text="Voltar", command=self.voltar_callback)

		self.EntryCNPJCadastro.bind("<KeyRelease>",self.AplicarCracteresESpeciaisEntry)

		self.leftFrameCadastro.pack(fill='y', side='left', expand=1, padx=10, pady=10)
		self.rightFrameCadastro.pack(padx=10, pady=10)
		self.EntryFrameCadastro.pack(side='top', fill='x', padx=5, pady=5)
		
		self.LabelRS.grid(row=0, column=0, padx=5, pady=(10, 2.5), sticky="w")
		self.EntryRSaCadastro.grid(row=0, column=1)
		self.LabelCNPJ.grid(row=1, column=0, padx=5, sticky="w")
		self.EntryCNPJCadastro.grid(row=1, column=1)	
		self.Bt_AddAlterar.grid(row=2, column=3, pady=5, padx=50)
		self.Bt_voltar_Cadastro.pack(anchor="w", side="bottom", padx=10, pady=10)

	def ModfCadastCliente(self):
		TmpNome = (self.EntryRSaCadastro.get()).upper().strip()
		TmpNumeroIdentificacao = (self.EntryCNPJCadastro.get()).strip()
		TmpNumero = self.EntryCNPJCadastro.get().replace(".", "").replace("-", "").replace("/", "")
		self.AplicarCracteresESpeciaisEntry(None)
		if self.Bt_voltar_Cadastro._state == 'disabled':
			self.Bt_voltar_Cadastro.configure(state='normal')
			self.Bt_AddAlterar.configure(text="Cadastrar",fg_color='green')

		if len(TmpNumero) == 14 or len(TmpNumero) == 11 :
			if TmpNumeroIdentificacao not in self.Clientes.keys():
				self.EntryRSaCadastro.delete(0,"end")
				self.EntryCNPJCadastro.delete(0,"end")
				#criando label na lista
				Client_Label(self,self.rightFrameCadastro,TmpNome,TmpNumeroIdentificacao)
				#Escrevendo no banco temporario
				self.Clientes[TmpNumeroIdentificacao] = TmpNome

				#Escrevendo no banco permanente
				self.SalvarEmBancoClientes()
			else:
				messagebox.showwarning("Alerta","Este Cnpj ja esta cadastrado")
		else:
			messagebox.showwarning("Alerta","Numeração de Cadastro incorreta, insira um CNPJ ou CPF")

	def SalvarEmBancoClientes(self):
		#Salvando permanentemente em Banco de dados de Clientes
		with open('Clientes.json','w',encoding='utf-8') as arq:
			json.dump(self.Clientes,arq)
			arq.close()
		
	def ListarClientes(self):
		#Mostrar todos os clientes
		if self.rightFrameCadastro.winfo_children().__len__() == 0:
			for Cliente in list(self.Clientes.keys()):
				Client_Label(self,self.rightFrameCadastro,self.Clientes[Cliente],Cliente)
			pass

	def ValidEntrys(self,new_value):##Validando entrada de numeros no entry do historico
		new_value = new_value.replace(".", "").replace("-", "").replace("/", "")
		if new_value.isdigit() or new_value == '':
			#Caso esteja na entry do CNPJ-CPF 
			if new_value.__len__() <= 14:
				return True
			else:
				return False
		else:
			return False
		
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
	# end def

class Historico(customtkinter.CTkFrame):
	def __init__(self, master, voltar_callback):
		super().__init__(master)
		self.voltar_callback = voltar_callback
		self.create_widgets()
		print(master.title())

	def create_widgets(self):
		self.leftFrameHisto = customtkinter.CTkFrame(self, corner_radius=0, fg_color='transparent')
		self.rightFrameHisto = customtkinter.CTkFrame(self)

		self.EntryFrameHisto = customtkinter.CTkFrame(self.leftFrameHisto, fg_color='#6B6B6B')
		
		self.LabelDt = customtkinter.CTkLabel(self.EntryFrameHisto, text='Data', anchor='center')
		self.LabelDia = customtkinter.CTkLabel(self.EntryFrameHisto, text='Dia')
		self.EntryDiaHistorico = customtkinter.CTkEntry(self.EntryFrameHisto, width=45,validate='key',validatecommand=(self.master.register(self.ValidEntrys), '%P'))
		self.LabelMes = customtkinter.CTkLabel(self.EntryFrameHisto, text='Mês')
		self.EntryMesHistorico = customtkinter.CTkEntry(self.EntryFrameHisto, width=45,validate='key',validatecommand=(self.master.register(self.ValidEntrys), '%P'))
		self.LabelAno = customtkinter.CTkLabel(self.EntryFrameHisto, text='Ano')
		self.EntryAnoHistorico = customtkinter.CTkEntry(self.EntryFrameHisto, width=45,validate='key',validatecommand=(self.master.register(self.ValidEntrys), '%P'))
		self.Bt_Pesquisar = customtkinter.CTkButton(self.EntryFrameHisto, text="Pesquisar",command=self.Pesq_Historico)
		self.Bt_voltar_Historico = customtkinter.CTkButton(self.leftFrameHisto, text="Voltar", command=self.voltar_callback)
		self.listbox_Historico = Listbox(self.rightFrameHisto, width=60, height=15)

		self.leftFrameHisto.pack(fill='y', side='left', expand=1, padx=10, pady=10)
		self.rightFrameHisto.pack(padx=10, pady=10)
		self.EntryFrameHisto.pack(side='top', fill='x', padx=5, pady=5, ipadx=5)
		
		self.LabelDt.pack()
		self.Bt_Pesquisar.pack(pady=5, side='bottom')
		self.LabelDia.pack(padx=5, side="left")
		self.EntryDiaHistorico.pack(side="left")
		self.LabelMes.pack(padx=5, side="left")
		self.EntryMesHistorico.pack(side="left")
		self.LabelAno.pack(padx=5, side="left")
		self.EntryAnoHistorico.pack(side="left")
		
		self.Bt_voltar_Historico.pack(side="bottom", padx=10, pady=10)
		self.listbox_Historico.pack()

	def Pesq_Historico():
		#TODO FUNÇÃO PARA BUSCAR DADOS NO HISTORICO CASO HAJA
		pass

	def ValidEntrys(self,new_value):
		if new_value.isdigit():
			match (self.master.focus_get().master):
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

class App:
	def __init__(self):
		self.janela = customtkinter.CTk()
		self.janela.title("Organizador de Diretórios")
		self.janela.resizable(False, False)

		self.frame_menu_principal = MenuPrincipal(self.janela, self.abrir_cadastro, self.abrir_historico,self.abrir_estruturacao)
		self.frame_cadastro = Cadastro(self.janela, self.voltar_menu)
		self.frame_historico = Historico(self.janela, self.voltar_menu)
		self.frame_estrutura = GerenciadorCategorias(self.janela, self.voltar_menu)

		self.frame_menu_principal.pack()


	def abrir_cadastro(self):
		self.frame_menu_principal.pack_forget()
		self.frame_cadastro.pack()
		self.frame_cadastro.ListarClientes()
		
	def abrir_historico(self):
		self.frame_menu_principal.pack_forget()
		self.frame_historico.pack()

	def abrir_estruturacao(self):
		self.frame_menu_principal.pack_forget()
		self.frame_estrutura.pack()
		pass


	def voltar_menu(self):
		self.frame_cadastro.pack_forget()
		self.frame_historico.pack_forget()
		self.frame_estrutura.pack_forget()
		self.frame_menu_principal.pack()

if __name__ == "__main__":
	app = App()
	app.janela.mainloop()
