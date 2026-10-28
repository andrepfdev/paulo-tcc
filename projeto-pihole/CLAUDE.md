# Projeto de Pesquisa – Pi-hole em prédios públicos municipais (TCC UEMA/Uemanet)

Contexto para continuar o trabalho no Claude Code. Leia este arquivo antes de editar qualquer coisa.

## Arquivos

| Arquivo | Função |
|---|---|
| `projeto_pihole.md` | **Fonte única do texto.** Edite aqui, nunca direto no .docx |
| `build_docx.js` | Gera o .docx ABNT/UEMA a partir do .md (Node + pacote `docx`) |
| `pages.py` | Lê o PDF renderizado e calcula as páginas do sumário (`pages.json`) |
| `arquitetura.mmd` / `arquitetura.png` | Figura 1 (Mermaid → PNG via `mmdc`) |
| `projeto.docx` | Saída final |

### Como regenerar (2 passadas para o sumário ficar com as páginas certas)

```bash
npm i docx            # se necessário
mmdc -i arquitetura.mmd -o arquitetura.png -b white -s 3 -w 900   # só se mudar a figura
node build_docx.js pages.json projeto.docx
soffice --headless --convert-to pdf projeto.docx
python3 pages.py projeto.pdf          # atualiza pages.json
node build_docx.js pages.json projeto.docx   # rode de novo até pages.json não mudar
```

Convenções do .md: `#`/`##`/`###` = seções; `a) ...` = alínea; `[[QUADRO|n|título]]` + tabela + `Fonte:`; `[[FIGURA|n|título|arquivo.png]]` + `Fonte:`; blocos `::: resumo`, `::: abstract`, `::: siglas`. Dados de capa no front matter YAML. Se acrescentar quadros, ajuste `colWeightsByQuadro` no script. Se acrescentar figura, ajuste `wpx/hpx` (dimensões do PNG) no script.

## Decisões já tomadas (não mudar sem falar com o orientador)

- Modalidade: TCC **Proposta Tecnológica** (estrutura do modelo UEMA + exigências da atividade: Introdução com problema, justificativa, hipóteses e objetivos; Fundamentação; Metodologia).
- Título escolhido: **FILTRAGEM DNS COM PI-HOLE EM SERVIDOR LOCAL: proposta de controle de acesso a conteúdos indevidos na rede de um prédio público municipal**. Alternativas:
  1. Pi-hole como ferramenta de segurança de rede na administração pública municipal: implantação e avaliação em ambiente de baixo custo
  2. Controle de navegação baseado em DNS na administração pública municipal: uma proposta com Pi-hole
  3. Segurança de redes em prédios públicos municipais: o Pi-hole como filtro DNS contra conteúdo impróprio e malicioso
  4. Um "buraco negro" para o conteúdo indevido: Pi-hole na proteção da rede de prédios públicos municipais
- **Sem Raspberry Pi**: servidor local Linux (Debian 12 ou Ubuntu Server 24.04 LTS), físico reaproveitado ou VM, IP fixo, Pi-hole v6, Unbound opcional.
- Escopo **fechado**: 1 prédio; 4 categorias (sexual, apostas, malware/phishing, conteúdo criminoso); testes em ambiente de homologação + piloto opcional de 15 dias em 1 setor.
- **Fora do escopo**: inspeção HTTPS, autenticação por usuário, dados móveis 4G/5G, filtrar conteúdo dentro de site permitido, alta disponibilidade.
- Método: pesquisa aplicada, quali-quantitativa, exploratória/descritiva, **Design Science Research** (Dresch; Lacerda; Antunes Júnior, 2015; Hevner et al., 2004).
- Métricas-alvo (validar com orientador): bloqueio ≥ 90%; falsos positivos < 2%; aumento < 10% no tempo mediano de resposta DNS.
- Extra opcional (só se sobrar tempo): painel de relatórios em **PHP** consumindo a API REST do Pi-hole v6, apenas dados agregados.

## Pendências do estudante (campos entre colchetes no .md)

- `[NOME DO ESTUDANTE]`, `[NOME DO CURSO]`, `[Polo]`, `[Titulação] [Nome do(a) Orientador(a)]`
- `[Município]`, nome do prédio/órgão, nº de estações, equipamentos de rede (seção 3.2)
- Parágrafo final da justificativa (1.2): motivação pessoal, sem 1ª pessoa do singular
- Confirmar com o orientador: elementos pré-textuais exigidos (o modelo de Proposta Tecnológica traz ficha catalográfica e folha de aprovação — foram omitidas por ser etapa de projeto), ordem Fundamentação/Metodologia, meses do cronograma, necessidade de CEP (Res. CNS 510/2016)
- Obter termo de anuência do órgão antes de qualquer coleta

## Referências – status de verificação (out./2026)

Todas foram localizadas em fonte real. Atenção ao revisar:

- **Verificadas online nesta sessão**: Elavarasi et al. (2026, JADS, DOI 10.47738/jads.v7i3.1472); NIST SP 800-81r3 (Rose; Liu; Gibson, mar. 2026); CISA Encrypted DNS Guidance (2024); NSA/CISA Protective DNS (2021); TIC Governo Eletrônico 2023 (dados: 4.265 prefeituras, 91% com serviço digital, 33% com centro de operações); Arruda (2025, WeLiveSecurity); Guia PPSI v1.1.3 (2024); Pi-hole v6 (blog, 18 fev. 2025); Decreto 11.856/2023; Kührer et al. (RAID 2014); Hounsel et al. (WWW 2020); Khormali et al. (arXiv 2006.15277); Kurose e Ross 8. ed. (Bookman, 2021); Tanenbaum, Feamster e Wetherall 6. ed. (Bookman, 2021).
- **Conhecimento consolidado, conferir dados de edição na biblioteca/Minha Biblioteca**: Gil (2022), Marconi e Lakatos (2022), Wazlawick (2014), Stallings e Brown (2014), Bardin (2016), Dresch et al. (2015), Hevner et al. (2004), ABNT NBR ISO/IEC 27001/27002 (2022), RFCs 1034, 1035, 7858, 8484, leis e decretos (planalto.gov.br).
- **Conferir URL antes de entregar**: UT1 Blacklists (`dsi.ut-capitole.fr/blacklists/`), Unbound docs, CIS Controls v8.1.
- Todas as citações são **indiretas** (sem número de página). Se transformar alguma em citação direta, inclua a página exata.
- Formato: NBR 10520:2023 (autor-data em maiúsculas/minúsculas) e NBR 6023 (título em negrito, alinhado à esquerda, espaço simples, linha em branco entre referências).

## Próximos passos sugeridos (TCC completo)

1. Preencher pendências e enviar ao orientador.
2. Executar o diagnóstico (Apêndices A e B) → reescrever 3.2 com dados reais.
3. Laboratório: instalar Pi-hole, montar amostras de domínios (fonte independente das listas usadas), scripts de teste com `dig` (taxa de bloqueio, falsos positivos, latência) gerando CSV.
4. Seção 4 vira "Proposta Tecnológica" final: manual de implantação passo a passo + minuta de política de uso aceitável + resultados (tabelas/gráficos).
5. Acrescentar Resultados e Discussão + Considerações Finais; atualizar resumo/abstract (formato informativo, 150–500 palavras).
