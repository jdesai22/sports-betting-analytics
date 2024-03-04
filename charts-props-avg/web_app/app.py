from flask import Flask, render_template, request
from plot_player_data import plot_player_data_plotly

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    plot_div = None
    if request.method == "POST":
        player_name = request.form.get("player_name")
        plot_div = plot_player_data_plotly(player_name)
    return render_template("home.html", plot_div=plot_div)


if __name__ == "__main__":
    app.run(debug=True)
