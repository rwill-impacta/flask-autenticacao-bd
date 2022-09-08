class Aluno:

	def __init__(self, usuario, senha, nome, curso, data_inicio, media):
		self.usuario = usuario
		self.senha = senha
		self.nome = nome
		self.curso = curso
		self.data_inicio = data_inicio
		self.media = media
	
	@property
	def usuario(self):
		return self.__usuario
	
	@property
	def senha(self):
		return self.__senha
	
	@property
	def nome(self):
		return self.__nome
	
	@property
	def curso(self):
		return self.__curso
	
	@property
	def data_inicio(self):
		return self.__data_inicio
	
	@property
	def media(self):
		return self.__media

	@usuario.setter
	def usuario(self, valor):
		self.__usuario = valor
	
	@senha.setter
	def senha(self, valor):
		self.__senha = valor
	
	@nome.setter
	def nome(self, valor):
		self.__nome = valor
	
	@curso.setter
	def curso(self, valor):
		self.__curso = valor
	
	@data_inicio.setter
	def data_inicio(self, valor):
		self.__data_inicio = valor
	
	@media.setter
	def media(self, valor):
		self.__media = valor
