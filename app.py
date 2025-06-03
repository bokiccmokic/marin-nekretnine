from flask import Flask, render_template_string
import datetime

app = Flask(__name__)

# Dummy oglasi (može se proširiti scraperima)
oglasi = [
    {
        'naslov': 'Stan 60m² uz more - Zadar',
        'lokacija': 'Zadar',
        'cijena': '145.000 €',
        'link': 'https://www.realitica.com/hr/listing/123',
        'vrijeme': datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    },
    {
        'naslov': 'Kuća u Puli, 120m², novogradnja',
        'lokacija': 'Pula',
        'cijena': '220.000 €',
        'link': 'https://www.njuskalo.hr/nekretnine/456',
        'vrijeme': datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    }
]

html_template = """
<!doctype html>
<html lang="hr">
  <head>
    <meta charset="utf-8">
    <title>Marin Nekretnine</title>
    <style>
      body { font-family: Arial; background: #f5f5f5; padding: 2em; }
      .oglas { background: #fff; margin: 1em 0; padding: 1em; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
      a { text-decoration: none; color: #1a73e8; font-weight: bold; }
    </style>
  </head>
  <body>
    <h1>🏠 Marin Nekretnine – Novi oglasi</h1>
    {% for oglas in oglasi %}
      <div class="oglas">
        <a href="{{ oglas.link }}" target="_blank">{{ oglas.naslov }}</a><br>
        📍 {{ oglas.lokacija }}<br>
        💰 {{ oglas.cijena }}<br>
        🕒 <small>{{ oglas.vrijeme }}</small>
      </div>
    {% endfor %}
  </body>
</html>
"""

@app.route("/")
def prikaz_oglasa():
    return render_template_string(html_template, oglasi=oglasi)

if __name__ == "__main__":
    app.run()
