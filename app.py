from flask import Flask, render_template_string, request
import feedparser

app = Flask(__name__)

# Gradovi i njihovi RSS feedovi s Realitice (primjeri)
rss_izvori = {
    "Split": "https://www.realitica.com/rss/?t=nekretnine_spl_hr",
    "Zadar": "https://www.realitica.com/rss/?t=nekretnine_zd_hr",
    "Rijeka": "https://www.realitica.com/rss/?t=nekretnine_ri_hr",
    "Pula": "https://www.realitica.com/rss/?t=nekretnine_pu_hr",
    "Šibenik": "https://www.realitica.com/rss/?t=nekretnine_si_hr",
    "Makarska": "https://www.realitica.com/rss/?t=nekretnine_mk_hr"
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
      <label for="grad">Odaberi grad:</label>
      <select name="grad" id="grad">
        {% for grad in rss_izvori %}
          <option value="{{ grad }}" {% if grad == odabrani_grad %}selected{% endif %}>{{ grad }}</option>
        {% endfor %}
      </select>
      <button type="submit">Prikaži</button>
    </form>

    {% if oglasi %}
      <h2>Oglasi za {{ odabrani_grad }}</h2>
      {% for oglas in oglasi %}
        <div class="oglas">
          <a href="{{ oglas.link }}" target="_blank">{{ oglas.title }}</a><br>
          <small>{{ oglas.published }}</small>
        </div>
      {% endfor %}
    {% else %}
      <p>Nema oglasa za odabrani grad.</p>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET"])
def prikaz_oglasa():
    odabrani_grad = request.args.get("grad", "Split")
    feed_url = rss_izvori.get(odabrani_grad)
    oglasi = []
    if feed_url:
        feed = feedparser.parse(feed_url)
        oglasi = feed.entries[:20]
    return render_template_string(html_template, oglasi=oglasi, rss_izvori=rss_izvori, odabrani_grad=odabrani_grad)

if __name__ == "__main__":
    app.run()
