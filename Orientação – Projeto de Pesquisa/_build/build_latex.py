#!/usr/bin/env python3
"""Gera o projeto Overleaf (main.tex + figura) a partir de projeto-paulo.md.
Uso: python3 build_latex.py <pasta_de_saida>
Fonte: Helvetica/Nimbus Sans (pacote helvet), métrica equivalente à do Arial, disponível em qualquer TeX Live/Overleaf."""
import re, sys, shutil, pathlib

HERE = pathlib.Path(__file__).parent
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / 'overleaf'
out.mkdir(parents=True, exist_ok=True)
raw = (HERE / 'projeto-paulo.md').read_text(encoding='utf8')

fm = {}
m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
for l in m.group(1).split('\n'):
    k, v = l.split(':', 1)
    fm[k.strip()] = v.strip().strip('"')
raw = raw[m.end():]

SPECIAL = {'&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
           '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '\\': r'\textbackslash{}'}
def esc(t):
    t = t.replace('●', '\x00')
    return ''.join(SPECIAL.get(c, c) for c in t).replace('\x00', r'$\bullet$')

TOK = re.compile(r'(==.+?==|\*\*[^*]+\*\*|\*[^*]+\*|https?://[^\s]+)')
def inline(t):
    out_, last = [], 0
    for mm in TOK.finditer(t):
        out_.append(esc(t[last:mm.start()]))
        s = mm.group(0)
        if s.startswith('=='):
            out_.append(r'\colorbox{yellow}{' + inline(s[2:-2]) + '}')
        elif s.startswith('**'):
            out_.append(r'\textbf{' + inline(s[2:-2]) + '}')
        elif s.startswith('*'):
            out_.append(r'\textit{' + inline(s[1:-1]) + '}')
        else:
            url, trail = s, ''
            while url and url[-1] in '.,;)':
                trail = url[-1] + trail; url = url[:-1]
            out_.append(r'\url{' + url + '}' + esc(trail))
        last = mm.end()
    out_.append(esc(t[last:]))
    return ''.join(out_)

def title_runs(bold=True):
    return r'\textbf{' + esc(fm['titulo']) + (':' if fm.get('subtitulo') else '') + '}' + \
           ((' ' + esc(fm['subtitulo'])) if fm.get('subtitulo') else '')

W = {1: [2.1, 1.6, 3.7, 1.3], 2: [1.4, 3.6, 1.8, 1.8], 3: [5, 1, 1, 1, 1, 1, 1], 4: [4, 2.5, 2.5]}
def table(rows, q):
    n = len(rows[0]); w = W[q]; tot = sum(w)
    if q == 3:
        spec = r'|p{0.40\textwidth}|' + '|'.join(['>{\\centering\\arraybackslash}p{0.07\\textwidth}'] * (n - 1)) + '|'
    else:
        spec = '|' + '|'.join(f'>{{\\raggedright\\arraybackslash}}p{{{0.96 * x / tot - 0.0:.3f}\\textwidth}}' for x in w) + '|'
    lines = [r'{\fontsize{10}{12}\selectfont\renewcommand{\arraystretch}{1.2}', r'\begin{tabular}{' + spec + '}', r'\hline']
    for ri, r in enumerate(rows):
        cells = [inline(c) for c in r]
        if ri == 0:
            cells = [r'\textbf{' + c + '}' if c else c for c in cells]
        lines.append(' & '.join(cells) + r' \\ \hline')
    lines += [r'\end{tabular}}']
    return '\n'.join(lines)

L = raw.split('\n')
body, toc_unnum = [], []
i = 0
in_refs = False
first_primary = True
while i < len(L):
    t = L[i].strip()
    if not t:
        i += 1; continue
    if t.startswith('#'):
        hm = re.match(r'(#+)\s+(.*)', t)
        lvl, txt = len(hm.group(1)), hm.group(2)
        nm = re.match(r'(\d+(?:\.\d+)*)\s+(.*)', txt)
        in_refs = txt.startswith('REFERÊNCIAS')
        if nm:
            title = nm.group(2)
            if lvl == 1:
                body.append(r'\clearpage' + '\n' + r'\section{' + inline(title.upper().replace('*', '')) + '}')
                if first_primary:
                    first_primary = False
            elif lvl == 2:
                body.append(r'\subsection{' + inline(title) + '}')
            else:
                body.append(r'\subsubsection{' + inline(title) + '}')
        else:
            u = inline(txt)
            plain = esc(txt).replace('–', '--')
            body.append(r'\clearpage' + '\n' + r'\begin{center}\textbf{' + u + r'}\end{center}' + '\n' +
                        r'\addcontentsline{toc}{section}{' + plain + '}\n' + r'\vspace{6pt}')
        i += 1; continue
    mq = re.match(r'^\[\[QUADRO\|(\d+)\|(.+)\]\]$', t)
    if mq:
        q = int(mq.group(1)); rows = []; j = i + 1
        while j < len(L) and L[j].strip().startswith('|'):
            cells = [c.strip() for c in L[j].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'-+', c) for c in cells):
                rows.append(cells)
            j += 1
        body.append(r'\begin{minipage}{\textwidth}\begin{spacing}{1}' + '\n' +
                    r'\noindent\textbf{Quadro ' + mq.group(1) + r' --} ' + inline(mq.group(2)) + r'\par\vspace{3pt}' + '\n' +
                    r'\noindent' + table(rows, q) + r'\par\end{spacing}\end{minipage}' if False else
                    r'\begin{spacing}{1}\noindent\textbf{Quadro ' + mq.group(1) + r' --} ' + inline(mq.group(2)) + r'\par\vspace{3pt}\nopagebreak' + '\n' +
                    r'\noindent' + table(rows, q) + r'\par\end{spacing}')
        i = j; continue
    mf = re.match(r'^\[\[FIGURA\|(\d+)\|(.+)\|(.+)\]\]$', t)
    if mf:
        body.append(r'\begin{spacing}{1}\noindent\textbf{Figura ' + mf.group(1) + r' --} ' + inline(mf.group(2)) + r'\par\vspace{3pt}\nopagebreak' + '\n' +
                    r'\begin{center}\includegraphics[height=0.62\textheight,keepaspectratio]{' + mf.group(3) + r'}\end{center}\end{spacing}')
        i += 1; continue
    if t.startswith('Fonte:'):
        body.append(r'\begin{spacing}{1}\noindent{\fontsize{10}{12}\selectfont ' + inline(t) + r'}\par\vspace{10pt}\end{spacing}')
        i += 1; continue
    if in_refs:
        body.append(r'\begin{spacing}{1}\raggedright\noindent ' + inline(t) + r'\par\vspace{12pt}\end{spacing}')
        i += 1; continue
    if re.match(r'^[a-z]\)\s', t):
        body.append(r'{\leftskip=1.25cm\noindent\hangindent=0.6cm ' + inline(t).replace(')', ')~', 1) + r'\par}')
        i += 1; continue
    body.append(inline(t) + '\n')
    i += 1

tex = r'''% Projeto de Pesquisa -- UEMA/Uemanet -- compilar com pdfLaTeX (padrão do Overleaf)
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[brazil]{babel}
\usepackage[scaled=1]{helvet}      % Helvetica/Nimbus Sans: métrica equivalente à do Arial
\renewcommand{\familydefault}{\sfdefault}
\usepackage[a4paper,top=3cm,left=3cm,bottom=2cm,right=2cm,headsep=1cm]{geometry}
\usepackage{setspace}
\usepackage{titlesec}
\usepackage{tocloft}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{array}
\usepackage[table]{xcolor}
\usepackage{url}
\urlstyle{same}
\usepackage[hyphens]{url}
\Urlmuskip=0mu plus 1mu
\sloppy
\onehalfspacing
\setlength{\parindent}{1.25cm}
\setlength{\parskip}{0pt}
\raggedbottom

% Títulos (NBR 6024): primária em maiúsculas/negrito; secundária negrito; terciária negrito itálico
\titleformat{\section}{\normalfont\normalsize\bfseries}{\thesection}{1ex}{}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{\thesubsection}{1ex}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries\itshape}{\thesubsubsection}{1ex}{}
\titlespacing*{\section}{0pt}{0pt}{18pt}
\titlespacing*{\subsection}{0pt}{18pt}{18pt}
\titlespacing*{\subsubsection}{0pt}{18pt}{18pt}

% Sumário
\addto\captionsbrazil{\renewcommand{\contentsname}{SUMÁRIO}}
\renewcommand{\cfttoctitlefont}{\hfill\normalfont\normalsize\bfseries}
\renewcommand{\cftaftertoctitle}{\hfill\mbox{}}
\renewcommand{\cftsecfont}{\bfseries}
\renewcommand{\cftsecpagefont}{\bfseries}
\renewcommand{\cftsecleader}{\bfseries\cftdotfill{\cftdotsep}}
\setlength{\cftbeforesecskip}{4pt}
\setlength{\cftbeforesubsecskip}{2pt}
\setlength{\cftsecindent}{0pt}\setlength{\cftsecnumwidth}{1.3cm}
\setlength{\cftsubsecindent}{0pt}\setlength{\cftsubsecnumwidth}{1.3cm}
\setlength{\cftsubsubsecindent}{0pt}\setlength{\cftsubsubsecnumwidth}{1.8cm}

% Número de página: 10 pt, canto superior direito
\pagestyle{empty}
\fancypagestyle{texto}{\fancyhf{}\fancyhead[R]{\fontsize{10}{12}\selectfont\thepage}\renewcommand{\headrulewidth}{0pt}}

\begin{document}

% ---------- CAPA (não contada) ----------
\begin{titlepage}
\centering\singlespacing
\textbf{@INST@}\\
\textbf{@NUCLEO@}\\
\textbf{@CURSO@}\par
\vspace{3.2cm}
\textbf{@AUTOR@}\par
\vspace{3.2cm}
@TITULO@\par
\vfill
\textbf{@LOCAL@}\\
\textbf{@ANO@}
\end{titlepage}
\setcounter{page}{1}

% ---------- FOLHA DE ROSTO ----------
\begin{titlepage}
\centering\singlespacing
\textbf{@AUTOR@}\par
\vspace{3.6cm}
@TITULO@\par
\vspace{1.2cm}
\hfill\begin{minipage}{8cm}\raggedright\singlespacing
@NATUREZA@\par\vspace{12pt}
Orientador: @ORIENTADOR@.
\end{minipage}
\vfill
\textbf{@LOCAL@}\\
\textbf{@ANO@}
\end{titlepage}

% ---------- SUMÁRIO ----------
\clearpage
\singlespacing\tableofcontents\onehalfspacing

\pagestyle{texto}
@BODY@
\end{document}
'''
rep = {
    '@INST@': esc(fm['instituicao']), '@NUCLEO@': esc(fm['nucleo']), '@CURSO@': esc(fm['curso']),
    '@AUTOR@': ' \\\\ '.join(esc(a) for a in fm['autor'].split(' | ')), '@TITULO@': title_runs(), '@LOCAL@': inline(fm['local']), '@ANO@': esc(fm['ano']),
    '@ORIENTADOR@': esc(fm['orientador']),
    '@NATUREZA@': 'Projeto de pesquisa apresentado ao curso ' + esc(fm['curso_extenso']) +
                  ' como requisito da disciplina de TCC, para fins de planejamento, organização e elaboração de trabalhos científicos.',
    '@BODY@': '\n'.join(body),
}
for k, v in rep.items():
    tex = tex.replace(k, v)
# a seção primária da Introdução inicia o texto numerado em estilo 'texto'
tex = tex.replace(r'\pagestyle{texto}' + '\n' + r'\clearpage', r'\clearpage\pagestyle{texto}')
(out / 'main.tex').write_text(tex, encoding='utf8')
shutil.copy(HERE / 'arquitetura.png', out / 'arquitetura.png')
(out / 'README.txt').write_text(
    'Projeto de Pesquisa - Paulo Ricardo Coimbra Sousa\n'
    'Overleaf: Menu > Compiler = pdfLaTeX; Main document = main.tex. Fonte: Helvetica/Nimbus Sans (equivalente métrico do Arial).\n'
    'Campos destacados em amarelo no texto são pendências do autor (polo, município, prédio etc.).\n', encoding='utf8')
print('ok', out / 'main.tex')
