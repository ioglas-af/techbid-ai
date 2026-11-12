"""Configura a chave Gemini localmente sem exibi-la no terminal.

Uso normal:  python configurar_chave.py
Trocar chave: python configurar_chave.py --trocar
"""
from __future__ import annotations

import getpass
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENV_PATH = BASE / '.env'
EXAMPLE_PATH = BASE / '.env.example'


def ler_variavel(nome: str) -> str:
    if not ENV_PATH.exists():
        return ''
    for linha in ENV_PATH.read_text(encoding='utf-8-sig').splitlines():
        if linha.strip().startswith(nome + '='):
            return linha.split('=', 1)[1].strip().strip('"').strip("'")
    return ''


def configurar(trocar: bool = False) -> bool:
    if not ENV_PATH.exists():
        if EXAMPLE_PATH.exists():
            ENV_PATH.write_text(EXAMPLE_PATH.read_text(encoding='utf-8'), encoding='utf-8')
        else:
            ENV_PATH.write_text('GEMINI_API_KEY=\nGEMINI_MODEL=gemini-3.5-flash-lite\nN8N_WEBHOOK_URL=\n', encoding='utf-8')

    if ler_variavel('GEMINI_API_KEY') and not trocar:
        print('[OK] Chave Gemini ja foi configurada no arquivo .env.')
        print('     Para alterar, execute TROCAR_CHAVE_GEMINI.bat.')
        return True

    print('\n========================================')
    print(' CONFIGURAR CHAVE GEMINI')
    print('========================================')
    print('Cole sua chave Gemini aqui. O terminal NAO vai mostrar o texto digitado.')
    print('A chave fica somente no arquivo local .env (ignorado pelo Git).')
    try:
        chave = getpass.getpass('GEMINI_API_KEY (colar e pressionar Enter): ').strip()
    except (EOFError, KeyboardInterrupt):
        print('\nConfiguracao cancelada.')
        return False
    if not chave:
        print('[ERRO] Nenhuma chave informada. O app nao sera iniciado.')
        return False
    if any(c in chave for c in ('\n', '\r', ' ', '\t', '\x00', '"', "'")):
        print('[ERRO] Chave contem caracteres invalidos ou espacos. Confira a copia.')
        return False

    linhas = ENV_PATH.read_text(encoding='utf-8-sig').splitlines()
    novas = []
    substituida = False
    for linha in linhas:
        if linha.strip().startswith('GEMINI_API_KEY='):
            if not substituida:
                novas.append('GEMINI_API_KEY=' + chave)
                substituida = True
        else:
            novas.append(linha)
    if not substituida:
        novas.insert(0, 'GEMINI_API_KEY=' + chave)
    ENV_PATH.write_text('\n'.join(novas).rstrip('\n') + '\n', encoding='utf-8')
    # A chave nao e testada aqui: validar a chave requer uma solicitacao real ao Google.
    print('[OK] Chave salva no .env, sem ser exibida no terminal.')
    print('     A autenticacao sera conferida ao testar Gemini no app.')
    return True


if __name__ == '__main__':
    sys.exit(0 if configurar('--trocar' in sys.argv) else 1)
