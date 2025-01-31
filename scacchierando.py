# V11.0 del 2025.01.31 by IZ4APU and ChatGPT O1
import json
import os
from datetime import datetime
from GBUtils import key

DATA_FILE = "Scacchierando - registro_studenti.json"

def carica_dati():
	if os.path.exists(DATA_FILE):
		with open(DATA_FILE, "r") as file:
			return json.load(file)
	return {}

def salva_dati(dati):
	with open(DATA_FILE, "w") as file:
		json.dump(dati, file, indent=2)

def index_to_letter(index):
	"""
	Converte un indice 0-based in lettere stile Excel: 0 -> A, 1 -> B, ..., 25 -> Z, 26 -> AA, 27 -> AB, ...
	"""
	letters = []
	# Usiamo una logica di "base 26" con un leggero adattamento
	while True:
		# Prendiamo il 'resto' per determinare la lettera
		remainder = index % 26
		# Otteniamo il carattere ASCII corrispondente ad A + remainder
		letters.append(chr(remainder + ord('A')))
		index = index // 26
		if index == 0:
			break
		# Calcolo per continuare la conversione
		index -= 1
	letters.reverse()
	return "".join(letters)

def genera_report(dati):
	report_lines = []
	totale_studenti = len(dati)
	report_lines.append(f"# {datetime.now().strftime('%Y.%m.%d %H:%M:%S')} CLASSIFICHE DEGLI STUDENTI ({len(dati)}).")

	# --- Prime 4 classifiche inalterate ---
	classifiche = {
		"CLASSIFICA RISOLUTORI": sorted(dati.items(), key=lambda x: x[1]["Esercizi"]["totale"], reverse=True),
		"CLASSIFICA COLLABORATORI": sorted(dati.items(), key=lambda x: x[1]["Aiuto"]["totale"], reverse=True),
		"CLASSIFICA COMMENTATORI": sorted(dati.items(), key=lambda x: x[1]["Commenti"]["totale"], reverse=True),
		"CLASSIFICA PRESENZE ONLINE": sorted(dati.items(), key=lambda x: x[1]["Presenze online"]["totale"], reverse=True)
	}

	for titolo, classifica in classifiche.items():
		report_lines.append(f"\n## {titolo}.")
		report_lines.append("Pos.: (Valutazioni) Nome: Punti: Media:")
		for pos, (studente, dettagli) in enumerate(classifica, start=1):
			pos_str = f"{pos:2}"
			if titolo == "CLASSIFICA PRESENZE ONLINE":
				totale = dettagli["Presenze online"]["totale"]
				contatore = dettagli["Presenze online"]["valutazioni"]
			elif titolo == "CLASSIFICA RISOLUTORI":
				totale = dettagli["Esercizi"]["totale"]
				contatore = dettagli["Esercizi"]["valutazioni"]
			elif titolo == "CLASSIFICA COMMENTATORI":
				totale = dettagli["Commenti"]["totale"]
				contatore = dettagli["Commenti"]["valutazioni"]
			elif titolo == "CLASSIFICA COLLABORATORI":
				totale = dettagli["Aiuto"]["totale"]
				contatore = dettagli["Aiuto"]["valutazioni"]
			media = totale / contatore if contatore != 0 else 0
			report_lines.append(f"{pos_str}: ({contatore}) {studente}: {totale}: {media:.2f}")

	# --- 5a sezione: Note degli studenti ---
	report_lines.append("\n## NOTE DEGLI STUDENTI.\n")
	# Ordiniamo gli studenti in ordine alfabetico, 
	# oppure puoi lasciare items() liscio se vuoi l’ordine d’inserimento
	for i, (studente, dettagli) in enumerate(sorted(dati.items()), start=1):
		# Raccogliamo la stringa delle note
		note_str = dettagli.get("Note", "").strip()
		# Se l’utente ha accumulato note su più righe, le dividiamo
		# E ignoriamo eventuali righe vuote
		note_lines = [riga.strip() for riga in note_str.split("\n") if riga.strip()]

		# Intestazione: "1. NomeStudente"
		report_lines.append(f"{i}. {studente}")

		# Se non ci sono note, puoi decidere di non stampare nulla, oppure stampare un messaggio
		if not note_lines:
			continue

		# Stampa delle note con lettera maiuscola progressiva
		for j, nota in enumerate(note_lines):
			letter_label = index_to_letter(j)  # Converte j in A, B, C, ..., Z, AA, AB, ...
			report_lines.append(f"\t{letter_label}. {nota}")

	# Salviamo il report finale
	with open("e:/dropbox/scacchierando/Risorse e curiosità/Il giochino - Classifiche.txt", "w", encoding="utf-8") as file:
		file.write("\n".join(report_lines))

	print("Report generato: report_finale.txt")

def trova_corrispondenze(dati, nome):
	corrispondenze = [studente for studente in dati if nome.lower() in studente.lower()]
	return corrispondenze

def main():
	dati = carica_dati()
	print("Registro Studenti - CLI")
	print("Inserisci il nome dello studente oppure 'FINE' per terminare.")
	while True:
		nome = input("\nNome studente: ").strip().title()
		if nome.lower() == "fine":
			genera_report(dati)
			salva_dati(dati)
			print("Dati salvati e report generato. Uscita.")
			break

		corrispondenze = trova_corrispondenze(dati, nome)
		if len(corrispondenze) > 1:
			print(f"Corrispondenze trovate: {len(corrispondenze)}")
			for studente in corrispondenze:
				print(f"- {studente}")
			print("Specifica meglio il nome.")
			continue
		elif len(corrispondenze) == 1:
			print("Trovato studente:", corrispondenze[0])
			nome = corrispondenze[0]
		else:
			scelta = key(f"Studente {nome} non trovato. Lo aggiungo? s/n")
			if scelta == "s":
				dati[nome] = {
					"Presenze online": {"totale": 0, "valutazioni": 0},
					"Esercizi": {"totale": 0, "valutazioni": 0},
					"Commenti": {"totale": 0, "valutazioni": 0},
					"Aiuto": {"totale": 0, "valutazioni": 0},
					"Note": ""
				}
			else:
				print("Ok, non aggiungo nessuno.")
				continue

		print("Opzioni: [1] Presenze online, [2] Esercizi, [3] Commenti, [4] Aiuto agli altri, [5] Nota [0] Elimina")
		scelta = key("Seleziona l'opzione (1-2-3-4-5-0): ")
		if scelta in {"1", "2", "3", "4"}:
			while True:
				valore = key("Valore da aggiungere (-5 a 5): ")
				if valore == "-":
					valore2 = key("...meno? (1 a 5): ")
					valore = -int(valore2)
				else:
					valore = int(valore)
				if -5 <= valore <= 5:
					if scelta == "1":
						dati[nome]["Presenze online"]["totale"] += valore
						dati[nome]["Presenze online"]["valutazioni"] += 1
						print(f"\n{nome}, Presenze: val. {dati[nome]['Presenze online']['valutazioni']} = {dati[nome]['Presenze online']['totale']-valore} a {dati[nome]['Presenze online']['totale']}")
					elif scelta == "2":
						dati[nome]["Esercizi"]["totale"] += valore
						dati[nome]["Esercizi"]["valutazioni"] += 1
						print(f"\n{nome}, Esercizi: val. {dati[nome]['Esercizi']['valutazioni']} = {dati[nome]['Esercizi']['totale']-valore} a {dati[nome]['Esercizi']['totale']}")
					elif scelta == "3":
						dati[nome]["Commenti"]["totale"] += valore
						dati[nome]["Commenti"]["valutazioni"] += 1
						print(f"\n{nome}, Commenti: val. {dati[nome]['Commenti']['valutazioni']} = {dati[nome]['Commenti']['totale']-valore} a {dati[nome]['Commenti']['totale']}")
					elif scelta == "4":
						dati[nome]["Aiuto"]["totale"] += valore
						dati[nome]["Aiuto"]["valutazioni"] += 1
						print(f"\n{nome}, Aiuto: val. {dati[nome]['Aiuto']['valutazioni']} = {dati[nome]['Aiuto']['totale']-valore} a {dati[nome]['Aiuto']['totale']}")
					break
				else:
					print("\nValore non valido. Deve essere compreso tra -5 e 5.")
		elif scelta == "0":
			print(f"\nSei sicuro? Elimino {dati[nome]}?\ns/n")
			if key().lower() == "s":
				del dati[nome]
				print(f"\nStudente {nome} eliminato.")
			else:
				print("\nOk, non elimino nessuno")
		elif scelta == "5":
			nota = input("Inserisci la nota: ").strip()
			data_corrente = datetime.now().strftime("%Y.%m.%d")
			# Accodiamo la nota. Volendo si può strutturare diversamente,
			# ma qui continuiamo con la stessa logica
			dati[nome]["Note"] += f"\n    {data_corrente}: {nota} "
			print(f"\nStudente: {nome}, Note, {len(dati[nome]['Note'])}")
		else:
			print("\nScelta non valida. Riprova.")

if __name__ == "__main__":
	main()
