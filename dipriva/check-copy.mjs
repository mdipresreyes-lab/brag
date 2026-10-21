#!/usr/bin/env node
// Dipriva copy check for /brag output: banned words, engagement bait, em dashes
// and dash substitutes, emoji. Same rules as the dipriva-social content gate.
//
// Usage: node dipriva/check-copy.mjs <file or directory> [...]
// Checks .txt, .md and .html files. In HTML only visible text and quoted script
// strings count. Text between <!-- brand-exempt:start --> and
// <!-- brand-exempt:end --> is skipped: use it only for a rejected example shown
// on purpose. Exits 1 when any error is found.
import {readdirSync, readFileSync, statSync} from 'node:fs';
import path from 'node:path';

const brand = JSON.parse(readFileSync(new URL('./brand.json', import.meta.url), 'utf8'));
const NOT_LETTER = '(?<![\\p{L}\\p{N}])';
const NOT_LETTER_AFTER = '(?![\\p{L}\\p{N}])';
const term = (rule) => new RegExp(`${NOT_LETTER}(?:${rule.pattern})${NOT_LETTER_AFTER}`, 'iu');
const EXTENSIONS = new Set(['.txt', '.md', '.html']);
const SKIP_DIRS = new Set(['node_modules', 'frames', 'work', 'fonts', '.git']);

function files(target) {
  if (!statSync(target).isDirectory()) return [target];
  return readdirSync(target).flatMap((name) => {
    const full = path.join(target, name);
    if (statSync(full).isDirectory()) return SKIP_DIRS.has(name) ? [] : files(full);
    return EXTENSIONS.has(path.extname(name)) ? [full] : [];
  });
}

function visibleText(file, raw) {
  let text = raw.replace(/<!-- brand-exempt:start[\s\S]*?brand-exempt:end -->/g, '');
  if (file.endsWith('.html')) {
    text = text
      .replace(/<style[\s\S]*?<\/style>/g, '')
      .replace(/<script[\s\S]*?<\/script>/g, (s) => (s.match(/'[^'\n]*'/g) ?? []).join('\n'))
      .replace(/<!--[\s\S]*?-->/g, '')
      .replace(/<[^>]+>/g, '\n');
  }
  if (file.endsWith('.md')) {
    // Markdown syntax is not copy: table rules, list bullets, code spans.
    text = text.replace(/^\|[-| :]+\|$/gm, '').replace(/^\s*[-*] /gm, '').replace(/`[^`\n]*`/g, '');
  }
  return text;
}

let errors = 0;
const targets = process.argv.slice(2);
if (targets.length === 0) {
  console.error('Usage: node dipriva/check-copy.mjs <file or directory> [...]');
  process.exit(2);
}
for (const file of targets.flatMap(files)) {
  const text = visibleText(file, readFileSync(file, 'utf8'));
  const issues = [];
  for (const rule of brand.bannedTerms) if (term(rule).test(text)) issues.push(['error', `banned word "${rule.label}"`]);
  for (const rule of brand.engagementBait) if (term(rule).test(text)) issues.push(['error', `engagement bait "${rule.label}"`]);
  if (/[—―]|--/.test(text) || /\s–\s/.test(text)) issues.push(['error', 'em dash or dash substitute']);
  if (/\p{Extended_Pictographic}/u.test(text)) issues.push(['error', 'emoji']);
  if (/\s-\s/.test(text)) issues.push(['warn', 'spaced hyphen reads as a dash']);
  for (const rule of brand.warnTerms) if (term(rule).test(text)) issues.push(['warn', `${rule.label}`]);
  // Captions and share copy: every figure must be a proof point or an approved
  // firm figure, as in the dipriva-social gate. On-screen UI is not checked.
  if (file.endsWith('.txt')) {
    const allowed = new Set([
      ...brand.claims.firmFigures.flatMap((f) => f.figures),
      ...brand.claims.proofPoints.flatMap((p) => p.statement.match(/\$?\d[\d,.]*%?\+?/g) ?? []),
    ].map((f) => f.replace(/[$,%+]/g, '')));
    const prose = text.replace(/https?:\/\/\S+/g, '');
    for (const figure of prose.match(/\d[\d,.]*/g) ?? []) {
      const bare = figure.replace(/[,.]+$/, '').replace(/,/g, '');
      if (!allowed.has(bare)) issues.push(['error', `figure "${bare}" is not a proof point or approved firm figure`]);
    }
  }
  const failed = issues.some(([severity]) => severity === 'error');
  if (failed) errors += 1;
  console.log(`${failed ? 'FAIL' : 'PASS'} ${file}`);
  for (const [severity, message] of issues) console.log(`  ${severity.padEnd(5)} ${message}`);
}
process.exit(errors ? 1 : 0);
