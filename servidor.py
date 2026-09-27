import json  #YEISON
from http.server import BaseHTTPRequestHandler, HTTPServer

usuarios = []

class MiServidor(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/usuarios":
            texto = ""
            for usuario in usuarios:
                texto = texto + "Nombre: " + usuario["nombre"] + "\n"

            self.send_response(200)
            self.end_headers()
            self.wfile.write(texto.encode())

        elif self.path.startswith("/usuarios/"):
            try:
                indice = int(self.path.split("/")[2])
                try:
                    texto = "Nombre: " + usuarios[indice]["nombre"]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(texto.encode())
                except:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Usuario no encontrado")
            except:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Indice invalido")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")

    def do_POST(self):
        if self.path == "/usuarios":
            largo = int(self.headers.get("Content-Length", 0))
            cuerpo = self.rfile.read(largo)

            try:
                datos = json.loads(cuerpo)

                if "nombre" in datos:
                    usuarios.append(datos)

                    self.send_response(201)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(datos).encode())
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Falta el campo nombre")

            except:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"JSON invalido")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")

    def do_PUT(self):
        if self.path.startswith("/usuarios/"):
            largo = int(self.headers.get("Content-Length", 0))
            cuerpo = self.rfile.read(largo)

            try:
                indice = int(self.path.split("/")[2])

                try:
                    datos = json.loads(cuerpo)

                    if "nombre" in datos:
                        usuarios[indice] = {"nombre": datos["nombre"]}

                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b"Usuario actualizado")
                    else:
                        self.send_response(400)
                        self.end_headers()
                        self.wfile.write(b"Falta el campo nombre")

                except:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"JSON invalido")

            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Indice invalido o no encontrado")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")

    def do_DELETE(self):
        if self.path.startswith("/usuarios/"):
            try:
                indice = int(self.path.split("/")[2])

                try:
                    del usuarios[indice]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Usuario eliminado")
                except:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Usuario no encontrado")

            except:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Indice invalido")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta no encontrada")


servidor = HTTPServer(("localhost", 8000), MiServidor)
print("Servidor corriendo en http://localhost:8000")
servidor.serve_forever()