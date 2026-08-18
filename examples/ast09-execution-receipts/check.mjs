#!/usr/bin/env node
// Vendor-neutral offline checker for the AST09 signed-admission vector.
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PINNED_ISSUER_SPKI = 'MCowBQYDK2VwAyEAtI_hu4q5yjIsTuWwCFyqPqFP8UFgHU36i5qZY2qiLbs';
const REQUIRED = [
  'receipt_type', 'attempt_id', 'agent_id', 'executor_id', 'audience',
  'action', 'action_digest', 'policy_version', 'decision', 'timestamp_ms',
  'issuer', 'key_id', 'signature',
];

function canonicalize(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalize).join(',')}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalize(value[key])}`).join(',')}}`;
}

function digest(value) {
  return `sha256:${crypto.createHash('sha256').update(canonicalize(value)).digest('hex')}`;
}

export function checkReceipt(file) {
  let receipt;
  try {
    receipt = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (error) {
    return { ok: false, failures: [`read_or_parse_failed:${error.message}`] };
  }
  const failures = [];
  const missing = REQUIRED.filter((field) => !(field in receipt));
  if (missing.length) failures.push(`missing_fields:${missing.join(',')}`);
  if (receipt.receipt_type !== 'admission') failures.push('wrong_receipt_type');
  if (receipt.decision !== 'DENY') failures.push('decision_not_deny');
  if (!Number.isSafeInteger(receipt.timestamp_ms)) failures.push('timestamp_not_safe_integer');
  if (digest(receipt.action) !== receipt.action_digest) failures.push('action_digest_mismatch');
  if (receipt.signature?.algorithm !== 'Ed25519') failures.push('unsupported_signature_algorithm');

  try {
    const unsigned = { ...receipt };
    delete unsigned.signature;
    const key = crypto.createPublicKey({
      key: Buffer.from(PINNED_ISSUER_SPKI, 'base64url'),
      format: 'der',
      type: 'spki',
    });
    const valid = crypto.verify(
      null,
      Buffer.from(canonicalize(unsigned), 'utf8'),
      key,
      Buffer.from(receipt.signature?.value || '', 'base64url'),
    );
    if (!valid) failures.push('signature_invalid_under_pinned_issuer_key');
  } catch {
    failures.push('signature_invalid_under_pinned_issuer_key');
  }
  return { ok: failures.length === 0, failures };
}

function runOne(file) {
  const result = checkReceipt(file);
  console.log(`${result.ok ? 'PASS' : 'FAIL'} ${path.basename(file)}`);
  for (const failure of result.failures) console.log(`  - ${failure}`);
  if (result.ok) {
    console.log('  Claim boundary: pinned issuer signed DENY for the exact action.');
    console.log('  Missing outcome: INDETERMINATE without authenticated completeness.');
  }
  return result.ok ? 0 : 1;
}

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
if (args.length === 1 && args[0] === '--selftest') {
  const cases = [
    ['deny-admission-receipt.json', 0],
    ['deny-admission-receipt.tampered.json', 1],
    ['deny-admission-receipt.rehashed-forgery.json', 1],
  ];
  let failed = false;
  for (const [name, expected] of cases) {
    const actual = runOne(path.join(here, name));
    if (actual !== expected) failed = true;
  }
  process.exit(failed ? 1 : 0);
}
if (args.length !== 1 || args[0].startsWith('-')) {
  console.error('usage: node check.mjs <receipt.json> | --selftest');
  process.exit(2);
}
process.exit(runOne(path.resolve(args[0])));
