---
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

# 1 INTRODUÇÃO

A informatização dos serviços públicos municipais avançou de forma expressiva na última década. Segundo a pesquisa TIC Governo Eletrônico 2023, que ouviu 4.265 prefeituras, 91% delas já disponibilizavam ao menos um serviço digital ao cidadão, contra 75% dez anos antes (CENTRO REGIONAL DE ESTUDOS PARA O DESENVOLVIMENTO DA SOCIEDADE DA INFORMAÇÃO, 2024). Essa expansão amplia a superfície de exposição das redes municipais: quanto mais os serviços e os usuários dependem da conexão, maior o impacto de acessos indevidos e de ataques, e os incidentes contra órgãos públicos têm crescido (ARRUDA, 2025). A pesquisa do Cetic.br, contudo, não mede a segurança cibernética das prefeituras; por isso, a ausência de controles de navegação em redes de municípios de pequeno porte é tratada aqui como problema observado pelos pesquisadores, e não como dado estatístico.

Os efeitos dessa fragilidade já são visíveis. Em 2025, ataques cibernéticos interromperam serviços de prefeituras como as de São José do Rio Preto (SP), Paranhos (MS) e Porto Nacional (TO), afetando emissão de notas fiscais, agendamento de consultas e sistemas de arrecadação; dados do Centro de Prevenção, Tratamento e Resposta a Incidentes Cibernéticos de Governo indicam que, em apenas sete meses de 2025, os incidentes contra sistemas governamentais superaram os totais anuais de 2021, 2022 e 2023 (ARRUDA, 2025). Grande parte desses ataques começa com uma ação simples do usuário final, como o acesso a uma página maliciosa, o clique em um *link* de *phishing* ou o *download* de um arquivo infectado, o que coloca a navegação na *web* no centro do problema.

Paralelamente ao risco técnico, existe um problema de conduta e de responsabilidade. A rede de um prédio público é um bem público, e seu uso para acessar conteúdo sexual, sítios de apostas ou, em casos extremos, material de natureza criminosa, como o que envolve abuso sexual de crianças e adolescentes, tipificado pelo Estatuto da Criança e do Adolescente (BRASIL, 1990), expõe a administração a danos de imagem, a responsabilização e ao desperdício de recursos. A norma ABNT NBR ISO/IEC 27002 inclui, entre seus controles, a filtragem da *web* como meio de reduzir a exposição a conteúdo malicioso e de impedir o acesso a recursos externos não autorizados (ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS, 2022b), e o *Center for Internet Security* recomenda o uso de serviços de filtragem DNS em todos os ativos da organização como salvaguarda básica (CENTER FOR INTERNET SECURITY, 2024).

Soluções comerciais de filtragem de conteúdo, como *firewalls* de próxima geração e *proxies* com inspeção de tráfego, existem, mas geralmente envolvem licenças anuais e exigem mão de obra especializada, o que as torna pouco acessíveis à realidade da maioria das prefeituras. Nesse cenário, o Pi-hole surge como alternativa: trata-se de um software livre que atua como servidor DNS (*Domain Name System*) da rede local e que responde com um endereço nulo às consultas por domínios presentes em listas de bloqueio, impedindo que qualquer dispositivo da rede alcance esses destinos, sem necessidade de instalar programas nas estações de trabalho (PI-HOLE, 2025a). Embora seja popularmente associado ao Raspberry Pi, o Pi-hole pode ser instalado em qualquer servidor Linux, inclusive em um computador reaproveitado, solução adotada neste projeto, com instalação nativa e sem contêineres, e em uma máquina virtual, restrita ao ambiente de homologação, por oferecer maior capacidade de processamento, armazenamento e estabilidade para um ambiente institucional.

Diante desse contexto, este projeto delimita-se ao estudo da implantação do Pi-hole em servidor local, como filtro DNS, na rede de **um** prédio público municipal de Sítio Novo/MA, com foco no bloqueio de quatro categorias de conteúdo: (i) sexual/pornográfico; (ii) apostas *on-line*; (iii) domínios maliciosos (*malware* e *phishing*); e (iv) domínios associados a conteúdo de natureza criminosa presentes em listas públicas. Ficam fora do escopo a inspeção do conteúdo de tráfego cifrado (HTTPS), a autenticação individual de usuários, o controle de dispositivos que utilizem redes móveis próprias (4G/5G) e a filtragem de conteúdos específicos dentro de sítios permitidos, limites que serão discutidos ao longo do trabalho.

Este projeto está organizado em cinco seções. Após esta introdução, a seção 2 apresenta os objetivos geral e específicos. A seção 3 traz o referencial teórico, abordando a segurança da informação na administração pública, o funcionamento do DNS, a filtragem baseada em DNS, o Pi-hole e seus limites, além dos aspectos legais envolvidos. A seção 4 descreve a metodologia, incluindo a proposta tecnológica preliminar, e a seção 5 apresenta o cronograma de execução. Seguem-se as referências e os apêndices.

## 1.1 Problema e questão norteadora

Prédios públicos municipais, em geral, oferecem acesso à internet a servidores e, por vezes, a visitantes, sem qualquer mecanismo de filtragem, deixando a rede vulnerável a ameaças digitais e sem meios de coibir o acesso a conteúdo incompatível com o ambiente de trabalho e com a moralidade administrativa. Ao mesmo tempo, a escassez de orçamento e de pessoal técnico dificulta a adoção de soluções comerciais. Assim, a pesquisa será guiada pela seguinte questão norteadora: **em que medida a implantação do Pi-hole em um servidor local, como filtro DNS, é capaz de controlar o acesso de servidores públicos a sítios indevidos e maliciosos na rede de um prédio público municipal, com baixo custo e sem prejudicar o desempenho da navegação?**

## 1.2 Justificativa

A relevância social do estudo reside na proteção do patrimônio informacional público e na promoção do uso adequado de um recurso custeado pelo contribuinte. Ao bloquear domínios maliciosos antes mesmo que a conexão seja estabelecida, a filtragem DNS reduz a superfície de ataque da rede e atua como uma camada preventiva contra *ransomware* e *phishing*, ameaças que, como visto, já paralisaram serviços de prefeituras brasileiras (ARRUDA, 2025). Ao bloquear categorias de conteúdo impróprio, contribui para que a administração cumpra os princípios constitucionais da moralidade e da eficiência e para que disponha de evidências técnicas, ainda que agregadas, em casos de uso indevido.

A relevância institucional decorre do alinhamento com as políticas públicas de segurança da informação. A Política Nacional de Segurança da Informação (BRASIL, 2025a), a Política Nacional de Cibersegurança (BRASIL, 2023) e a Estratégia Nacional de Cibersegurança (BRASIL, 2025b) estabelecem diretrizes para a proteção dos ativos de informação na administração pública, e o Programa de Privacidade e Segurança da Informação (PPSI), da Secretaria de Governo Digital, organiza seus controles com base no CIS Controls, incluindo o controle dedicado às proteções de *e-mail* e de navegador *web* (BRASIL, 2024). Embora tais normas sejam voltadas prioritariamente à esfera federal, servem de referência para estados e municípios, que carecem de modelos práticos e acessíveis para aplicá-las.

A relevância acadêmica está em produzir um estudo aplicado, com avaliação mensurável, sobre uma ferramenta amplamente utilizada em ambientes domésticos, mas ainda pouco investigada em contextos institucionais públicos. A literatura recente começa a explorar o Pi-hole em ambientes educacionais (ELAVARASI *et al.*, 2026), porém não foram localizados, no levantamento preliminar, estudos voltados especificamente à administração pública municipal brasileira, com suas particularidades legais, como a necessidade de conciliar o controle de acesso com a Lei Geral de Proteção de Dados Pessoais (BRASIL, 2018).

Por fim, a escolha do tema relaciona-se com a formação no curso de Tecnologia em Análise e Desenvolvimento de Sistemas, especialmente com os conteúdos de redes de computadores, sistemas operacionais e segurança da informação, e com a necessidade observada de evitar o uso indevido das redes públicas de internet, o que motivou a busca por uma solução acessível de controle de acesso.

## 1.3 Hipóteses

A pesquisa será norteada pelas hipóteses abaixo, que, no percurso da investigação, serão confirmadas ou refutadas:

a) o Pi-hole, instalado em servidor local e configurado com listas de bloqueio por categoria, bloqueia a maior parte dos domínios de teste das categorias definidas, com baixa incidência de bloqueios indevidos de serviços legítimos e sem aumento perceptível no tempo de resposta das consultas DNS;

b) o recurso de gerenciamento de grupos do Pi-hole permite aplicar políticas de filtragem diferenciadas por setor ou segmento da rede, sem custo de licenciamento;

c) a eficácia do Pi-hole como ferramenta de controle depende de medidas complementares no roteador ou *firewall*, como o bloqueio de servidores DNS externos e de serviços conhecidos de DNS cifrado, sem as quais o filtro pode ser facilmente contornado.

# 2 OBJETIVOS

Os objetivos a seguir orientam o desenvolvimento da pesquisa.

## 2.1 Objetivo Geral

Avaliar a eficácia do Pi-hole, implantado em servidor local, como ferramenta de segurança e de controle de acesso a conteúdos indevidos na rede de um prédio público municipal de Sítio Novo/MA.

## 2.2 Objetivos Específicos

Para alcançar o objetivo geral, serão realizadas as seguintes ações:

a) diagnosticar a infraestrutura de rede e as práticas de uso da internet no prédio público municipal selecionado;

b) implantar e configurar o Pi-hole em servidor local, com listas de bloqueio por categoria, grupos por setor e medidas complementares contra o contorno do filtro;

c) mensurar a eficácia do bloqueio, a ocorrência de falsos positivos e o impacto no desempenho das consultas DNS por meio de testes em ambiente controlado;

d) elaborar um modelo documentado de implantação e uma minuta de política de uso aceitável da internet, passíveis de replicação em outros prédios da administração municipal.

# 3 REFERENCIAL TEÓRICO

Esta seção reúne os conceitos que sustentam a pesquisa, partindo do contexto mais amplo da segurança da informação na administração pública até chegar às características técnicas e aos limites do Pi-hole, objeto central do estudo.

## 3.1 Segurança da informação na administração pública

A segurança da informação é tradicionalmente definida pela preservação de três propriedades: confidencialidade, integridade e disponibilidade. Stallings e Brown (2014) destacam que essas propriedades não são garantidas por um único mecanismo, mas por um conjunto de controles sobrepostos, organizados em camadas, de modo que a falha de um deles seja compensada pelos demais. Essa noção de defesa em profundidade é fundamental para esta pesquisa, pois a filtragem DNS não pretende substituir antivírus, atualizações ou *backups*, e sim acrescentar uma camada preventiva situada antes do estabelecimento da conexão.

No plano normativo, a ABNT NBR ISO/IEC 27001 estabelece os requisitos de um sistema de gestão da segurança da informação baseado em análise de riscos (ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS, 2022a), enquanto a ABNT NBR ISO/IEC 27002 detalha os controles aplicáveis, entre os quais se encontra a filtragem da *web*, voltada a reduzir a exposição a conteúdo malicioso e a impedir o acesso a recursos externos não autorizados (ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS, 2022b). O *Center for Internet Security* segue linha semelhante e, em seu conjunto de controles críticos, recomenda expressamente o uso de serviços de filtragem DNS para bloquear o acesso a domínios maliciosos conhecidos (CENTER FOR INTERNET SECURITY, 2024). A convergência entre essas referências indica que a filtragem de navegação é reconhecida como boa prática, e não como medida excepcional.

No Brasil, a Política Nacional de Segurança da Informação (BRASIL, 2025a), a Política Nacional de Cibersegurança (BRASIL, 2023) e a Estratégia Nacional de Cibersegurança (BRASIL, 2025b) definem princípios e objetivos para a proteção dos ativos de informação do Estado. Para operacionalizá-los, a Secretaria de Governo Digital criou o PPSI, cujo guia de *framework* adota o CIS Controls como base e inclui um controle específico para proteções de *e-mail* e navegador *web* (BRASIL, 2024). Há, contudo, uma lacuna entre esse arcabouço, pensado para órgãos federais com equipes estruturadas, e a realidade municipal. O aumento dos incidentes contra órgãos públicos (ARRUDA, 2025) reforça a necessidade de soluções simples, de baixo custo e documentadas, que traduzam essas diretrizes para a escala de um prédio municipal. É nesse espaço que se insere a presente proposta.

## 3.2 O sistema de nomes de domínio (DNS)

Para compreender por que o DNS é um ponto estratégico de controle, é necessário entender seu papel. O DNS é o serviço que traduz nomes de domínio legíveis por humanos, como "www.exemplo.gov.br", em endereços IP utilizados pelos equipamentos de rede. Sua arquitetura foi especificada por Mockapetris (1987a, 1987b) como uma base de dados hierárquica e distribuída, na qual servidores raiz, servidores de domínio de topo e servidores autoritativos cooperam para responder às consultas. Kurose e Ross (2021) explicam que, na prática, o computador do usuário envia a consulta a um servidor DNS local, normalmente informado pelo protocolo DHCP, que realiza a resolução em nome do cliente e armazena as respostas em *cache* para acelerar consultas futuras. A terminologia adotada neste trabalho segue a consolidação mais recente publicada pelo IETF (HOFFMAN; FUJIWARA, 2024).

Essa característica é o que torna o DNS um ponto de controle privilegiado. Como praticamente toda comunicação na internet começa com uma consulta DNS, quem controla o servidor DNS local consegue decidir, antes de qualquer conexão, quais nomes serão resolvidos e quais não serão. Tanenbaum, Feamster e Wetherall (2021) observam que o DNS foi concebido sem mecanismos nativos de segurança, o que o expõe a ataques como envenenamento de *cache* e redirecionamento malicioso; a mesma fragilidade, no entanto, é explorada de forma defensiva pela filtragem DNS. Khormali *et al.* (2020), em revisão sobre segurança e privacidade do DNS, mostram que o protocolo é simultaneamente vetor de ataques, como tunelamento de dados e uso de domínios gerados algoritmicamente por *malware*, e fonte valiosa de observação para defesa, justamente por concentrar a intenção de acesso de todos os dispositivos da rede.

## 3.3 Filtragem baseada em DNS e *DNS sinkhole*

A filtragem DNS consiste em interceptar as consultas da rede e comparar o domínio solicitado com listas de bloqueio. Quando o domínio consta da lista, o servidor devolve uma resposta nula ou um endereço inválido, técnica chamada de *DNS sinkhole*, e o dispositivo simplesmente não consegue estabelecer a conexão. A Agência de Segurança Nacional e a Agência de Segurança Cibernética e de Infraestrutura dos Estados Unidos denominam esse tipo de serviço de *Protective DNS* e recomendam sua adoção por permitir bloquear, em um único ponto, o acesso a domínios de *malware*, *phishing* e comando e controle, além de produzir registros úteis para a detecção de incidentes (NATIONAL SECURITY AGENCY; CYBERSECURITY AND INFRASTRUCTURE SECURITY AGENCY, 2021). A revisão mais recente do guia de implantação segura de DNS do NIST também incorpora o *Protective DNS* entre as práticas recomendadas para organizações (ROSE; LIU; GIBSON, 2026).

O CIS Controls v8.1 distingue a filtragem de DNS (salvaguarda 9.2), que bloqueia domínios maliciosos conhecidos, dos filtros de URL em nível de rede (salvaguarda 9.3), distinção que delimita o que o Pi-hole resolve e o que exigiria controles adicionais (CENTER FOR INTERNET SECURITY, 2024). A eficácia desse modelo, porém, depende diretamente da qualidade das listas utilizadas. Kührer, Rossow e Holz (2014), ao avaliarem listas públicas de domínios maliciosos, constataram que elas apresentam coberturas muito distintas, que nenhuma lista isolada é suficiente e que a atualização frequente é decisiva, pois domínios maliciosos têm vida curta. Para a filtragem de categorias de conteúdo, como sítios adultos e de apostas, existem listas mantidas por comunidades e instituições, como o repositório *hosts* de Steven Black, que consolida diversas fontes e oferece extensões para pornografia e jogos de azar (BLACK, 2025), e as listas UT1 da Universidade Toulouse Capitole, organizadas por categorias como adulto, apostas, *malware* e *phishing* (UNIVERSITÉ TOULOUSE CAPITOLE, 2025). Essas evidências justificam uma das escolhas metodológicas desta pesquisa: avaliar a combinação de listas, e não uma única fonte, e medir explicitamente tanto a taxa de bloqueio quanto a ocorrência de falsos positivos.

## 3.4 O Pi-hole: arquitetura e funcionalidades

O Pi-hole é um software livre que implementa um *DNS sinkhole* para toda a rede local. Seu núcleo, o FTL (*Faster Than Light*), derivado do servidor dnsmasq, responde às consultas, consulta um banco de dados denominado *gravity*, que reúne os domínios das listas assinadas, e encaminha ao servidor DNS superior (*upstream*) apenas as consultas permitidas (PI-HOLE, 2025a). A versão 6, lançada em fevereiro de 2025, incorporou servidor *web* e API REST ao próprio FTL, eliminando dependências como lighttpd e PHP, unificou a configuração em um único arquivo e passou a oferecer suporte nativo a HTTPS e a listas de permissão por assinatura (PI-HOLE, 2025b). O Pi-hole também é distribuído como imagem Docker, forma que não será avaliada neste trabalho. Como o filtro atua no servidor, todos os dispositivos que usam o Pi-hole como DNS ficam protegidos sem instalação de *software* nas estações.

Entre as funcionalidades relevantes para o contexto desta pesquisa, destacam-se: o gerenciamento de grupos, que permite associar clientes, identificados por endereço IP, MAC ou sub-rede, a conjuntos distintos de listas e regras; o bloqueio por expressões regulares; as listas de permissão, úteis para garantir o funcionamento de sistemas governamentais; o painel de estatísticas e o registro de consultas; e os níveis de privacidade, que permitem ocultar domínios e clientes nos registros (PI-HOLE, 2025a). Este último recurso é particularmente importante na administração pública, pois possibilita equilibrar a necessidade de auditoria com os princípios de necessidade e de minimização de dados previstos na LGPD (BRASIL, 2018). O Pi-hole pode, ainda, trabalhar em conjunto com o Unbound, um resolvedor recursivo com validação DNSSEC, que permite à rede resolver nomes diretamente a partir dos servidores raiz, sem depender de provedores externos de DNS (NLNET LABS, 2025).

No campo acadêmico, Elavarasi *et al.* (2026) implantaram o Pi-hole em uma rede educacional e o compararam com *firewall*, *proxy* e extensões de navegador, concluindo que ele apresentou o melhor equilíbrio entre facilidade de implantação, custo e cobertura de dispositivos, embora com capacidade inferior à de um *firewall* corporativo em redes de grande porte. Os autores utilizaram um Raspberry Pi como servidor; a presente pesquisa diferencia-se ao adotar um servidor local convencional, com mais recursos, e ao transpor o estudo para o contexto da administração pública municipal, com suas exigências legais e de gestão.

## 3.5 Limites da filtragem DNS e medidas complementares

Reconhecer os limites da ferramenta é condição para avaliá-la de forma honesta. O primeiro limite é que a filtragem DNS bloqueia domínios, e não conteúdos: não é possível, por exemplo, bloquear um vídeo específico em uma plataforma permitida. O segundo, e mais relevante, é a possibilidade de contorno. Um usuário pode configurar manualmente outro servidor DNS na estação, utilizar uma VPN ou recorrer a protocolos de DNS cifrado. O DNS sobre TLS (DoT) utiliza uma porta própria, a 853 (HU *et al.*, 2016), o que facilita seu bloqueio, enquanto o DNS sobre HTTPS (DoH) trafega pela mesma porta 443 usada na navegação comum (HOFFMAN; MCMANUS, 2018), o que o torna difícil de distinguir do restante do tráfego. Hounsel *et al.* (2020) mostram que esses protocolos já estão integrados aos principais navegadores, e a CISA alerta que recursos de DNS cifrado ativados por padrão em aplicativos e sistemas operacionais podem desviar as consultas dos controles de DNS da organização (CYBERSECURITY AND INFRASTRUCTURE SECURITY AGENCY, 2024). O DNS sobre QUIC (DoQ), padronizado em 2022, oferece confidencialidade comparável à do DoT sobre outro transporte (HUITEMA; DICKINSON; MANKIN, 2022); por restrição de escopo, os testes de contorno se limitarão a DNS externo configurado manualmente, DoT e DoH, e o DoQ será registrado como limitação.

A literatura aponta, portanto, que a filtragem DNS precisa ser acompanhada de medidas no perímetro da rede. A Cybersecurity and Infrastructure Security Agency (2024) recomenda bloquear o tráfego para provedores conhecidos de DoH e restringir o uso de servidores DNS não autorizados, e Elavarasi *et al.* (2026) chegam à mesma conclusão, ao indicar que o Pi-hole deve ser combinado com redirecionamento forçado de DNS e regras de *firewall*. Esse conjunto de evidências fundamenta a terceira hipótese desta pesquisa e orienta o desenho dos testes de contorno descritos na metodologia.

## 3.6 Aspectos legais e éticos do controle de acesso

O controle da navegação em uma rede pública envolve, inevitavelmente, o tratamento de dados. O Marco Civil da Internet estabelece princípios como a proteção da privacidade e dos dados pessoais no uso da internet (BRASIL, 2014), e a LGPD determina que o tratamento de dados pelo poder público deve atender à sua finalidade pública e observar os princípios da finalidade, da necessidade e da transparência (BRASIL, 2018). Os registros de consultas DNS, ao associarem um endereço IP a um domínio acessado, podem configurar dados pessoais quando permitirem identificar o servidor que os gerou. Por isso, a proposta deve definir com clareza a finalidade dos registros, o período de retenção e quem terá acesso a eles, e comunicar a existência do filtro aos usuários por meio de uma política de uso aceitável. O guia orientativo da ANPD sobre o tratamento de dados pessoais pelo poder público detalha a aplicação das bases legais e dos princípios da LGPD a órgãos públicos (AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS, 2023a), e o guia sobre fins acadêmicos orienta o tratamento de dados em estudos e pesquisas (AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS, 2023b).

Ao mesmo tempo, o ordenamento jurídico reforça a pertinência do bloqueio de determinados conteúdos. O Estatuto da Criança e do Adolescente tipifica como crime, entre outras condutas, adquirir, possuir ou armazenar material que contenha cena de sexo explícito ou pornográfica envolvendo criança ou adolescente (BRASIL, 1990), e a Lei nº 12.737/2012 tipifica delitos informáticos, como a invasão de dispositivo informático (BRASIL, 2012). A filtragem não substitui a apuração dessas condutas pelas autoridades competentes, mas reduz a possibilidade de que a infraestrutura pública seja utilizada para praticá-las. O desafio que emerge da literatura e da legislação, e que esta pesquisa pretende enfrentar, é construir um mecanismo de controle eficaz que seja, ao mesmo tempo, proporcional, transparente e respeitoso à privacidade dos servidores.

# 4 METODOLOGIA

Esta seção descreve como a pesquisa será desenvolvida, articulando cada procedimento aos objetivos específicos e ao problema de pesquisa.

## 4.1 Caracterização da pesquisa

Quanto à natureza, a pesquisa é aplicada, pois busca gerar conhecimento voltado à solução de um problema concreto (GIL, 2022). Quanto à abordagem, é quali-quantitativa: qualitativa no diagnóstico do ambiente e na análise da entrevista; quantitativa na mensuração da eficácia de bloqueio, dos falsos positivos e do tempo de resposta DNS. Quanto aos objetivos, é exploratória, por investigar um tema ainda pouco estudado no contexto municipal, e descritiva, por registrar sistematicamente as características do ambiente e o comportamento da solução (GIL, 2022). Quanto aos procedimentos, combina pesquisa bibliográfica e documental, estudo de caso, aplicado a um prédio público específico, e testes em ambiente controlado (MARCONI; LAKATOS, 2022; WAZLAWICK, 2014).

Como método orientador, será adotada a *Design Science Research* (DSR), adequada a pesquisas que têm como resultado a construção e a avaliação de um artefato destinado a resolver um problema real (HEVNER *et al.*, 2004). Peffers *et al.* (2007) propõem processo em seis atividades (identificação do problema e motivação, definição dos objetivos da solução, projeto e desenvolvimento, demonstração, avaliação e comunicação), que orienta a sequência das etapas do Quadro 1. Dresch, Lacerda e Antunes Júnior (2015) organizam a DSR em etapas de identificação do problema, conscientização, proposição, projeto e desenvolvimento do artefato, avaliação, explicitação das aprendizagens e comunicação dos resultados. Neste projeto, o artefato é o modelo de implantação do Pi-hole, composto pela configuração do servidor, pelas listas e grupos, pelas regras complementares de rede e pela documentação de replicação.

## 4.2 Local, objeto de estudo e participantes

O estudo será realizado no prédio-sede da Secretaria Municipal de Educação de Sítio Novo/MA, situado na Avenida Leonardo de Almeida, s/nº, Centro, que conta com aproximadamente 14 estações de trabalho, conectadas em sua maior parte por rede cabeada com cabeamento de categoria 5e, além de rede sem fio (*Wi-Fi*), sendo a distribuição de endereços (DHCP) e o acesso à internet realizados por um roteador TP-Link Aginet EX511 (*Wi-Fi* 6, *Dual-Band* AX3000). O objeto de estudo é o serviço de resolução de nomes (DNS) da rede local e o comportamento do Pi-hole como filtro desse serviço. Os participantes diretos serão o(s) responsável(is) técnico(s) pela rede, que responderão à entrevista de diagnóstico. Os demais servidores não serão sujeitos individuais da pesquisa: apenas estatísticas agregadas e anonimizadas do tráfego DNS serão analisadas, caso o piloto seja autorizado.

A fim de garantir a exequibilidade no prazo disponível, os testes de eficácia e desempenho serão realizados em ambiente de homologação montado com equipamentos do próprio órgão ou dos pesquisadores, reproduzindo a configuração da rede diagnosticada. A implantação em produção, em um único setor e por período limitado, será realizada somente mediante autorização formal da instituição.

## 4.3 Etapas e procedimentos

O Quadro 1 relaciona as etapas da pesquisa às fases da DSR e aos objetivos específicos.

[[QUADRO|1|Etapas da pesquisa, fases da DSR e objetivos específicos]]
| Etapa | Fase da DSR | Procedimentos | Objetivo |
|---|---|---|---|
| 1. Levantamento bibliográfico e documental | Conscientização | Revisão de livros, artigos, normas técnicas, legislação e documentação oficial do Pi-hole | Todos |
| 2. Diagnóstico da rede | Identificação do problema | Entrevista semiestruturada (Apêndice A) e *checklist* de infraestrutura (Apêndice B) | a |
| 3. Projeto e implantação | Proposição, projeto e desenvolvimento | Instalação do Linux e do Pi-hole no servidor local, configuração de listas, grupos, permissões e regras de rede | b |
| 4. Testes em ambiente controlado | Avaliação | Testes de bloqueio, de falsos positivos, de desempenho e de contorno | c |
| 5. Piloto (se autorizado) | Avaliação | Operação por 15 dias em um setor, com coleta de estatísticas agregadas | c |
| 6. Análise e documentação | Explicitação das aprendizagens e comunicação | Estatística descritiva, análise de conteúdo, redação do modelo de implantação e da minuta de política | d |
Fonte: Elaborado pelos autores (2026).

A avaliação do artefato segue o *framework* FEDS, de Venable, Pries-Heje e Baskerville (2016), que classifica as avaliações quanto ao propósito (formativa ou somativa) e ao paradigma (artificial ou naturalista). Os testes em ambiente de homologação constituem avaliação artificial e formativa, que permite corrigir o artefato; o piloto, quando autorizado, constitui avaliação naturalista e somativa. Caso o piloto não seja autorizado, a conclusão se apoiará na avaliação em homologação, e as limitações decorrentes serão registradas.

Na etapa 3, o servidor local receberá um sistema operacional Linux de suporte estendido (Debian 12 ou Ubuntu Server 24.04 LTS), sem interface gráfica, instalado em computador reaproveitado, endereço IP fixo e a versão estável mais recente do Pi-hole, instalada diretamente no sistema, sem contêineres, pela simplicidade da configuração de rede e pela facilidade de replicação por equipes pequenas. O acesso ao painel de administração será restrito, por regra de *firewall* do servidor, às estações da administração, com senha forte e HTTPS. O computador será configurado para reiniciar após queda de energia e terá cópia periódica de suas configurações. Serão configuradas listas de bloqueio por categoria, a partir das fontes discutidas na seção 3.3, uma lista local de domínios indesejados, definida com o responsável pelo setor e aplicada apenas ao grupo de clientes desse setor, uma lista de permissão com domínios de sistemas utilizados pelo órgão e, ao menos, dois grupos de clientes com políticas distintas. No roteador ou *firewall*, será configurado o DHCP para distribuir o Pi-hole como DNS da rede e serão criadas regras que bloqueiem consultas DNS (portas 53 e 853) destinadas a servidores externos, exceto as originadas pelo próprio Pi-hole.

Na etapa 4, os testes seguirão o protocolo descrito no Quadro 2.

[[QUADRO|2|Testes, indicadores e instrumentos de coleta]]
| Teste | Procedimento | Indicador | Instrumento |
|---|---|---|---|
| Eficácia de bloqueio | Consultar uma amostra de domínios por categoria (sexual, apostas, *malware*/*phishing* e conteúdo criminoso), extraída de fontes independentes das listas utilizadas, com tamanho, origem, data de coleta e critério de classificação registrados | Taxa de bloqueio (%) por categoria | Comando dig e registro de consultas do Pi-hole |
| Falsos positivos | Consultar uma amostra de domínios legítimos usados pelo órgão (gov.br, bancos, sistemas de saúde, educação e tributação) | Taxa de bloqueio indevido (%) | Comando dig e lista de verificação |
| Desempenho | Medir o tempo de resposta de um mesmo conjunto de consultas com o DNS atual e com o Pi-hole, com *cache* frio e aquecido, em medições repetidas | Mediana e dispersão do tempo de resposta (ms) | Comando dig ou ferramenta de *benchmark* DNS |
| Contorno | Tentar usar DNS externo configurado manualmente e DoH no navegador, antes e depois das regras de *firewall* | Sucesso ou falha do contorno | Roteiro de testes e registro em planilha |
| Custo | Registrar o custo de aquisição ou aproveitamento do servidor, o tempo de configuração, a manutenção necessária e, se viável, o consumo elétrico estimado | Custo (R$), tempo (h) e consumo estimado (kWh/mês) | Registro de implantação |
| Confiabilidade | Simular a indisponibilidade do servidor Pi-hole e uma regra de *firewall* incorreta, o desligamento abrupto do computador e a restauração da cópia de configuração, registrando o comportamento da rede e a recuperação, e verificar que o painel não abre em estação comum | Tempo de recuperação e comportamento da rede | Roteiro de testes e registro em planilha |
| Grupos | Verificar se clientes de grupos diferentes recebem políticas diferentes | Conformidade com a política (sim/não) | Registro de consultas do Pi-hole |
Fonte: Elaborado pelos autores (2026).

Os critérios de avaliação, definidos antes da execução dos testes e a serem validados com o orientador, não são resultados esperados nem garantidos; são eles: taxa de bloqueio igual ou superior a 90% nas categorias testadas; taxa de falsos positivos inferior a 2% na amostra de domínios legítimos; e acréscimo inferior a 10% no tempo mediano de resposta em relação ao DNS atualmente utilizado.

No diagnóstico da etapa 2, será confirmado se o roteador TP-Link Aginet EX511 permite definir o DNS distribuído por DHCP e criar regras de saída que bloqueiem DNS externo; caso não permita, serão documentadas alternativas, como o uso de um *firewall* adicional ou do próprio servidor como DHCP. Ressalta-se que o Pi-hole bloqueia nomes de domínio das categorias escolhidas, e não o conteúdo das páginas, de modo que os resultados não permitirão afirmar que o acesso a conteúdo indevido foi impedido por completo nem que os riscos de *malware* e *phishing* foram eliminados.

## 4.4 Proposta tecnológica preliminar

Esta subseção antecipa a solução que será construída e avaliada. Os detalhes definitivos dependerão do diagnóstico da etapa 2. A Figura 1 apresenta a arquitetura proposta.

[[FIGURA|1|Arquitetura proposta para a filtragem DNS com Pi-hole|arquitetura.png]]
Fonte: Elaborado pelos autores (2026).

A solução é composta por quatro elementos:

a) servidor local: computador reaproveitado com Linux em edição servidor, endereço IP fixo, Pi-hole instalado de forma nativa e, opcionalmente, Unbound como resolvedor recursivo;

b) políticas de filtragem: listas de bloqueio por categoria, lista local de domínios indesejados definida com cada setor, expressões regulares, lista de permissão para sistemas governamentais e grupos, por exemplo, "Administração", "Atendimento" e "Visitantes", com regras distintas;

c) medidas complementares de rede: DHCP do roteador apontando o Pi-hole como único DNS e regras de *firewall* que bloqueiem DNS externo (portas 53 e 853) e domínios conhecidos de DoH;

d) gestão e governança: painel de acompanhamento com acesso restrito às estações de administração, nível de privacidade definido, retenção limitada de registros, *backup* periódico das configurações e minuta de política de uso aceitável da internet, a ser apresentada à gestão municipal.

Além do controle de conteúdo, a solução agrega outras funcionalidades de segurança e de gestão: bloqueio de domínios de *malware* e *phishing*, bloqueio de anúncios e rastreadores, com redução do consumo de banda, e geração de estatísticas de uso que apoiam a tomada de decisão. Como possível desdobramento, caso o cronograma permita, poderá ser desenvolvido um pequeno painel de relatórios gerenciais em PHP que consuma a API REST do Pi-hole e apresente indicadores agregados à gestão, sem expor dados individuais.

## 4.5 Análise dos dados

Os dados quantitativos serão organizados em planilhas e analisados por estatística descritiva, com cálculo de frequências, percentuais, médias e medianas, e apresentados em tabelas e gráficos. As respostas da entrevista serão examinadas por meio de análise de conteúdo, com categorização temática (BARDIN, 2016), de modo a identificar necessidades, restrições e expectativas do órgão em relação ao controle de acesso. A confrontação entre os resultados dos testes e as hipóteses permitirá confirmá-las ou refutá-las e responder à questão norteadora.

## 4.6 Aspectos éticos

A pesquisa será iniciada somente após a obtenção de termo de anuência da instituição. A entrevista com o responsável técnico tratará exclusivamente da infraestrutura e dos procedimentos do órgão, e o entrevistado assinará termo de consentimento livre e esclarecido. Os registros do Pi-hole utilizados na análise serão agregados e anonimizados, com o uso dos níveis de privacidade da própria ferramenta, sem identificação de servidores, em conformidade com a LGPD (BRASIL, 2018). Os registros terão como finalidade exclusiva a avaliação do filtro e a segurança da rede, com acesso restrito ao responsável técnico e aos pesquisadores, prazo de retenção definido com a instituição e limitado ao necessário para a pesquisa, e exclusão ao término do estudo (AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS, 2023a, 2023b). A necessidade de submissão ao Comitê de Ética em Pesquisa será verificada com o orientador, à luz da Resolução nº 510/2016 do Conselho Nacional de Saúde (BRASIL, 2016).

# 5 CRONOGRAMA

O Quadro 3 apresenta a distribuição das atividades ao longo do período de execução, de outubro de 2026 a março de 2027, que poderá ser ajustada ao calendário acadêmico do curso e à autorização da instituição para a realização do piloto.

[[QUADRO|3|Cronograma de execução da pesquisa]]
| Atividades | Out. | Nov. | Dez. | Jan. | Fev. | Mar. |
|---|---|---|---|---|---|---|
| Levantamento bibliográfico e documental | ● | ● | ● |  |  |  |
| Elaboração e entrega do projeto de pesquisa | ● | ● |  |  |  |  |
| Orientações com o orientador | ● | ● | ● | ● | ● | ● |
| Obtenção do termo de anuência e diagnóstico da rede |  |  | ● |  |  |  |
| Implantação do Pi-hole em ambiente de homologação |  |  | ● | ● |  |  |
| Testes de bloqueio, desempenho e contorno |  |  |  | ● |  |  |
| Piloto em um setor (se autorizado) |  |  |  | ● | ● |  |
| Análise dos dados |  |  |  |  | ● |  |
| Elaboração da proposta tecnológica e do texto final |  |  |  |  | ● | ● |
| Apresentação à banca examinadora |  |  |  |  |  | ● |
Fonte: Elaborado pelos autores (2026).

# REFERÊNCIAS

ARRUDA, Guilherme. Ciberataques no Brasil em 2025: prejuízos e falhas expostas. **WeLiveSecurity**, [*s. l.*], 25 ago. 2025. Disponível em: https://www.welivesecurity.com/pt/seguranca-digital/ciberataques-no-brasil-em-2025-prejuizos-e-falhas-expostas/. Acesso em: 26 out. 2026.

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **ABNT NBR ISO/IEC 27001**: segurança da informação, segurança cibernética e proteção à privacidade: sistemas de gestão da segurança da informação: requisitos. Rio de Janeiro: ABNT, 2022a.

ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS. **ABNT NBR ISO/IEC 27002**: segurança da informação, segurança cibernética e proteção à privacidade: controles de segurança da informação. Rio de Janeiro: ABNT, 2022b.

AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS. **Tratamento de dados pessoais pelo Poder Público**: guia orientativo. Versão 2.0. Brasília, DF: ANPD, jun. 2023a. Disponível em: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-poder-publico-anpd-versao-final.pdf. Acesso em: 28 out. 2026.

AUTORIDADE NACIONAL DE PROTEÇÃO DE DADOS. **Tratamento de dados pessoais para fins acadêmicos e para a realização de estudos e pesquisas**: guia orientativo. Brasília, DF: ANPD, 2023b. Disponível em: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-tratamento-de-dados-pessoais-para-fins-academicos-e-para-a-realizacao-de-estudos-e-pesquisas. Acesso em: 28 out. 2026.

BARDIN, Laurence. **Análise de conteúdo**. São Paulo: Edições 70, 2016.

BLACK, Steven. **Hosts**: consolidating and extending hosts files from several well-curated sources. [*S. l.*]: GitHub, 2025. Disponível em: https://github.com/StevenBlack/hosts. Acesso em: 26 out. 2026.

BRASIL. Lei nº 8.069, de 13 de julho de 1990. Dispõe sobre o Estatuto da Criança e do Adolescente e dá outras providências. **Diário Oficial da União**: seção 1, Brasília, DF, 16 jul. 1990. Disponível em: https://www.planalto.gov.br/ccivil_03/leis/l8069.htm. Acesso em: 26 out. 2026.

BRASIL. Lei nº 12.737, de 30 de novembro de 2012. Dispõe sobre a tipificação criminal de delitos informáticos; altera o Decreto-Lei nº 2.848, de 7 de dezembro de 1940 - Código Penal; e dá outras providências. **Diário Oficial da União**: seção 1, Brasília, DF, 3 dez. 2012. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12737.htm. Acesso em: 26 out. 2026.

BRASIL. Lei nº 12.965, de 23 de abril de 2014. Estabelece princípios, garantias, direitos e deveres para o uso da Internet no Brasil. **Diário Oficial da União**: seção 1, Brasília, DF, 24 abr. 2014. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l12965.htm. Acesso em: 26 out. 2026.

BRASIL. Conselho Nacional de Saúde. Resolução nº 510, de 7 de abril de 2016. Dispõe sobre as normas aplicáveis a pesquisas em Ciências Humanas e Sociais. **Diário Oficial da União**: seção 1, Brasília, DF, 24 maio 2016. Disponível em: https://conselho.saude.gov.br/resolucoes/2016/Reso510.pdf. Acesso em: 26 out. 2026.

BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). **Diário Oficial da União**: seção 1, Brasília, DF, 15 ago. 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm. Acesso em: 26 out. 2026.

BRASIL. Decreto nº 11.856, de 26 de dezembro de 2023. Institui a Política Nacional de Cibersegurança e o Comitê Nacional de Cibersegurança. **Diário Oficial da União**: seção 1, Brasília, DF, 27 dez. 2023. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/decreto/d11856.htm. Acesso em: 26 out. 2026.

BRASIL. Ministério da Gestão e da Inovação em Serviços Públicos. Secretaria de Governo Digital. **Guia do framework de privacidade e segurança da informação**. Versão 1.1.3. Brasília, DF: SGD, 2024. Disponível em: https://www.gov.br/governodigital/pt-br/privacidade-e-seguranca/ppsi/guia_framework_psi.pdf. Acesso em: 26 out. 2026.

BRASIL. Decreto nº 12.572, de 4 de agosto de 2025. Institui a Política Nacional de Segurança da Informação e dispõe sobre a governança da segurança da informação. **Diário Oficial da União**: seção 1, Brasília, DF, 5 ago. 2025a. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/d12572.htm. Acesso em: 28 out. 2026.

BRASIL. Decreto nº 12.573, de 4 de agosto de 2025. Institui a Estratégia Nacional de Cibersegurança. **Diário Oficial da União**: seção 1, Brasília, DF, 5 ago. 2025b. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/decreto/d12573.htm. Acesso em: 28 out. 2026.

CENTER FOR INTERNET SECURITY. **CIS Critical Security Controls**: version 8.1. East Greenbush, NY: CIS, 2024. Disponível em: https://www.cisecurity.org/insights/white-papers/cis-critical-security-controls-v8-1. Acesso em: 26 out. 2026.

CENTRO REGIONAL DE ESTUDOS PARA O DESENVOLVIMENTO DA SOCIEDADE DA INFORMAÇÃO. **TIC Governo Eletrônico 2023**: pesquisa sobre o uso das tecnologias de informação e comunicação no setor público brasileiro: resumo executivo. São Paulo: Comitê Gestor da Internet no Brasil, 2024. Disponível em: https://cetic.br/media/docs/publicacoes/2/20240826104230/resumo_executivo_tic_governo_eletronico_2023.pdf. Acesso em: 26 out. 2026.

CYBERSECURITY AND INFRASTRUCTURE SECURITY AGENCY. **Encrypted DNS implementation guidance**. Version 1.0. Washington, DC: CISA, 2024. Disponível em: https://www.cisa.gov/sites/default/files/2024-05/Encrypted%20DNS%20Implementation%20Guidance_508c.pdf. Acesso em: 26 out. 2026.

DRESCH, Aline; LACERDA, Daniel Pacheco; ANTUNES JÚNIOR, José Antonio Valle. **Design science research**: método de pesquisa para avanço da ciência e tecnologia. Porto Alegre: Bookman, 2015.

ELAVARASI, R. *et al*. Enhancing network security and content control in academic environments using Pi-hole. **Journal of Applied Data Sciences**, [*s. l.*], v. 7, n. 3, p. 2504-2515, set. 2026. DOI: https://doi.org/10.47738/jads.v7i3.1472.

GIL, Antonio Carlos. **Como elaborar projetos de pesquisa**. 7. ed. Barueri, SP: Atlas, 2022.

HEVNER, Alan R. *et al*. Design science in information systems research. **MIS Quarterly**, Minneapolis, v. 28, n. 1, p. 75-105, 2004.

HOFFMAN, Paul; FUJIWARA, Kazunori. **RFC 9499**: DNS terminology. [*S. l.*]: IETF, 2024. DOI: https://doi.org/10.17487/RFC9499.

HOFFMAN, Paul; MCMANUS, Patrick. **RFC 8484**: DNS queries over HTTPS (DoH). [*S. l.*]: IETF, 2018. DOI: https://doi.org/10.17487/RFC8484.

HOUNSEL, Austin *et al*. Comparing the effects of DNS, DoT, and DoH on web performance. *In*: THE WEB CONFERENCE, 29., 2020, Taipei. **Proceedings** [...]. New York: ACM, 2020. DOI: https://doi.org/10.1145/3366423.3380139.

HU, Zi *et al*. **RFC 7858**: specification for DNS over Transport Layer Security (TLS). [*S. l.*]: IETF, 2016. DOI: https://doi.org/10.17487/RFC7858.

HUITEMA, Christian; DICKINSON, Sara; MANKIN, Allison. **RFC 9250**: DNS over dedicated QUIC connections. [*S. l.*]: IETF, 2022. DOI: https://doi.org/10.17487/RFC9250.

KHORMALI, Aminollah *et al*. Domain name system security and privacy: a contemporary survey. **arXiv**, [*s. l.*], 2020. Preprint arXiv:2006.15277. Disponível em: https://arxiv.org/abs/2006.15277. Acesso em: 26 out. 2026.

KÜHRER, Marc; ROSSOW, Christian; HOLZ, Thorsten. Paint it black: evaluating the effectiveness of malware blacklists. *In*: INTERNATIONAL SYMPOSIUM ON RESEARCH IN ATTACKS, INTRUSIONS AND DEFENSES, 17., 2014, Gothenburg. **Proceedings** [...]. Cham: Springer, 2014. p. 1-21. DOI: https://doi.org/10.1007/978-3-319-11379-1_1.

KUROSE, James F.; ROSS, Keith W. **Redes de computadores e a Internet**: uma abordagem top-down. 8. ed. Porto Alegre: Bookman, 2021.

MARCONI, Marina de Andrade; LAKATOS, Eva Maria. **Fundamentos de metodologia científica**. 9. ed. São Paulo: Atlas, 2022.

MOCKAPETRIS, Paul. **RFC 1034**: domain names: concepts and facilities. [*S. l.*]: IETF, 1987a. DOI: https://doi.org/10.17487/RFC1034.

MOCKAPETRIS, Paul. **RFC 1035**: domain names: implementation and specification. [*S. l.*]: IETF, 1987b. DOI: https://doi.org/10.17487/RFC1035.

NATIONAL SECURITY AGENCY; CYBERSECURITY AND INFRASTRUCTURE SECURITY AGENCY. **Selecting a protective DNS service**. Fort Meade, MD: NSA, 2021. Disponível em: https://www.nsa.gov/Press-Room/News-Highlights/Article/Article/2523771/nsa-and-cisa-release-cybersecurity-information-on-protective-dns/. Acesso em: 26 out. 2026.

NLNET LABS. **Unbound documentation**. Amsterdam: NLnet Labs, 2025. Disponível em: https://unbound.docs.nlnetlabs.nl/. Acesso em: 26 out. 2026.

PEFFERS, Ken *et al*. A design science research methodology for information systems research. **Journal of Management Information Systems**, [*s. l.*], v. 24, n. 3, p. 45-77, 2007. DOI: https://doi.org/10.2753/MIS0742-1222240302.

PI-HOLE. **Pi-hole documentation**. [*S. l.*]: Pi-hole, 2025a. Disponível em: https://docs.pi-hole.net/. Acesso em: 26 out. 2026.

PI-HOLE. **Introducing Pi-hole v6**. [*S. l.*]: Pi-hole, 18 fev. 2025b. Disponível em: https://pi-hole.net/blog/2025/02/18/introducing-pi-hole-v6/. Acesso em: 26 out. 2026.

ROSE, Scott; LIU, Cricket; GIBSON, Ross. **Secure Domain Name System (DNS) deployment guide**. Gaithersburg, MD: NIST, 2026. (NIST Special Publication 800-81r3). DOI: https://doi.org/10.6028/NIST.SP.800-81r3.

STALLINGS, William; BROWN, Lawrie. **Segurança de computadores**: princípios e práticas. 2. ed. Rio de Janeiro: Elsevier, 2014.

TANENBAUM, Andrew S.; FEAMSTER, Nick; WETHERALL, David J. **Redes de computadores**. 6. ed. Porto Alegre: Bookman, 2021.

UNIVERSITÉ TOULOUSE CAPITOLE. **Blacklists UT1**. Toulouse: Université Toulouse Capitole, 2025. Disponível em: https://dsi.ut-capitole.fr/blacklists/. Acesso em: 26 out. 2026.

VENABLE, John; PRIES-HEJE, Jan; BASKERVILLE, Richard. FEDS: a framework for evaluation in design science research. **European Journal of Information Systems**, [*s. l.*], v. 25, n. 1, p. 77-89, 2016. DOI: https://doi.org/10.1057/ejis.2014.36.

WAZLAWICK, Raul Sidnei. **Metodologia de pesquisa para ciência da computação**. 2. ed. Rio de Janeiro: Elsevier, 2014.

# APÊNDICE A – ROTEIRO DE ENTREVISTA SEMIESTRUTURADA COM O RESPONSÁVEL TÉCNICO PELA REDE

a) Qual é sua função e há quanto tempo é responsável pela rede deste prédio?

b) Quantos computadores, dispositivos e usuários utilizam a rede atualmente? Há rede sem fio para visitantes?

c) Qual equipamento faz a função de roteador, *firewall* e servidor DHCP? Qual servidor DNS é distribuído hoje aos computadores?

d) Existe alguma política formal de uso da internet ou de segurança da informação no órgão?

e) Já ocorreram incidentes de segurança, como vírus, *ransomware*, *phishing* ou sequestro de contas? Como foram tratados?

f) Há registros ou relatos de acesso a conteúdo indevido a partir da rede? Que tipo de conteúdo preocupa mais a gestão?

g) Existe algum mecanismo atual de bloqueio ou de monitoramento de navegação? Qual?

h) Quais sistemas e sítios eletrônicos são indispensáveis ao funcionamento do órgão e não podem ser bloqueados?

i) Quais restrições existem para a instalação de um servidor local, como disponibilidade de equipamento, energia, espaço e acesso administrativo ao roteador?

j) Que funcionalidades, além do bloqueio de conteúdo, seriam úteis para a gestão de TI do órgão?

# APÊNDICE B – CHECKLIST DE DIAGNÓSTICO DA REDE

[[QUADRO|4|Checklist de diagnóstico da infraestrutura de rede]]
| Item verificado | Situação encontrada | Observações |
|---|---|---|
| Topologia da rede (cabeada/sem fio, *switches*, segmentos) | | |
| Modelo do roteador/*firewall* e possibilidade de criar regras de saída | | |
| Servidor DHCP utilizado e DNS distribuído atualmente | | |
| Número de estações e de dispositivos móveis conectados | | |
| Existência de rede separada para visitantes | | |
| Equipamento disponível para o servidor local (CPU, RAM, disco) ou hipervisor | | |
| Disponibilidade de *nobreak* e local adequado para o servidor | | |
| Sistemas governamentais essenciais (lista de domínios a permitir) | | |
| Política de uso aceitável ou de segurança da informação vigente | | |
| Velocidade do *link* de internet e provedor | | |
Fonte: Elaborado pelos autores (2026).
