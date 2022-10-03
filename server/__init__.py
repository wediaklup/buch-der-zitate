from flask import Flask, jsonify, render_template, request, redirect, flash, url_for
import os
from datetime import datetime, date
import socket

# Definition der wichtigen Socket-Variablen
SOCKET_SERVER = "194.233.175.193"
SOCKET_PORT = 9807
FRMT = "utf-8"

# Objektdefinitionen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app = Flask(__name__) # "Definition" der Website
app.config['SECRET_KEY'] = "secretkey123"

@app.route("/")
def home():
        return redirect("/boq")

@app.route("/boq")
def boq():
        def read():
                """Liest alle Zitate aus der Datei und konvertiert sie in ein dict"""
                quotes = {}
                name = None
                with open(f"/root/qe-flask/dicts.dat", "r") as f:
                    line = f.readline()
                    length = len(line)

                    while length > 0:
                        print(f"{line = }")
                        print(f"{length = }")
                        
                        # Feststellen, ob die gelesene Zeile
                        # ein Namensheader oder eine Zitateliste ist
                        if line[0] == "&":
                                name = line[1:-1]

                        else:
                                qt = line.strip("\n")
                                quotes[name] = eval(qt)
                                print(f"{qt = }")
                                print(f"{quotes[name] = }")

                        line = f.readline()
                        length = len(line)

                print(quotes)

                return quotes


        def html_format(dictionary):
                
                now = datetime.now()
                jetzt = now.strftime("%H:%M:%S")
                heute = date.today()

                html = ""
                for name in dictionary:
                        print(name)
                        html += f'<h2 class="nomarg">{name}</h2>'
                        html += f"<ol>"
                        for qts in dictionary[name]:
                                print(qts)
                                html += f"<li>{qts}</li>"
                        html += f"</ol><br>"

                #with open("testausgabe.html", "w") as f:
                #    f.write(html)
                
                print(html)
                
                return html

        html = html_format(read())
        return render_template("root.html", data=html)


@app.route("/boq/submit", methods=["GET", "POST"])
def boqsubmit():
        if request.method == "POST":
                req = request.form
                
                clnt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clnt.connect((SOCKET_SERVER, SOCKET_PORT))
                header = "NEW+".encode(FRMT)
                clnt.send(header)

                name = req['name']
                quote = req['quote']
                name_capt = req['name_capt']
                quote_capt = req['quote_capt']

                to_send = {'name': name.upper(), 'quote': quote, 'name_capt': name_capt, 'quote_capt': quote_capt}
                clnt.send(str(to_send).encode(FRMT))
                flash("Die Anfrage wird bearbeitet")

                return redirect(request.url)

        return render_template("neu.html")


@app.route("/is/this/a/virus/<name>")
def isThisAVirus(name):
	return "<script>while (true) {alert('" + name + "');}</script>"


@app.route("/is/this/a/python", methods=["GET", "POST"])
def isThisAPython():
	template = """<form action="/is/this/a/python" method="POST"><font name="out">APython V.0.0.2{d}<br></font><br><input type="text" name="inp"><br></input><button type="submit">Enter</button></form>"""
	if request.method == "POST":
		d = request.form["out"]
		#d = data
		#txt = request.form["inp"]
		#d += "<br>"
		#d += txt
		return redirect("/is/this/a/virus/" + d)
		#return redirect("/is/this/a/virus/nworld")
		#return redirect(request.url)
		#return request.form["name"]
		#return "It IS APython but that does'nt mean it works"
		#return template.format(d=txt)
	return template.format(d="")


@app.route("/defaultsite")
def defaultsite():
	return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
