import json
import os
from datetime import datetime

class Scoreboard:
    def __init__(self, filepath="highscores.json"):
        self.filepath = filepath
        self.scores = self.load_scores()

    def load_scores(self):
        """Lê o arquivo JSON. Se não existir, retorna uma lista vazia."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []

    def save_score(self, new_score):
        """Adiciona a nova pontuação com a data atual, ordena e salva os 5 melhores."""
        if new_score <= 0:
            return # Evita salvar pontuações zeradas

        # Captura a data de hoje no formato DD/MM/AAAA
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        self.scores.append({"score": int(new_score), "date": current_date})
        
        # Ordena a lista do maior para o menor score
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        
        # Corta a lista para manter estritamente os 5 primeiros (Top 5)
        self.scores = self.scores[:5]
        
        # Grava de volta no arquivo
        with open(self.filepath, "w") as file:
            json.dump(self.scores, file, indent=4)