from flask import Flask, render_template_string, request
import requests
import feedparser

app = Flask(__name__)

rss_izvori = {
    "Zagrebačka": "https://www.realitica.com/rss/?cat=realestate&region=Zagrebačka&lang=hr",
    "Splitsko-dalmatinska": "https://www.realitica.com/rss/?cat=realestate&region=Splitsko-dalmatinska&lang=hr",
    "Zadarska": "https://www.realitica.com/rss/?cat=realestate&region=Zadarska&lang=hr",
    "Istarska": "https://www.realitica.com/rss/?cat=realestate&region=Istarska&lang=hr",
    "Primorsko-goranska": "https://www.realitica.com/rss/?cat=realestate&region=Primorsko-goranska&lang=hr",
    "Šibensko-kninska": "https://www.realitica.com/rss/?cat=realestate&region=Šibensko-kninska&lang=hr",
    "Dubrovačko-neretvanska": "https://www.realitica.com/rss/?cat=realestate&region=Dubrovačko-neretvanska&lang=hr"
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
      .error { color: red; margin-top: 1em; }
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

    {% if error %}
      <p class="error">{{ error }}</p>
    {% elif oglasi %}
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
    error = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        if feed_url:
            r = requests.get(feed_url, headers=headers, timeout=10)
            feed = feedparser.parse(r.content)
            if feed.bozo:
                error = "Greška pri učitavanju oglasa. RSS nije čitljiv."
            else:
                oglasi = feed.entries[:20]
    except Exception as e:
        error = f"Greška: {str(e)}"
    return render_template_string(html_template, oglasi=oglasi, rss_izvori=rss_izvori, odabrana_zupanija=odabrana_zupanija, error=error)

if __name__ == "__main__":
    app.run()
