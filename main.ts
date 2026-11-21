// gta6-meme-x-01 v6 — "LEONIDA DMV: VEHICLE REGISTRATION RENEWAL".
//
// The entry is the X post itself: an AI agent made the meme (meme.png,
// rendered deterministically by render_meme.py), posted it on X from a
// public account with make.fun and the play code in its text, and this
// program hands the post's address to the house.
//
// What this program does (Node 22, standard library only):
//   1. Reads POST.json from the repository root and checks it is a JSON
//      object with a single `url` field shaped like an X post address:
//      https://x.com/<handle>/status/<digits> (twitter.com and
//      /i/web/status/<id> spellings are accepted too).
//   2. Checks meme.png is present next to it, so a broken repository
//      cannot be entered by accident.
//   3. Copies POST.json to /output/POST.json, where the gate reads it.
//
// The placeholder address this repository ships with (status/PLACEHOLDER)
// is not a real post: it passes with a warning but the house will refuse
// it, by design. Replace it with the real post address before submitting.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// An X post address: optional www./mobile. host, x.com or twitter.com,
// then /<handle>/status/<digits> or /i/web/status/<digits>. A query or
// fragment after the id is tolerated and ignored.
const POST_URL =
  /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/(i\/web\/status\/\d+|[A-Za-z0-9_]+\/status\/\d+)(\?[^#]*)?(#.*)?$/;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const postPath = join(BOT_DIR, "POST.json");
if (!existsSync(postPath)) {
  fail(`POST.json not found in ${BOT_DIR}`);
}

let raw: string;
try {
  raw = readFileSync(postPath, "utf8");
} catch (err) {
  fail(`POST.json could not be read: ${(err as Error).message}`);
}

let post: unknown;
try {
  post = JSON.parse(raw!);
} catch (err) {
  fail(`POST.json is not valid JSON: ${(err as Error).message}`);
}

if (typeof post !== "object" || post === null || Array.isArray(post)) {
  fail("POST.json must be a JSON object, {\"url\": \"...\"}");
}
const url = (post as Record<string, unknown>).url;
if (typeof url !== "string") {
  fail(`POST.json url is not a string: ${JSON.stringify(url)}`);
}
if (url.endsWith("/status/PLACEHOLDER")) {
  console.warn(
    "main.ts: warning: POST.json still holds the placeholder address " +
      "(status/PLACEHOLDER) — replace it with the real post before submitting.",
  );
} else if (!POST_URL.test(url)) {
  fail(
    `POST.json url is not an X post address: ${JSON.stringify(url)} ` +
      `(expected https://x.com/<handle>/status/<id>)`,
  );
}

const memePath = join(BOT_DIR, "meme.png");
if (!existsSync(memePath)) {
  fail(`meme.png not found in ${BOT_DIR} — the meme is part of the entry`);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
writeFileSync(join(OUTPUT_DIR, "POST.json"), raw!, "utf8");
console.log(`main.ts: handed in post ${url}`);
