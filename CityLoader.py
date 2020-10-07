import csv
import codecs
import mysql.connector
import config
from unidecode import unidecode
from datetime import datetime

################################################################################
################################## IMPORTANT: ##################################
################################################################################
# in order to run this script you'll need to
# load the "municipios" and "secoes_{year}" dumps from the drive
# adjust the DB_CONF to connect to the database

class CityLoader:
	def __init__(self, city, state):
		self.db = mysql.connector.connect(
			host = config.host,
			user = config.user,
			passwd = config.password,
			db = config.db)
		self.cursor = self.db.cursor()
		self.city = city.lower()
		self.state = state.upper()
		self.cursor.execute(
			f"SELECT cod_tse, id FROM municipios WHERE nome = '{self.city}' AND uf = '{self.state}';")
		[(self.city_code_int, self.city_id_int)] = self.cursor.fetchall()
		self.start = datetime.now()
		self.city_code = str(self.city_code_int)
		self.city_id = str(self.city_id_int)
		self.dump = ''

	def __saveToFile(self):
		formatted_city_name = unidecode(self.city).replace(' ','_')
		file_name = f"dumps/{formatted_city_name}_{self.state}.sql"
		with codecs.open(file_name, 'w', 'utf8', errors='strict') as new_file:
			new_file.write(self.dump)

	def __getPath(self, table, year):
		folder_name = ""
		if table == "profiles":
			folder_name = "wider"
		elif table == "votes":
			folder_name = "votos"
		elif table == "candidates":
			folder_name == "candidatos"
		path = f"./{folder_name}/{folder_name}_{year}_{self.state}.csv"
		return path

	def __getTableName(self, table, year):
		table_name = ""
		if table == "profiles":
			table_name = f"perfis_{year}_sumario"
		if table == "votes":
			table_name = f"votos_{year}"
		if table == "candidates":
			table_name = f"candidatos_{year}"
		return table_name

	def __getTableColumn(self, table, year):
		table_column = ''
		if table == 'profiles':
			if ((year == 2016 or year == 2014) and self.state == "DF") or year < 2014:
				table_column = f"( municipio_id, secao_{year}_id, nao_informado_educ, analfabeto, le, fund_inc, fund_comp, med_incomp, med_comp, sup_incomp, sup_comp, nao_informado_id, dezesseis, dezessete, vinte, id2124, id3034, id4044, id5559, id6569, id7579, id9999, gen_outros, masculino, feminino, nao_informado_civil, solteiro, casado, viuvo, separado, divorciado, qt_eleitores_perfil)"
			else:
				table_column = f'( municipio_id, secao_{year}_id, nao_informado_educ, analfabeto, le, fund_inc, fund_comp, med_incomp, med_comp, sup_incomp, sup_comp, nao_informado_id, dezesseis, dezessete, dezoito, dezenove, vinte, id2124, id2529, id3034, id3539, id4044, id4549, id5054, id5559, id6064, id6569, id7074, id7579, id8084, id8589, id9094, id9599, id9999, gen_outros, masculino, feminino, nao_informado_civil, solteiro, casado, viuvo, separado, divorciado, qt_eleitores_perfil)'
		elif table == 'votes':
			table_column = f'( municipio_id, secao_{year}_id, turno, ds_cargo, nr_votavel, nm_candidato, qt_votos )'
		return table_column

	def __getCityIndex(self, table, year):
		if table == 'profiles':
			return -1
		if table == 'votes':
			if year == 2018:
				return 13
			if year <= 2016:
				return 3

	def __constructRow(self, row, table, year):
		new_row = ""
		fixed_row = [x if x != "NA" else "0" for x in row]
		if table == "profiles":
			if ((year == 2016 or year == 2014) and self.state == "DF") or year < 2013:
				self.cursor.execute(
					f"SELECT id FROM secoes_2016 WHERE municipio_id = '{self.city_id}' AND nr_zona = '{fixed_row[1]}' AND nr_secao = '{fixed_row[2]}';")
				try:
					[(secao_id,)] = self.cursor.fetchall()
					new_row = f"( '{self.city_id}', '{secao_id}', '{fixed_row[3]}', '{fixed_row[4]}', '{fixed_row[5]}', '{fixed_row[6]}', '{fixed_row[7]}', '{fixed_row[8]}', '{fixed_row[9]}', '{fixed_row[10]}', '{fixed_row[11]}', '{fixed_row[12]}', '{fixed_row[13]}', '{fixed_row[14]}', '{fixed_row[15]}', '{fixed_row[16]}', '{fixed_row[17]}', '{fixed_row[18]}', '{fixed_row[19]}', '{fixed_row[20]}', '{fixed_row[21]}', '{fixed_row[22]}', '{fixed_row[23]}', '{fixed_row[24]}', '{fixed_row[25]}', '{fixed_row[31]}', '{fixed_row[26]}', '{fixed_row[27]}', '{fixed_row[28]}', '{fixed_row[29]}', '{fixed_row[30]}', '{fixed_row[32]}')"
				except:
					new_row = f"( '{self.city_id}', NULL, '{fixed_row[3]}', '{fixed_row[4]}', '{fixed_row[5]}', '{fixed_row[6]}', '{fixed_row[7]}', '{fixed_row[8]}', '{fixed_row[9]}', '{fixed_row[10]}', '{fixed_row[11]}', '{fixed_row[12]}', '{fixed_row[13]}', '{fixed_row[14]}', '{fixed_row[15]}', '{fixed_row[16]}', '{fixed_row[17]}', '{fixed_row[18]}', '{fixed_row[19]}', '{fixed_row[20]}', '{fixed_row[21]}', '{fixed_row[22]}', '{fixed_row[23]}', '{fixed_row[24]}', '{fixed_row[25]}', '{fixed_row[31]}', '{fixed_row[26]}', '{fixed_row[27]}', '{fixed_row[28]}', '{fixed_row[29]}', '{fixed_row[30]}', '{fixed_row[32]}')"

			else:
				self.cursor.execute(
					f"SELECT id FROM secoes_{year} WHERE municipio_id = '{self.city_id}' AND nr_zona = '{fixed_row[1]}' AND nr_secao = '{fixed_row[2]}';")
				try:
					[(secao_id,)] = self.cursor.fetchall()
					remain = fixed_row[3:-1]
					new_row = f"('{self.city_id}', '{secao_id}', '{remain[0]}', '{remain[1]}', '{remain[2]}', '{remain[3]}', '{remain[4]}', '{remain[5]}', '{remain[6]}', '{remain[7]}', '{remain[8]}', '{remain[9]}', '{remain[10]}', '{remain[11]}', '{remain[12]}', '{remain[13]}', '{remain[14]}', '{remain[15]}', '{remain[16]}', '{remain[17]}', '{remain[18]}', '{remain[19]}', '{remain[20]}', '{remain[21]}', '{remain[22]}', '{remain[23]}', '{remain[24]}', '{remain[25]}', '{remain[26]}', '{remain[27]}', '{remain[28]}', '{remain[29]}', '{remain[30]}', '{remain[31]}', '{remain[32]}', '{remain[33]}', '{remain[34]}', '{remain[35]}', '{remain[36]}', '{remain[37]}', '{remain[38]}', '{remain[39]}', '{remain[40]}', '{remain[41]}')"
				except:
					remain = fixed_row[3:-1]
					new_row = f"('{self.city_id}', NULL, '{remain[0]}', '{remain[1]}', '{remain[2]}', '{remain[3]}', '{remain[4]}', '{remain[5]}', '{remain[6]}', '{remain[7]}', '{remain[8]}', '{remain[9]}', '{remain[10]}', '{remain[11]}', '{remain[12]}', '{remain[13]}', '{remain[14]}', '{remain[15]}', '{remain[16]}', '{remain[17]}', '{remain[18]}', '{remain[19]}', '{remain[20]}', '{remain[21]}', '{remain[22]}', '{remain[23]}', '{remain[24]}', '{remain[25]}', '{remain[26]}', '{remain[27]}', '{remain[28]}', '{remain[29]}', '{remain[30]}', '{remain[31]}', '{remain[32]}', '{remain[33]}', '{remain[34]}', '{remain[35]}', '{remain[36]}', '{remain[37]}', '{remain[38]}', '{remain[39]}', '{remain[40]}', '{remain[41]}')"
			
		if table == "votes":
			if year == 2018:
				self.cursor.execute(
					f"SELECT id FROM secoes_{year} WHERE municipio_id = '{self.city_id}' AND nr_zona = '{fixed_row[15]}' AND nr_secao = '{fixed_row[16]}';")
				[(secao_id,)] = self.cursor.fetchall()
				new_row = f"( '{self.city_id}', '{secao_id}', '{fixed_row[5]}', '{fixed_row[18]}', '{fixed_row[19]}', '{fixed_row[20]}', '{fixed_row[21]}' )"
			elif year <= 2016:
				self.cursor.execute(
					f"SELECT id FROM secoes_{year} WHERE municipio_id = '{self.city_id}' AND nr_zona = '{fixed_row[5]}' AND nr_secao = '{fixed_row[6]}';")
				try:
					[(secao_id,)] = self.cursor.fetchall()
					new_row = f"( '{self.city_id}', '{secao_id}', '{fixed_row[1]}', '{fixed_row[7]}', '{fixed_row[8]}', NULL, '{fixed_row[9]}' )"
				except:
					new_row = f"( '{self.city_id}', NULL, '{fixed_row[1]}', '{fixed_row[7]}', '{fixed_row[8]}', NULL, '{fixed_row[9]}' )"

		return new_row

	# complement votes table with the president votes
	# only works for presidential elections (2018 so far)
	def __dumpPresidentVotes(self, year):
		print(f"Dumping president votes {year}...")
		table_name = self.__getTableName('votes', year)
		table_column = self.__getTableColumn('votes', year)
		start = f"INSERT INTO {table_name} {table_column} VALUES "
		local_dump = f"LOCK TABLES {table_name} WRITE;\n\n" + start
		path = self.__getPath('votes', year).replace(self.state, 'BR')
		indexOfCityCode = self.__getCityIndex('votes', year)
		count = 0
		count_all = 0
		with codecs.open(path, encoding="utf-8", errors='strict') as csv_data:
			reader = csv.reader(csv_data, delimiter=';', quotechar='"')
			first = True
			local_dump_part = ""
			for row in reader:
				count_all += 1
				if row[indexOfCityCode] != self.city_code:  # skip if not the city
					continue
				count += 1
				# formatting sql
				if count % 5000 == 0:
					print(f"written lines: {count}, read lines: {count_all}")
					local_dump += local_dump_part
					local_dump_part = ""
				if count % 5000 == 0:
					local_dump_part += ';\n'
					local_dump_part += start
				else:
					if not first:
						local_dump_part += ",\n"
					if first:
						first = False

				local_dump_part += self.__constructRow(row, "votes", year)
			local_dump += local_dump_part
		# saving file

		local_dump += ";\n\nUNLOCK TABLES;\n\n"
		self.dump += local_dump
		print(f"Success in read file! table: votos, {year}, presidentes, {count} written lines, {count_all} read lines.")


	# receive year as integer and table definition as strong "votes"/"profiles"
	# and create the dump of the specified table
	def dumpSingle(self, year, table):
		startTime = datetime.now()
		print(f"Dumping {table} {year} {self.city}...")
		table_name = self.__getTableName(table, year)
		table_column = self.__getTableColumn(table, year)
		start = f"INSERT INTO {table_name} {table_column} VALUES "
		local_dump = f"LOCK TABLES {table_name} WRITE;\n\n" + start
		path = self.__getPath(table, year)
		indexOfCityCode = self.__getCityIndex(table, year)
		count = 0
		count_all = 0
		with codecs.open(path, encoding = "utf-8", errors='strict') as csv_data:
			reader = csv.reader(csv_data, delimiter=';', quotechar='"')
			first = True
			local_dump_part = ""
			for row in reader:
				count_all += 1
				if row[indexOfCityCode] != self.city_code:  # skip if not the city
					continue
				count += 1
				# splitting the string to improve the performance
				if count % 50000 == 0:
					local_dump += local_dump_part
					local_dump_part = ""
				# formatting sql
				if count % 5000 == 0:
					print(f"written lines: {count}, read lines: {count_all}")
					local_dump_part += ';\n'
					local_dump_part += start
				else:
					if not first:
						local_dump_part += ",\n"
					if first:
						first = False
				local_dump_part += self.__constructRow(row, table, year)

			# saving file
			local_dump += local_dump_part
			local_dump += ";\n\nUNLOCK TABLES;\n\n"
			if table == "profiles":
				local_dump += f"INSERT INTO perfis_{year}_municipio(municipio_id,nao_informado_educ,analfabeto,le,fund_inc,fund_comp,med_incomp,med_comp,sup_incomp,sup_comp,nao_informado_id,dezesseis,dezessete,dezoito,dezenove,vinte,id2124,id2529,id3034,id3539,id4044,id4549,id5054,id5559,id6064,id6569,id7074,id7579,id8084,id8589,id9094,id9599,id9999,feminino,gen_outros,masculino,casado,divorciado,nao_informado_civil,separado,solteiro,viuvo) SELECT municipio_id, SUM(nao_informado_educ), SUM(analfabeto), SUM(le), SUM(fund_inc), SUM(fund_comp), SUM(med_incomp), SUM(med_comp), SUM(sup_incomp), SUM(sup_comp), SUM(nao_informado_id), SUM(dezesseis), SUM(dezessete), SUM(dezoito), SUM(dezenove), SUM(vinte), SUM(id2124), SUM(id2529), SUM(id3034), SUM(id3539), SUM(id4044), SUM(id4549), SUM(id5054), SUM(id5559), SUM(id6064), SUM(id6569), SUM(id7074), SUM(id7579), SUM(id8084), SUM(id8589), SUM(id9094), SUM(id9599), SUM(id9999), SUM(feminino), SUM(gen_outros), SUM(masculino), SUM(casado), SUM(divorciado), SUM(nao_informado_civil), SUM(separado), SUM(solteiro), SUM(viuvo) FROM perfis_2018_sumario WHERE municipio_id = {self.city_id};\n\n"
			self.dump += local_dump
			finish = datetime.now()
			time_spent = finish - startTime
			print(f"Success in read file! table: {table}, {year}, {count} written lines, {count_all} read lines.")
			print(f"Time spent: {time_spent}")
			if table == "votes" and (year == 2014 or year ==2018):
				self.__dumpPresidentVotes(year)

	# dump profiles tables of all years
	def dumpProfilesSumary(self):
		print("Dumping profiles")
		self.dumpSingle(2018, "profiles")
		self.dumpSingle(2016, "profiles")
		self.dumpSingle(2014, "profiles")
		self.dumpSingle(2012, "profiles")

	# dump votes tables of all years
	def dumpVotes(self):
		print("Dumping votes...")
		self.dumpSingle(2018, "votes")
		self.dumpSingle(2014, "votes")
		if self.state != "DF":
			self.dumpSingle(2016, "votes")
			self.dumpSingle(2012, "votes")

	# dump by year
	def dumpYear(self, year):
		print(f"Dumping {self.city} year {year}...")
		self.dumpSingle(year, "profiles")
		if year == 2018 or year == 2016 or self.state != "DF":
			self.dumpSingle(year, "votes")

	# dump everything possible from the city
	def dumpCity(self):
		print(f"Dumping {self.city}...")
		self.dumpProfilesSumary()
		self.dumpVotes()

	# save the file and close the db connection
	def finish(self):
		finish = datetime.now()
		time = finish - self.start
		print(f"Finished dumping {self.city}, {self.state} in {time}")
		self.__saveToFile()
		self.cursor.close()
		self.db.close()

# how to use:
# create a new instance of the loader
# with the city name in lower case with graphic signals
# and the state initials in upper case
loader = CityLoader("rio de janeiro", "RJ")

# execute the method dumpCity() to create a file with the dump of all the tables
# loader.dumpCity()

# or execute the method dumpProfiles() or dumpVotes() to load all the respective
# tables of that city
# loader.dumpProfilesSumary()

# or execute the method dumpYear(year) to load all the tables from that year
# and city
# loader.dumpYear(2018)

# or execute the method dumpSingle(year, table) to load that specific table
loader.dumpSingle(2016, 'votes')


# finish() method save the file and close the conection with the database
loader.finish()
