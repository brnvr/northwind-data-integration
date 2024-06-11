import os
import sys
import json
from datetime import date, datetime

def generate_files_definition(data_dir, date=None):
  """
  Gera um arquivo "files-definition.json" com base no dicionário csv_map.json.

  Args:
      data_dir (str): Diretório dos dados
      date_str (str, optional): Data no formato YYYY-MM-DD. Padrão: data atual
  """

  # Valida data_dir
  if not os.path.isdir(data_dir):
    raise ValueError(f"Invalid data directory: {data_dir}")

  # Verifica a data
  if not date:
    date = datetime.today().strftime("%Y-%m-%d")
  try:
    datetime.strptime(date, "%Y-%m-%d")
  except ValueError:
    print(f"Formato da data inválido. Usar yyyy-mm-dd.")

  csv_map_path = os.path.join(data_dir, "csv_map.json")

  # Carrega o JSON do dicionário
  try:
    with open(csv_map_path, "r") as f:
      csv_map = json.load(f)
  except FileNotFoundError:
    raise FileNotFoundError(f"csv_map.json not found in {data_dir}")

  files_definition = []

  #popula o files_definition
  for entity in csv_map:
    try:
      entity_path = csv_map[entity][date]
    except KeyError:
      raise KeyError(f"Data from '{entity}' not extracted on {formatted_date}.json")

    files_definition.append({
      "entity": entity,
      "path": entity_path,
      "keys": [] 
    })

  temp_dir = os.path.join(data_dir, ".temp")
  os.makedirs(temp_dir, exist_ok=True)

  # Cria files_definition.json no diretório
  output_file_path = os.path.join(temp_dir, "files_definition.json")
  with open(output_file_path, "w") as f:
    json.dump(files_definition, f, indent=4)

  print(f"Generated files_definition.json in: {output_file_path}")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Correct usage: python generate_files_definition.py data_dir [date]")
    exit(1)

  data_dir = sys.argv[1]
  date = sys.argv[2] if len(sys.argv) > 2 else None

  if date == "TODAY":
    date = None

  generate_files_definition(data_dir, date)