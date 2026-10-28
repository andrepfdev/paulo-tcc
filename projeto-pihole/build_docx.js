// Gera o projeto de pesquisa (.docx) no padrão UEMA/ABNT a partir de projeto_pihole.md
// Uso: node build_docx.js [paginas.json] [saida.docx]
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel, Header,
  PageNumber, Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun,
  TabStopType, LeaderType, PageBreak, VerticalAlign, ShadingType,
} = require('docx');

const DIR = __dirname;
const SRC = path.join(DIR, 'projeto_pihole.md');
const pagesFile = process.argv[2];
const OUT = process.argv[3] || path.join(DIR, 'projeto.docx');
const pages = pagesFile && fs.existsSync(pagesFile) ? JSON.parse(fs.readFileSync(pagesFile, 'utf8')) : {};

const FONT = 'Arial';
const SZ = 24; // 12 pt
const SZ_SMALL = 20; // 10 pt
const LINE15 = 360; // 1,5
const LINE1 = 240;
const CM = 567; // twips por cm
const TEXT_W = Math.round((21 - 3 - 2) * CM); // 16 cm úteis

let raw = fs.readFileSync(SRC, 'utf8');
raw = raw.replace(/<!--[\s\S]*?-->/g, '');
// front matter
const fm = {};
const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n/);
if (fmMatch) {
  fmMatch[1].split('\n').forEach((l) => {
    const m = l.match(/^(\w+):\s*(.*)$/);
    if (m) fm[m[1]] = m[2].replace(/^"|"$/g, '');
  });
  raw = raw.slice(fmMatch[0].length);
}
// blocos pré-textuais
const blocks = {};
raw = raw.replace(/^::: (\w+)\n([\s\S]*?)\n:::\n/gm, (_, name, body) => { blocks[name] = body.trim(); return ''; });

// ---------- helpers de texto ----------
function runs(text, opts = {}) {
  // **negrito** e *itálico*
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0; let m;
  const size = opts.size || SZ;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size, bold: opts.bold, italics: opts.italics }));
    const t = m[0];
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), font: FONT, size, bold: true, italics: opts.italics }));
    else out.push(new TextRun({ text: t.slice(1, -1), font: FONT, size, italics: true, bold: opts.bold }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, size, bold: opts.bold, italics: opts.italics }));
  return out;
}
const P = (text, o = {}) => new Paragraph({
  alignment: o.align ?? AlignmentType.JUSTIFIED,
  spacing: { line: o.line ?? LINE15, before: o.before ?? 0, after: o.after ?? 0 },
  indent: o.indent ?? { firstLine: Math.round(1.25 * CM) },
  keepNext: o.keepNext,
  pageBreakBefore: o.pageBreakBefore,
  children: o.children ?? runs(text, o),
});
const blank = (line = LINE15) => new Paragraph({ spacing: { line }, children: [new TextRun({ text: '', font: FONT, size: SZ })] });
const center = (text, o = {}) => P(text, { ...o, align: AlignmentType.CENTER, indent: {} });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

// ---------- capa ----------
const titleRuns = (bold = true) => [
  new TextRun({ text: fm.titulo + (fm.subtitulo ? ': ' : ''), font: FONT, size: SZ, bold }),
  ...(fm.subtitulo ? [new TextRun({ text: fm.subtitulo, font: FONT, size: SZ, bold: false })] : []),
];
const capa = [
  center(fm.instituicao, { bold: true, line: LINE15 }),
  center(fm.nucleo, { bold: true }),
  center(fm.curso, { bold: true }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 2600, line: LINE15 }, children: runs(fm.autor, { bold: true }) }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 2600, line: LINE15 }, children: titleRuns() }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 4400, line: LINE15 }, children: runs(fm.local, { bold: true }) }),
  center(fm.ano, { bold: true }),
];
// ---------- folha de rosto ----------
const rosto = [
  new Paragraph({ alignment: AlignmentType.CENTER, pageBreakBefore: true, spacing: { line: LINE15 }, children: runs(fm.autor, { bold: true }) }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 3000, line: LINE15 }, children: titleRuns() }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { before: 900, line: LINE1 }, indent: { left: Math.round(8 * CM) },
    children: runs(`Projeto de pesquisa apresentado ao Curso de ${fm.curso_extenso} da Universidade Estadual do Maranhão, Núcleo de Tecnologias para Educação, como requisito para o desenvolvimento do Trabalho de Conclusão de Curso na modalidade Proposta Tecnológica, para obtenção do grau de ${fm.grau}.`),
  }),
  new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { before: 240, line: LINE1 }, indent: { left: Math.round(8 * CM) },
    children: runs(`Orientador(a): ${fm.orientador}.`),
  }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 3400, line: LINE15 }, children: runs(fm.local, { bold: true }) }),
  center(fm.ano, { bold: true }),
];
// ---------- resumo / abstract ----------
function resumoBlock(title, body, kwLabel) {
  const lines = body.split(/\n\s*\n/);
  const text = lines[0].replace(/\n/g, ' ');
  const kw = lines[1] || '';
  const [, kwText] = kw.match(/^[^:]+:\s*(.*)$/) || [null, kw];
  return [
    center(title, { bold: true, pageBreakBefore: true }),
    blank(),
    P(text, { indent: {} }),
    blank(),
    new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: LINE15 }, children: [new TextRun({ text: kwLabel + ': ', font: FONT, size: SZ, bold: true }), ...runs(kwText)] }),
  ];
}
const resumo = resumoBlock('RESUMO', blocks.resumo, 'Palavras-chave');
const abstract = resumoBlock('ABSTRACT', blocks.abstract, 'Keywords');
// ---------- siglas ----------
const siglas = [center('LISTA DE SIGLAS', { bold: true, pageBreakBefore: true }), blank()];
blocks.siglas.split('\n').forEach((l) => {
  const [s, d] = l.split('|').map((x) => x.trim());
  siglas.push(new Paragraph({
    spacing: { line: LINE15 }, tabStops: [{ type: TabStopType.LEFT, position: Math.round(2.5 * CM) }],
    indent: { left: Math.round(2.5 * CM), hanging: Math.round(2.5 * CM) },
    children: [new TextRun({ text: s, font: FONT, size: SZ }), new TextRun({ text: '\t', font: FONT, size: SZ }), ...runs(d)],
  }));
});

// ---------- corpo ----------
const lines = raw.split('\n');
const body = [];
const toc = []; // {level, num, text}
let firstPrimary = true;
let i = 0;
let pendingCaption = null; // para Fonte:

function headingPara(line) {
  const m = line.match(/^(#+)\s+(.*)$/);
  const level = m[1].length;
  const text = m[2].trim();
  const nm = text.match(/^(\d+(?:\.\d+)*)\s+(.*)$/);
  const num = nm ? nm[1] : '';
  const title = nm ? nm[2] : text;
  toc.push({ level, num, title });
  const unnumbered = !num;
  const children = [];
  if (num) children.push(new TextRun({ text: num + ' ', font: FONT, size: SZ, bold: true }));
  if (level === 1) children.push(...runs(title.toUpperCase().replace(/\*([^*]+)\*/g, '$1'), { bold: true }));
  else if (level === 2) children.push(...runs(title, { bold: true }));
  else children.push(...runs(title, { bold: true, italics: true }));
  return new Paragraph({
    heading: level === 1 ? HeadingLevel.HEADING_1 : level === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3,
    alignment: unnumbered ? AlignmentType.CENTER : AlignmentType.LEFT,
    pageBreakBefore: level === 1 && !(firstPrimary && !(firstPrimary = false)),
    keepNext: true,
    spacing: { line: LINE15, before: level === 1 ? 0 : 360, after: 360 },
    children,
  });
}

function parseTable(start) {
  const rows = [];
  let j = start;
  while (j < lines.length && lines[j].trim().startsWith('|')) {
    const cells = lines[j].trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
    if (!cells.every((c) => /^-+$/.test(c))) rows.push(cells);
    j++;
  }
  return { rows, next: j };
}
function buildTable(rows, colWeights) {
  const n = rows[0].length;
  const w = colWeights || Array(n).fill(1);
  const tot = w.reduce((a, b) => a + b, 0);
  const widths = w.map((x) => Math.floor((TEXT_W * x) / tot));
  widths[n - 1] += TEXT_W - widths.reduce((a, b) => a + b, 0);
  const border = { style: BorderStyle.SINGLE, size: 4, color: '000000' };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({
      tableHeader: ri === 0,
      cantSplit: true,
      children: r.map((c, ci) => new TableCell({
        width: { size: widths[ci], type: WidthType.DXA },
        borders,
        verticalAlign: VerticalAlign.CENTER,
        shading: ri === 0 ? { type: ShadingType.CLEAR, fill: 'E7E6E6', color: 'auto' } : undefined,
        margins: { top: 40, bottom: 40, left: 80, right: 80 },
        children: [new Paragraph({
          alignment: (n > 4 && ci > 0) || c === 'X' ? AlignmentType.CENTER : AlignmentType.LEFT,
          spacing: { line: LINE1 },
          children: runs(c, { size: SZ_SMALL, bold: ri === 0 }),
        })],
      })),
    })),
  });
}
const caption = (label, n, title) => new Paragraph({
  alignment: AlignmentType.LEFT, keepNext: true, spacing: { before: 240, line: LINE1, after: 60 },
  children: [new TextRun({ text: `${label} ${n} – `, font: FONT, size: SZ, bold: true }), ...runs(title)],
});
const fonte = (text) => new Paragraph({
  alignment: AlignmentType.LEFT, spacing: { before: 60, line: LINE1, after: 240 },
  children: runs(text, { size: SZ_SMALL }),
});

let inRefs = false;
let inAppendix = false;
const colWeightsByQuadro = { 1: [2.2, 1.6, 4, 0.9], 2: [1.4, 3.6, 1.8, 1.8], 3: [5, 1, 1, 1, 1, 1], 4: [4, 2.5, 2.5] };

while (i < lines.length) {
  const line = lines[i];
  const t = line.trim();
  if (!t) { i++; continue; }
  if (t.startsWith('#')) {
    const h = headingPara(t);
    inRefs = /^#\s+REFERÊNCIAS/.test(t);
    inAppendix = /^#\s+APÊNDICE/.test(t);
    body.push(h);
    i++; continue;
  }
  let m;
  if ((m = t.match(/^\[\[QUADRO\|(\d+)\|(.+)\]\]$/))) {
    body.push(caption('Quadro', m[1], m[2]));
    const { rows, next } = parseTable(i + 1);
    body.push(buildTable(rows, colWeightsByQuadro[m[1]]));
    i = next;
    continue;
  }
  if ((m = t.match(/^\[\[FIGURA\|(\d+)\|(.+)\|(.+)\]\]$/))) {
    body.push(caption('Figura', m[1], m[2]));
    const img = fs.readFileSync(path.join(DIR, m[3]));
    const wpx = 2400; const hpx = 2655;
    const targetW = 380; // pontos aproximados (~13,4 cm)
    body.push(new Paragraph({
      alignment: AlignmentType.CENTER, keepNext: true,
      children: [new ImageRun({ type: 'png', data: img, transformation: { width: targetW, height: Math.round(targetW * hpx / wpx) } })],
    }));
    i++; continue;
  }
  if (t.startsWith('Fonte:')) { body.push(fonte(t)); i++; continue; }
  if (t === '[[PAGEBREAK]]') { body.push(pageBreak()); i++; continue; }
  if (inRefs) {
    body.push(new Paragraph({ alignment: AlignmentType.LEFT, spacing: { line: LINE1, after: 240 }, children: runs(t) }));
    i++; continue;
  }
  if (/^[a-z]\)\s/.test(t)) {
    body.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED, spacing: { line: LINE15 },
      indent: { left: Math.round(1.25 * CM) + 340, hanging: 340 },
      children: runs(t),
    }));
    i++; continue;
  }
  body.push(P(t));
  i++;
}

// ---------- sumário ----------
const sumario = [center('SUMÁRIO', { bold: true, pageBreakBefore: true }), blank()];
toc.forEach((e) => {
  const label = e.num ? `${e.num} ` : '';
  const title = e.level === 1 ? e.title.toUpperCase().replace(/\*([^*]+)\*/g, '$1') : e.title.replace(/\*([^*]+)\*/g, '$1');
  const key = (e.num ? e.num + ' ' : '') + e.title;
  const pg = pages[key] !== undefined ? String(pages[key]) : '0';
  sumario.push(new Paragraph({
    spacing: { line: LINE15 },
    tabStops: [
      { type: TabStopType.LEFT, position: Math.round(1.3 * CM) },
      { type: TabStopType.RIGHT, position: TEXT_W, leader: LeaderType.DOT },
    ],
    indent: { left: e.num ? Math.round(1.3 * CM) : 0, hanging: e.num ? Math.round(1.3 * CM) : 0, right: Math.round(0.9 * CM) },
    children: [
      new TextRun({ text: label.trim(), font: FONT, size: SZ, bold: e.level === 1 }),
      new TextRun({ text: e.num ? '\t' : '', font: FONT, size: SZ }),
      new TextRun({ text: title, font: FONT, size: SZ, bold: e.level === 1, italics: e.level === 3 }),
      new TextRun({ text: '\t' + pg, font: FONT, size: SZ, bold: e.level === 1 }),
    ],
  }));
});
fs.writeFileSync(path.join(DIR, 'toc_keys.json'), JSON.stringify(toc.map((e) => ({ key: (e.num ? e.num + ' ' : '') + e.title, num: e.num, title: e.title, level: e.level })), null, 1));

// páginas pré-textuais contadas a partir da folha de rosto (capa não é contada)
const startPage = pages.__start || 6;

const pageProps = {
  size: { width: 11906, height: 16838 },
  margin: { top: Math.round(3 * CM), left: Math.round(3 * CM), bottom: Math.round(2 * CM), right: Math.round(2 * CM), header: Math.round(2 * CM) },
};

const doc = new Document({
  creator: fm.autor,
  title: `${fm.titulo}: ${fm.subtitulo}`,
  styles: {
    default: { document: { run: { font: FONT, size: SZ } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: SZ, bold: true, color: '000000' }, paragraph: { outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: SZ, bold: true, color: '000000' }, paragraph: { outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: SZ, bold: true, italics: true, color: '000000' }, paragraph: { outlineLevel: 2 } },
    ],
  },
  sections: [
    { properties: { page: pageProps }, children: [...capa, ...rosto, ...resumo, ...abstract, ...siglas, ...sumario] },
    {
      properties: { page: { ...pageProps, pageNumbers: { start: startPage } } },
      headers: {
        default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: SZ_SMALL })] })] }),
      },
      children: body,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log('ok', OUT); });
