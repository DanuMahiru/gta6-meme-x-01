// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: a WANTED poster for GTA VI, drawn by
// make_meme.py from the real make.fun press-kit ghost (assets/mark-1024.png).
// The poster reads:
//
//   LEONIDA POLICE DEPARTMENT — WANTED — ★★★★★ (five stars, full wanted level)
//   mugshot: the make.fun ghost
//   GTA VI — LAST SEEN: 17 SEPT 2013 — CHARGE: 4,811 DAYS OF WAITING
//   REWARD: $250 — PAID BY MY AI AGENT ON MAKE.FUN
//
// 17 Sept 2013 is the day GTA V came out; 19 Nov 2026, launch week of
// GTA VI, is exactly 4,811 days later. The ghost is the suspect, the five
// stars are GTA's wanted level, and the reward line is the pitch: agents
// win real money in make.fun bounties.
//
// This program is all the grader needs from the repository: it reads
// POST.json (the post's address on X, filled in after the post goes out),
// checks it really names one X post, copies it to /output/POST.json where
// the gate reads it, and writes a deterministic manifest of the meme
// (meme.json) beside it. No network, no wall clock, no files outside the
// repository; two runs write the same bytes.
//
// Run it the way the grader does:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// One X post address, exactly as X shows it: https://x.com/<handle>/status/<id>
const POST_URL = /^https:\/\/(x\.com|twitter\.com)\/[A-Za-z0-9_]+\/status\/[0-9]+$/;

// The meme this entry hands in, as data: the poster make_meme.py draws.
const MEME = {
  format: 'WANTED poster, Leonida Police Department, Vice City District',
  image: 'meme.png',
  size: [1024, 1024],
  headline: 'WANTED',
  wanted_level_stars: 5,
  mugshot: 'the make.fun ghost (assets/mark-1024.png, the real press-kit mark)',
  suspect: 'GTA VI',
  last_seen: '17 SEPT 2013',
  charge: '4,811 DAYS OF WAITING',
  reward: '$250 — PAID BY MY AI AGENT ON MAKE.FUN',
  joke: 'GTA VI was last seen the day GTA V came out; 4,811 days later it is still wanted, and the reward was already paid by an AI agent on make.fun.',
};

function main(): void {
  const raw = readFileSync(join(BOT_DIR, 'POST.json'), 'utf8');
  const post: unknown = JSON.parse(raw);
  if (
    typeof post !== 'object' ||
    post === null ||
    typeof (post as { url?: unknown }).url !== 'string' ||
    !POST_URL.test((post as { url: string }).url)
  ) {
    console.error(
      'POST.json must name one X post: {"url": "https://x.com/<handle>/status/<id>"}',
    );
    process.exit(1);
  }
  mkdirSync(OUTPUT_DIR, { recursive: true });
  copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
  const manifest = { post, meme: MEME };
  writeFileSync(
    join(OUTPUT_DIR, 'meme.json'),
    JSON.stringify(manifest, null, 2) + '\n',
    'utf8',
  );
}

main();
