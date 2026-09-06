"""Testes que rodam sem rede e sem .env.

src/run.py e um script de cima a baixo: abre o cliente STAC no import e le o
.env na hora. Importa-lo aqui e chamar a API do Planetary Computer de dentro do
CI — e o teste antigo ainda chamava um run.main() que nunca existiu. O que da
para garantir sem rede e o contrato: o script compila e toda variavel que ele
le esta documentada no .env.example.
"""
import ast
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "src" / "run.py"


def test_script_compila():
    ast.parse(SCRIPT.read_text(encoding="utf-8"), filename=str(SCRIPT))


def test_env_example_documenta_tudo_que_o_script_le():
    lidas = set(re.findall(r"os\.getenv\(['\"]([A-Z_]+)['\"]", SCRIPT.read_text(encoding="utf-8")))
    documentadas = {
        linha.split("=", 1)[0].strip()
        for linha in (RAIZ / ".env.example").read_text(encoding="utf-8").splitlines()
        if "=" in linha and not linha.lstrip().startswith("#")
    }
    faltando = lidas - documentadas
    assert not faltando, f"variaveis lidas pelo script e ausentes do .env.example: {sorted(faltando)}"
