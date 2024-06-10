import os
import sys
import json
from datetime import date, datetime

def organize_csv_files(data_dir, date=None):
  """
  Organiza os arquivos CSV em pastas separadas

  Args:
    data_dir: Diretório contendo os dados
    date (opcional): Data no formato yyyy-mm-dd. Padrão: data atual.
  """
  # Busca o diretório .temp
  temp_dir = os.path.join(data_dir, ".temp")

  if not os.path.isdir(temp_dir):
    print(".temp directory doesn't exist.")
    return

  # Verifica a data
  if not date:
    date = datetime.today().strftime("%Y-%m-%d")
  try:
    datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    print(f"Formato da data inválido. Usar yyyy-mm-dd.")

  # Carrega ou cria csv_map.json
  csv_map_path = os.path.join(data_dir, "csv_map.json")
  csv_map = {}
  if os.path.isfile(csv_map_path):
    try:
      with open(csv_map_path, "r") as f:
        csv_map = json.load(f)
    except json.JSONDecodeError:
      print("Error loading csv_map.json. Creating a new one.")
  else:
    print("csv_map.json not found. Creating a new one.")

  # Processa cada subdiretório em .temp (que contém os dados separados por fonte -- CSV, Postgres, etc...)
  for subfolder in os.listdir(temp_dir):
    if not os.path.isdir(os.path.join(temp_dir, subfolder)):
      continue

    group = subfolder

    inner_temp_dir = os.path.join(temp_dir, subfolder)
    for filename in os.listdir(inner_temp_dir):
      if not filename.endswith(".csv"):
        continue

      # Extrai nome da entidade
      entity = os.path.splitext(filename)[0]
      csv_dir = os.path.join(data_dir, group, entity, date)

      # e cria diretório final, se não existir
      if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

      # Move o CSV para o diretório
      source_file = os.path.join(inner_temp_dir, filename)
      os.rename(source_file, os.path.join(csv_dir, filename))
      csv_map[entity] = { date: csv_dir.replace("\\", "/") }

  # Salva csv_map.json
  with open(csv_map_path, "w") as f:
    json.dump(csv_map, f, indent=4)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Correct usage: python organize_csv_files.py data_dir [date]")
    exit(1)

  data_dir = sys.argv[1]
  date = sys.argv[2] if len(sys.argv) > 3 else None

  organize_csv_files(data_dir, date)