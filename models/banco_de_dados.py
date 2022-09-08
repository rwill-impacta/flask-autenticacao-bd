import sqlalchemy
import hashlib

if __name__ != '__main__':
	from .aluno import Aluno


class BancoDeDados:
	"""
	Classe que manipula um banco de dados sqlite, que contém uma tabela Aluno com os dados dos alunos.
	"""
	def __init__(self):
		self.__engine = sqlalchemy.create_engine('sqlite:///models/dados.db')
	

	def criar_tabelas(self):
		"""
		Cria o BD. Esse método só deve ser executado na etapa de configuração do sistema.
		"""
		connection = self.__engine.connect()
		connection.execute("""
			CREATE TABLE IF NOT EXISTS Aluno (
				usuario VARCHAR(50),
				senha VARCHAR(128) NOT NULL,
				nome VARCHAR(100) NOT NULL,
				curso VARCHAR(50),
				data_inicio DATE,
				media DECIMAL NOT NULL,
				CONSTRAINT ChP_ALUNO PRIMARY KEY(usuario)
			);
		""")
		connection.close()
	

	def inserir_aluno(self, obj_aluno):
		"""
		Insere uma nova linha no BD a partir de um objeto da classe Aluno.
		"""
		connection = self.__engine.connect()
		t = sqlalchemy.text("INSERT INTO Aluno VALUES (:usuario, :senha, :nome, :curso, :data_inicio, :media)")
		
		# A senha não deve ser guardada "crua" no BD. Portanto, vamos calcular o hash SHA-512 e armazenar este valor!
		senha_original = obj_aluno.senha
		hash_da_senha = hashlib.sha512(senha_original.encode('UTF-8')).hexdigest()
		
		connection.execute(t, usuario=obj_aluno.usuario, senha=hash_da_senha, nome=obj_aluno.nome, curso=obj_aluno.curso, data_inicio=obj_aluno.data_inicio, media=obj_aluno.media)
		connection.close()
	

	def listar_alunos(self):
		"""
		Retorna uma lista com objetos da classe Aluno, com todos os alunos existentes na tabela Aluno do BD
		"""
		connection = self.__engine.connect()
		alunos = []
		resultado = connection.execute("SELECT usuario, senha, nome, curso, data_inicio, media FROM Aluno ORDER BY usuario")
		for linha in resultado:
			usuario, senha, nome, curso, data_inicio, media = linha  # linha é uma tupla com todos esses campos, portanto podemos "descompacta-la" nessas 6 variáveis
			alu = Aluno(usuario, senha, nome, curso, data_inicio, media)  # criamos um objeto aluno com as variáveis
			alunos.append(alu)  # adicionamos o objeto à lista que será retornada pelo método
		connection.close()
		return alunos
	

	def obter_aluno(self, usuario):
		"""
			Retorna um objeto da classe Aluno, se o usuário existir. Caso contrário, retorna None.
		"""
		connection = self.__engine.connect()
		t = sqlalchemy.text("SELECT usuario, senha, nome, curso, data_inicio, media FROM Aluno WHERE usuario = :user")
		resultado = connection.execute(t, user=usuario)
		dado = resultado.fetchone()  # obtem o primeiro resultado (mas a nossa consulta sempre retornará no máximo 1 linha do BD)
		aluno = None
		if dado:  # se dado não é None, então:
			_, senha, nome, curso, data_inicio, media = dado
			aluno = Aluno(usuario, senha, nome, curso, data_inicio, media)
		connection.close()
		return aluno


if __name__ == '__main__':
	from aluno import Aluno
	print('O que deseja fazer?')
	print('   1- Criar tabelas e inserir dados no Banco de Dados')
	print('   2- Listar os dados gravados no Banco de Dados')
	opcao = int(input('Opcao: '))
	bd = BancoDeDados()
	if opcao == 1:
		bd.criar_tabelas()
		bd.inserir_aluno(Aluno('rafael', '1234', 'Rafael Will', 'Ciência da Computação', '01/02/2022', 7.5))
		bd.inserir_aluno(Aluno('maria', '4321', 'Maria dos Santos', 'Análise e Desenvolvimento de Sistemas', '11/08/2022', 8.6))
		bd.inserir_aluno(Aluno('jose', '9876', 'José Silva', 'Sistemas de Informação', '31/05/2022', 6.9))
		bd.inserir_aluno(Aluno('ana', '5678', 'Ana Beatriz', 'Engenharia da Computação', '05/10/2022', 9.2))
	else:
		lista = bd.listar_alunos()
		for aluno in lista:
			print('-'*80)
			print('Usuário:', aluno.usuario)
			print('Senha:', aluno.senha)
			print('Nome:', aluno.nome)
			print('Curso:', aluno.curso)
			print('Data início:', aluno.data_inicio)
			print('Média:', aluno.media)
