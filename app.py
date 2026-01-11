from flask import Flask, request, jsonify
import shutil
import os

app = Flask(__name__)

@app.route("/copiar", methods=["POST"])
def copiar():
    origem = request.json.get("origem")
    destino = request.json.get("destino")

    if not origem or not destino:
        return jsonify({"erro": "origem e destino obrigatórios"}), 400

    try:
        os.makedirs(destino, exist_ok=True)

        if os.path.isfile(origem):
            shutil.copy2(origem, destino)
        elif os.path.isdir(origem):
            shutil.copytree(origem, os.path.join(destino, os.path.basename(origem)), dirs_exist_ok=True)
        else:
            return jsonify({"erro": "origem não encontrada"}), 404

        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
