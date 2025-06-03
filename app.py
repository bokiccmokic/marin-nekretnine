from flask import Flask, render_template_string, request
import feedparser
import html

app = Flask(__name__)

# Sve županije u Hrvatskoj i odgovarajući RSS linkovi s Realitice
rss_izvori = {
    "Zagrebačka": "https://www.realitica.com/rss/?cat=realestate&region=Zagrebačka&lang=hr",
    "Krapinsko-zagorska": "https://www.realitica.com/rss/?cat=realestate&region=Krapinsko-zagorska&lang=hr",
    "Sisačko-moslavačka": "https://www.realitica.com/rss/?cat=realestate&region=Sisačko-moslavačka&lang=hr",
    "Karlovačka": "https://www.realitica.com/rss/?cat=realestate&region=Karlovačka&lang=hr",
    "Varaždinska": "https://www.realitica.com/rss/?cat=realestate&region=Varaždinska&lang=hr",
    "Koprivničko-križevačka": "https://www.realitica.com/rss/?cat=realestate&region=Koprivničko-križevačka&lang=hr",
    "Bjelovarsko-bilogorska": "https://www.realitica.com/rss/?cat=realestate&region=Bjelovarsko-bilogorska&lang=hr",
    "Primorsko-goranska": "https://www.realitica.com/rss/?cat=realestate&region=Primorsko-goranska&lang=hr",
    "Ličko-senjska": "https://www.realitica.com/rss/?cat=realestate&region=Ličko-senjska&lang=hr",
    "Virovitičko-podravska": "https://www.realitica.com/rss/?cat=realestate&region=Virovitičko-podravska&lang=hr",
    "Požeško-slavonska": "https://www.realitica.com/rss/?cat=realestate&region=Požeško-slavonska&lang=hr",
    "Brodsko-posavska": "https://www.realitica.com/rss/?cat=realestate&region=Brodsko-posavska&lang=hr",
    "Zadarska": "https://www.realitica.com/rss/?cat=realestate&region=Zadarska&lang=hr",
    "Osječko-baranjska": "https://www.realitica.com/rss/?cat=realestate&region=Osječko-baranjska&lang=hr",
    "Šibensko-kninska": "https://www.realitica.com/rss/?cat=realestate&region=Šibensko-kninska&lang=hr",
    "Vukovarsko-srijemska": "https://www.realitica.com/rss/?cat=realestate&region=Vukovarsko-srijemska&lang=hr",
    "Splitsko-dalmatinska": "https://www.realitica.com/rss/?cat=realestate&region=Splitsko-dalmatinska&lang=hr",
    "Istarska": "https://www.realitica.com/rss/?cat=realestate&region=Istarska&lang=hr",
    "Dubrovačko-neretvanska": "https://www.realitica.com/rss/?cat=realestate&region=Dubrovačko-neretvanska&lang=hr",
    "Međimurska": "https://www.realitica.com/rss/?cat=realestate&region=Međimurska&lang=hr"
}

html_template = """
<!doctype html>
<html lang="hr">
  <head>
    <meta charset="utf-8">
    <title>Marin Nekretnine</title>
    <style>
      body { font-family: Arial; background: #f0f0f0; padding: 2em; }
      select, button { padding: 0.5em; font-size: 1em; margin-bottom: 1em; }
      .oglas { background: white; padding: 1em; margin-bottom: 1em; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
      a { text-decoration: none; color: #007bff; font-weight: bold; }
    </style>
  </head>
  <body>
    <h1>🏡 Marin Nekretnine</h1>
    <form method="get">
      <label for="zupanija">Odaberi županiju:</label>
      <select name="zupanija" id="zupanija">
        {% for zupanija in rss_izvori %}
          <option value="{{ zupanija }}" {% if zupanija == odabrana_zupanija %}selected{% endif %}>{{ zupanija }}</option>
        {% endfor %}
      </select>
      <button type="submit">Prikaži</button>
    </form>

    {% if oglasi %}
      <h2>Oglasi za {{ odabrana_zupanija }} županiju</h2>
      {% for oglas in oglasi %}
        <div class="oglas">
          <a href="{{ oglas.link }}" target="_blank">{{ oglas.title }}</a><br>
          <small>{{ oglas.published }}</small><br>
          {% if oglas.get("summary") %}<em>{{ oglas.summary|safe }}</em>{% endif %}
        </div>
      {% endfor %}
    {% else %}
      <p>Nema dostupnih oglasa za odabranu županiju.</p>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def prikaz_oglasa():
    odabrana_zupanija = request.args.get("zupanija", "Splitsko-dalmatinska")
    feed_url = rss_izvori.get(odabrana_zupanija)
    oglasi = []
    if feed_url:
        feed = feedparser.parse(feed_url)
        oglasi = feed.entries[:20]
    return render_template_string(html_template, oglasi=oglasi, rss_izvori=rss_izvori, odabrana_zupanija=odabrana_zupanija)

if __name__ == "__main__":
    app.run()
