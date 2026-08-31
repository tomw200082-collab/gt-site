// Structural checks for the built page: every inline script must parse, and
// no HTML attribute may have been broken by a quote inside translated copy.
const fs = require('fs'), vm = require('vm'), path = require('path');
const file = path.join(__dirname, '..', 'src', 'index.html');
const s = fs.readFileSync(file, 'utf8');
let fail = 0;

const scripts = [...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
scripts.forEach((src, i) => {
  try { new vm.Script(src); console.log(`  ok   script ${i}  (${src.length} bytes)`); }
  catch (e) { fail++; console.log(`  FAIL script ${i}: ${e.message}`); }
});

// An unescaped " inside an attribute value would split the tag.
const badAttr = [...s.matchAll(/<[a-z][^>]*?=\s*"[^"]*"[^"=<>\s\/][^>]*>/gi)]
  .filter(m => !/^<(script|style)/i.test(m[0])).length;
console.log(`  ${badAttr === 0 ? 'ok  ' : 'FAIL'} attribute quoting (${badAttr} suspicious tags)`);
if (badAttr) fail++;

const pairs = [['<div', '</div>'], ['<section', '</section>'], ['<details', '</details>']];
for (const [o, c] of pairs) {
  const a = (s.match(new RegExp(o + '[\\s>]', 'g')) || []).length;
  const b = (s.match(new RegExp(c, 'g')) || []).length;
  console.log(`  ${a === b ? 'ok  ' : 'warn'} ${o}> ${a} / ${c} ${b}`);
}

console.log(`  ok   lang/dir: ${(s.match(/<html[^>]*>/) || [''])[0]}`);
process.exit(fail ? 1 : 0);
