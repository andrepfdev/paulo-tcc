#!/usr/bin/env python3
"""Gera projeto-paulo.md (estrutura do Modelo UEMA) a partir do rascunho da PPS."""
import re, sys, pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE.parent.parent / 'projeto-pihole' / 'projeto_pihole.md'
OUT = HERE / 'projeto-paulo.md'

raw = SRC.read_text(encoding='utf8')
raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
raw = re.sub(r'^---\n.*?\n---\n', '', raw, flags=re.S)
raw = re.sub(r'^::: \w+\n.*?\n:::\n', '', raw, flags=re.S | re.M)  # sem resumo/abstract/siglas

# divide em seções primárias
parts = re.split(r'^(?=# )', raw, flags=re.M)
sec = {}
for p in parts:
    m = re.match(r'# (.*)', p)
    if m:
        sec[m.group(1).strip()] = p
def get(prefix):
    return next(v for k, v in sec.items() if k.startswith(prefix))

intro = get('1 INTRODUÇÃO')
ref = get('2 FUNDAMENTAÇÃO')
met = get('3 METODOLOGIA')
prop = get('4 PROPOSTA')
cron = get('5 CRONOGRAMA')
tail = ''.join(v for k, v in sec.items() if k.startswith(('REFERÊNCIAS', 'APÊNDICE')))

# --- 1 Introdução / 2 Objetivos
i_main, i_obj = intro.split('## 1.4 Objetivos')
i_main = i_main.rstrip() + '\n\n'
obj_geral = re.search(r'### 1\.4\.1 Objetivo geral\n\n(.*?)\n\n### 1\.4\.2', i_obj, re.S).group(1)
obj_esp = re.search(r'### 1\.4\.2 Objetivos específicos\n\n(.*?)\n\nEste projeto está', i_obj, re.S).group(1)
# parágrafo final da introdução (estrutura do trabalho), reescrito
estrutura = ('Este projeto está organizado em cinco seções. Após esta introdução, a seção 2 apresenta os objetivos '
             'geral e específicos. A seção 3 traz o referencial teórico, abordando a segurança da informação na '
             'administração pública, o funcionamento do DNS, a filtragem baseada em DNS, o Pi-hole e seus limites, '
             'além dos aspectos legais envolvidos. A seção 4 descreve a metodologia, incluindo a proposta tecnológica '
             'preliminar, e a seção 5 apresenta o cronograma de execução. Seguem-se as referências e os apêndices.')
# insere o parágrafo antes de 1.1 (último parágrafo do texto de abertura)
i_main = i_main.replace('## 1.1 Problema', estrutura + '\n\n## 1.1 Problema', 1)
i_main = i_main.replace('Pi-hole surge como alternativa', 'Pi-hole surge como alternativa', 1)
i_main = i_main.replace('atua como servidor DNS da rede local',
                        'atua como servidor DNS (*Domain Name System*) da rede local', 1)
i_main = i_main.replace('(DSR)', '(DSR)')

objetivos = ('# 2 OBJETIVOS\n\nOs objetivos a seguir orientam o desenvolvimento da pesquisa.\n\n'
             '## 2.1 Objetivo Geral\n\n' + obj_geral.strip() + '\n\n'
             '## 2.2 Objetivos Específicos\n\nPara alcançar o objetivo geral, serão realizadas as seguintes ações:\n\n'
             + obj_esp.strip() + '\n\n')

# --- 3 Referencial teórico (2.x -> 3.x)
ref = ref.replace('# 2 FUNDAMENTAÇÃO TEÓRICA', '# 3 REFERENCIAL TEÓRICO')
ref = re.sub(r'^## 2\.(\d)', r'## 3.\1', ref, flags=re.M)
ref = ref.replace('Esta seção reúne', 'Esta seção reúne')

# --- 4 Metodologia (3.x -> 4.x) + proposta tecnológica preliminar como 4.4
met = met.replace('# 3 METODOLOGIA', '# 4 METODOLOGIA')
for old, new in [('3.5', '4.6'), ('3.4', '4.5'), ('3.3', '4.3'), ('3.2', '4.2'), ('3.1', '4.1')]:
    met = met.replace('## ' + old + ' ', '## ' + new + ' ')
met = met.replace('seção 2.3', 'seção 3.3')
prop_body = prop.split('\n', 1)[1].strip()
prop_body = prop_body.replace('Esta seção antecipa', 'Esta subseção antecipa')
sec44 = '## 4.4 Proposta tecnológica preliminar\n\n' + prop_body + '\n\n'
met = met.replace('## 4.5 Análise dos dados', sec44 + '## 4.5 Análise dos dados')

# --- 5 Cronograma: acrescenta out., marcador ●
cron = cron.replace('Nov. | Dez. | Jan. | Fev. | Mar. |', 'Out. | Nov. | Dez. | Jan. | Fev. | Mar. |')
cron = cron.replace('|---|---|---|---|---|---|', '|---|---|---|---|---|---|---|')
def fix_row(line):
    if not line.startswith('|') or line.startswith('| Atividades') or line.startswith('|---'):
        return line
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    cells = [cells[0], ''] + cells[1:]
    return '| ' + ' | '.join(c.replace('X', '●') for c in cells) + ' |'
cron = '\n'.join(fix_row(l) for l in cron.split('\n'))
# out.: entrega do projeto e orientação; ajustes de ordem
cron = cron.replace('| Levantamento bibliográfico e documental |  | ● | ● |', '| Levantamento bibliográfico e documental | ● | ● | ● |')
cron = cron.replace('| Elaboração e entrega do projeto de pesquisa |  | ● |', '| Elaboração e entrega do projeto de pesquisa | ● | ● |')
cron = cron.replace('| Orientações com o(a) orientador(a) |  |', '| Orientações com o orientador | ● |')
cron = cron.replace('com o(a) orientador(a)', 'com o orientador')
cron = cron.replace('Quadro 3 apresenta a distribuição das atividades ao longo do período de execução, que deverá ser ajustada ao calendário acadêmico do curso.',
                    'Quadro 3 apresenta a distribuição das atividades ao longo do período de execução, de outubro de 2026 a março de 2027, que poderá ser ajustada ao calendário acadêmico do curso e à autorização da instituição para a realização do piloto.')

text = i_main + objetivos + ref + met + cron + tail
text = re.sub(r'o\(a\) orientador\(a\)', 'o orientador', text)
text = text.replace('orientador(a)', 'orientador')

# --- citações: (Autor, ano) -> (AUTOR, ano)
CIT = re.compile(r'\(([^()\d;]+(?:;\s*[^()\d;]+)*,\s*\d{4}[a-z]?(?:;\s*[^()\d;]+(?:;\s*[^()\d;]+)*,\s*\d{4}[a-z]?)*)\)')
def up(m):
    inner = m.group(1)
    chunks = re.split(r'(\*et al\.\*)', inner)
    inner = ''.join(c if c == '*et al.*' else re.sub(r'[^\d,;\s]+(?:\s+[^\d,;\s]+)*', lambda w: w.group(0).upper(), c) for c in chunks)
    inner = re.sub(r'(\d{4})([A-Z])', lambda m: m.group(1) + m.group(2).lower(), inner)
    return '(' + inner + ')'
# aplica só fora das referências
head, sep, refs = text.partition('# REFERÊNCIAS')
head = CIT.sub(up, head)
text = head + sep + refs

# --- placeholders destacados
PH = re.compile(r'\[(Município|nome do prédio[^\]]*|número|descrever[^\]]*)\]')
text = PH.sub(lambda m: '==[' + m.group(1).replace('*', '') + ']==', text)
LOCAL = ('O estudo será realizado no prédio-sede da Secretaria Municipal de Educação de Sítio Novo/MA, situado na '
         'Avenida Leonardo de Almeida, s/nº, Centro, que conta com aproximadamente 14 estações de trabalho, conectadas em '
         'sua maior parte por rede cabeada com cabeamento de categoria 5e, além de rede sem fio (*Wi-Fi*), sendo a '
         'distribuição de endereços (DHCP) e o acesso à internet realizados por um roteador TP-Link Aginet EX511 '
         '(*Wi-Fi* 6, *Dual-Band* AX3000). ')
text = re.sub(r'O estudo será realizado no ==\[nome do prédio.*?==\[descrever[^\]]*\]==\. ', LOCAL, text, flags=re.S)
text = text.replace('==[Município]==', 'Sítio Novo').replace('[Nome do Curso]', 'Tecnologia em Análise e Desenvolvimento de Sistemas')
text = re.sub(r'e com a observação de que ==\[descrever[^\]]*\]==\.',
              'e com a necessidade observada de evitar o uso indevido das redes públicas de internet, o que motivou a busca por uma solução acessível de controle de acesso.', text)

fm = '''---
instituicao: UNIVERSIDADE ESTADUAL DO MARANHÃO
nucleo: NÚCLEO DE TECNOLOGIAS PARA EDUCAÇÃO
curso: CURSO SUPERIOR DE TECNOLOGIA EM ANÁLISE E DESENVOLVIMENTO DE SISTEMAS
curso_extenso: Superior de Tecnologia em Análise e Desenvolvimento de Sistemas
autor: PAULO RICARDO COIMBRA SOUSA
titulo: "FILTRAGEM DNS COM PI-HOLE EM SERVIDOR LOCAL"
subtitulo: "proposta de controle de acesso a conteúdos indevidos na rede de um prédio público municipal"
orientador: "Prof. Me. Paulo Ericson Valentim Silva"
local: "Grajaú – MA"
ano: "2026"
---

'''
OUT.write_text(fm + text.strip() + '\n', encoding='utf8')
print('ok', OUT, len(text))
