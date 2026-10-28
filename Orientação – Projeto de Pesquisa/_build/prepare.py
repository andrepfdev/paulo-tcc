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

# --- revisão pós-crítica (28/10/2026): referências, dado do Cetic.br, métodos
def sub1(old, new):
    global text
    assert text.count(old) == 1, ('âncora ausente/duplicada: ' + old[:60], text.count(old))
    text = text.replace(old, new)

ANPD = 'AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS'
# 1) dado do Cetic.br usado fora do escopo
text, n = re.subn(r'Essa expansão, porém, não foi acompanhada.*?pouca ou nenhuma camada de proteção e de controle\.',
    'Essa expansão amplia a superfície de exposição das redes municipais: quanto mais os serviços e os usuários '
    'dependem da conexão, maior o impacto de acessos indevidos e de ataques, e os incidentes contra órgãos públicos '
    'têm crescido (ARRUDA, 2025). A pesquisa do Cetic.br, contudo, não mede a segurança cibernética das prefeituras; '
    'por isso, a ausência de controles de navegação em redes de municípios de pequeno porte é tratada aqui como '
    'problema observado pelo pesquisador, e não como dado estatístico.', text, flags=re.S)
assert n == 1
sub1('Os dados da pesquisa TIC Governo Eletrônico, que revelam baixa presença de centros de monitoramento nas prefeituras menores '
     '(CENTRO REGIONAL DE ESTUDOS PARA O DESENVOLVIMENTO DA SOCIEDADE DA INFORMAÇÃO, 2024), e o aumento dos incidentes contra órgãos públicos (ARRUDA, 2025) reforçam',
     'O aumento dos incidentes contra órgãos públicos (ARRUDA, 2025) reforça')
# 2) normas vigentes
sub1('A Política Nacional de Segurança da Informação (BRASIL, 2018a) e a Política Nacional de Cibersegurança (BRASIL, 2023) estabelecem',
     'A Política Nacional de Segurança da Informação (BRASIL, 2025a), a Política Nacional de Cibersegurança (BRASIL, 2023) e a Estratégia Nacional de Cibersegurança (BRASIL, 2025b) estabelecem')
sub1('a Política Nacional de Segurança da Informação (BRASIL, 2018a) e a Política Nacional de Cibersegurança (BRASIL, 2023) definem',
     'a Política Nacional de Segurança da Informação (BRASIL, 2025a), a Política Nacional de Cibersegurança (BRASIL, 2023) e a Estratégia Nacional de Cibersegurança (BRASIL, 2025b) definem')
text = text.replace('2018b', '2018')
# 3) novas referências no texto
sub1('para acelerar consultas futuras.',
     'para acelerar consultas futuras. A terminologia adotada neste trabalho segue a consolidação mais recente publicada pelo IETF (HOFFMAN; FUJIWARA, 2024).')
sub1('A eficácia desse modelo, porém, depende diretamente da qualidade das listas utilizadas.',
     'O CIS Controls v8.1 distingue a filtragem de DNS (salvaguarda 9.2), que bloqueia domínios maliciosos conhecidos, dos filtros de URL em nível de rede '
     '(salvaguarda 9.3), distinção que delimita o que o Pi-hole resolve e o que exigiria controles adicionais (CENTER FOR INTERNET SECURITY, 2024). '
     'A eficácia desse modelo, porém, depende diretamente da qualidade das listas utilizadas.')
sub1('controles de DNS da organização (CYBERSECURITY AND INFRASTRUCTURE SECURITY AGENCY, 2024).',
     'controles de DNS da organização (CYBERSECURITY AND INFRASTRUCTURE SECURITY AGENCY, 2024). O DNS sobre QUIC (DoQ), padronizado em 2022, '
     'oferece confidencialidade comparável à do DoT sobre outro transporte (HUITEMA; DICKINSON; MANKIN, 2022); por restrição de escopo, os testes de contorno '
     'se limitarão a DNS externo configurado manualmente, DoT e DoH, e o DoQ será registrado como limitação.')
sub1('e comunicar a existência do filtro aos usuários por meio de uma política de uso aceitável.',
     'e comunicar a existência do filtro aos usuários por meio de uma política de uso aceitável. O guia orientativo da ANPD sobre o tratamento de dados pessoais pelo poder público '
     f'detalha a aplicação das bases legais e dos princípios da LGPD a órgãos públicos ({ANPD}, 2023a), e o guia sobre fins acadêmicos orienta o tratamento de dados em estudos e pesquisas ({ANPD}, 2023b).')
sub1('Dresch, Lacerda e Antunes Júnior (2015) organizam a DSR',
     'Peffers *et al.* (2007) propõem processo em seis atividades (identificação do problema e motivação, definição dos objetivos da solução, projeto e desenvolvimento, demonstração, avaliação e comunicação), '
     'que orienta a sequência das etapas do Quadro 1. Dresch, Lacerda e Antunes Júnior (2015) organizam a DSR')
sub1('Na etapa 3, o servidor local receberá',
     'A avaliação do artefato segue o *framework* FEDS, de Venable, Pries-Heje e Baskerville (2016), que classifica as avaliações quanto ao propósito (formativa ou somativa) e ao paradigma (artificial ou naturalista). '
     'Os testes em ambiente de homologação constituem avaliação artificial e formativa, que permite corrigir o artefato; o piloto, quando autorizado, constitui avaliação naturalista e somativa. '
     'Caso o piloto não seja autorizado, a conclusão se apoiará na avaliação em homologação, e as limitações decorrentes serão registradas.\n\n'
     'Na etapa 3, o servidor local receberá')
# 4) lista local de domínios indesejados do setor
sub1('a partir das fontes discutidas na seção 3.3, uma lista de permissão',
     'a partir das fontes discutidas na seção 3.3, uma lista local de domínios indesejados, definida com o responsável pelo setor e aplicada apenas ao grupo de clientes desse setor, uma lista de permissão')
sub1('b) políticas de filtragem: listas de bloqueio por categoria, expressões regulares,',
     'b) políticas de filtragem: listas de bloqueio por categoria, lista local de domínios indesejados definida com cada setor, expressões regulares,')
# 5) Quadro 2: amostras, cache e novos indicadores
sub1('extraída de fontes independentes das listas utilizadas |',
     'extraída de fontes independentes das listas utilizadas, com tamanho, origem, data de coleta e critério de classificação registrados |')
sub1('com o DNS atual e com o Pi-hole, com e sem *cache* | Tempo médio e mediana de resposta (ms) |',
     'com o DNS atual e com o Pi-hole, com *cache* frio e aquecido, em medições repetidas | Mediana e dispersão do tempo de resposta (ms) |')
sub1('| Grupos | Verificar',
     '| Custo | Registrar o custo de aquisição ou aproveitamento do servidor, o tempo de configuração, a manutenção necessária e, se viável, o consumo elétrico estimado | Custo (R$), tempo (h) e consumo estimado (kWh/mês) | Registro de implantação |\n'
     '| Confiabilidade | Simular a indisponibilidade do servidor Pi-hole e uma regra de *firewall* incorreta, registrando o comportamento da rede e a recuperação | Tempo de recuperação e comportamento da rede | Roteiro de testes e registro em planilha |\n'
     '| Grupos | Verificar')
sub1('Os parâmetros de referência para a análise, a serem validados com o orientador, são:',
     'Os critérios de avaliação, definidos antes da execução dos testes e a serem validados com o orientador, não são resultados esperados nem garantidos; são eles:')
sub1('em relação ao DNS atualmente utilizado.',
     'em relação ao DNS atualmente utilizado.\n\n'
     'No diagnóstico da etapa 2, será confirmado se o roteador TP-Link Aginet EX511 permite definir o DNS distribuído por DHCP e criar regras de saída que bloqueiem DNS externo; '
     'caso não permita, serão documentadas alternativas, como o uso de um *firewall* adicional ou do próprio servidor como DHCP. '
     'Ressalta-se que o Pi-hole bloqueia nomes de domínio das categorias escolhidas, e não o conteúdo das páginas, de modo que os resultados não permitirão afirmar que o acesso a conteúdo indevido foi impedido por completo nem que os riscos de *malware* e *phishing* foram eliminados.')
sub1('sem identificação de servidores, em conformidade com a LGPD (BRASIL, 2018).',
     'sem identificação de servidores, em conformidade com a LGPD (BRASIL, 2018). Os registros terão como finalidade exclusiva a avaliação do filtro e a segurança da rede, '
     'com acesso restrito ao responsável técnico e ao pesquisador, prazo de retenção definido com a instituição e limitado ao necessário para a pesquisa, e exclusão ao término do estudo '
     f'({ANPD}, 2023a, 2023b).')

# 5b) dois autores
text = text.replace('Elaborado pelo autor', 'Elaborado pelos autores')
sub1('como problema observado pelo pesquisador,', 'como problema observado pelos pesquisadores,')
sub1('do próprio órgão ou do pesquisador,', 'do próprio órgão ou dos pesquisadores,')
sub1('ao responsável técnico e ao pesquisador,', 'ao responsável técnico e aos pesquisadores,')

# 7) plataforma do servidor e acesso ao painel
sub1('inclusive em um computador reaproveitado ou em uma máquina virtual, solução adotada neste projeto',
     'inclusive em um computador reaproveitado, solução adotada neste projeto, com instalação nativa e sem contêineres, e em uma máquina virtual, restrita ao ambiente de homologação,')
sub1('um sistema operacional Linux de suporte estendido (Debian 12 ou Ubuntu Server 24.04 LTS), endereço IP fixo e a versão estável mais recente do Pi-hole.',
     'um sistema operacional Linux de suporte estendido (Debian 12 ou Ubuntu Server 24.04 LTS), sem interface gráfica, instalado em computador reaproveitado, endereço IP fixo e a versão estável mais recente do Pi-hole, instalada diretamente no sistema, sem contêineres, pela simplicidade da configuração de rede e pela facilidade de replicação por equipes pequenas. O acesso ao painel de administração será restrito, por regra de *firewall* do servidor, às estações da administração, com senha forte e HTTPS. O computador será configurado para reiniciar após queda de energia e terá cópia periódica de suas configurações.')
sub1('a) servidor local: computador ou máquina virtual com Linux, endereço IP fixo, Pi-hole e, opcionalmente, Unbound',
     'a) servidor local: computador reaproveitado com Linux em edição servidor, endereço IP fixo, Pi-hole instalado de forma nativa e, opcionalmente, Unbound')
sub1('d) gestão e governança: painel de acompanhamento,', 'd) gestão e governança: painel de acompanhamento com acesso restrito às estações de administração,')
sub1('registrando o comportamento da rede e a recuperação | Tempo de recuperação',
     'o desligamento abrupto do computador e a restauração da cópia de configuração, registrando o comportamento da rede e a recuperação, e verificar que o painel não abre em estação comum | Tempo de recuperação')
sub1('Como o filtro atua no servidor,',
     'O Pi-hole também é distribuído como imagem Docker, forma que não será avaliada neste trabalho. Como o filtro atua no servidor,')

# 6) Referências
m = re.search(r'^BRASIL\. Decreto nº 9\.637.*\n\n', text, re.M); assert m
text = text.replace(m.group(0), '')
def ins_before(anchor, entry):
    global text
    assert text.count('\n' + anchor) == 1, anchor
    text = text.replace('\n' + anchor, '\n' + entry + '\n\n' + anchor)
ins_before('CENTER FOR INTERNET SECURITY.',
  'BRASIL. Decreto nº 12.572, de 4 de agosto de 2025. Institui a Política Nacional de Segurança da Informação e dispõe sobre a governança da segurança da informação. '
  '**Diário Oficial da União**: seção 1, Brasília, DF, 5 ago. 2025a. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/d12572.htm. Acesso em: 28 out. 2026.\n\n'
  'BRASIL. Decreto nº 12.573, de 4 de agosto de 2025. Institui a Estratégia Nacional de Cibersegurança. '
  '**Diário Oficial da União**: seção 1, Brasília, DF, 5 ago. 2025b. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/d12573.htm. Acesso em: 28 out. 2026.')
ins_before('BARDIN, Laurence.',
  f'{ANPD}. **Tratamento de dados pessoais pelo Poder Público**: guia orientativo. Versão 2.0. Brasília, DF: ANPD, jun. 2023a. '
  'Disponível em: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-poder-publico-anpd-versao-final.pdf. Acesso em: 28 out. 2026.\n\n'
  f'{ANPD}. **Tratamento de dados pessoais para fins acadêmicos e para a realização de estudos e pesquisas**: guia orientativo. Brasília, DF: ANPD, 2023b. '
  'Disponível em: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-tratamento-de-dados-pessoais-para-fins-academicos-e-para-a-realizacao-de-estudos-e-pesquisas. Acesso em: 28 out. 2026.')
ins_before('HOFFMAN, Paul; MCMANUS',
  'HOFFMAN, Paul; FUJIWARA, Kazunori. **RFC 9499**: DNS terminology. [*S. l.*]: IETF, 2024. DOI: https://doi.org/10.17487/RFC9499.')
ins_before('KHORMALI, Aminollah',
  'HUITEMA, Christian; DICKINSON, Sara; MANKIN, Allison. **RFC 9250**: DNS over dedicated QUIC connections. [*S. l.*]: IETF, 2022. DOI: https://doi.org/10.17487/RFC9250.')
ins_before('PI-HOLE. **Pi-hole documentation**',
  'PEFFERS, Ken *et al*. A design science research methodology for information systems research. **Journal of Management Information Systems**, [*s. l.*], v. 24, n. 3, p. 45-77, 2007. DOI: https://doi.org/10.2753/MIS0742-1222240302.')
ins_before('WAZLAWICK, Raul',
  'VENABLE, John; PRIES-HEJE, Jan; BASKERVILLE, Richard. FEDS: a framework for evaluation in design science research. **European Journal of Information Systems**, [*s. l.*], v. 25, n. 1, p. 77-89, 2016. DOI: https://doi.org/10.1057/ejis.2014.36.')

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
autor: PAULO RICARDO COIMBRA SOUSA | KAIRO BRENDO RODRIGUES MARINHO LOPES SILVA
titulo: "FILTRAGEM DNS COM PI-HOLE EM SERVIDOR LOCAL"
subtitulo: "proposta de controle de acesso a conteúdos indevidos na rede de um prédio público municipal"
orientador: "Prof. Me. Paulo Ericson Valentim Silva"
local: "Grajaú – MA"
ano: "2026"
---

'''
OUT.write_text(fm + text.strip() + '\n', encoding='utf8')
print('ok', OUT, len(text))
