# Nosy — the interview worker for runp8.com

Nosy is the AI assistant in the `#interview` section of runp8.com. She answers
recruiters' questions about Eli's verified work history, products, and
technical experience. The chat on the page POSTs `{question, history}` to the
Cloudflare Worker `interview-workerjs`.

## Source of truth

`workers/interview-worker.js` is the exact file deployed to Cloudflare.
The worker's source used to live only in the Cloudflare dashboard, which is
how its profile went stale (it still listed 9 products and claimed TheJudgy
was live). Keep this file and the deployed worker in sync: edit here, deploy,
verify live.

## Deploy

From the Muse VM:

```bash
python3 workers/deploy_nosy.py workers/interview-worker.js
```

That PUTs the script to the `interview-workerjs` worker via the connected
Cloudflare credential. Then verify live:

```bash
curl https://interview-workerjs.infomomtelo.workers.dev/
curl -X POST https://interview-workerjs.infomomtelo.workers.dev/ \
  -H 'Content-Type: application/json' \
  -d '{"question":"How many products has Eli shipped, and which ones?","history":[]}'
```

## Secret

The worker reads `env.ANTHROPIC_API_KEY` — the SecondRail customer key
(`cust_bkj0zxhx`). It is set as a secret in the Cloudflare dashboard and is
never in this repo. A script upload does not touch it. The worker calls the
model through `https://secondrail.tello.live/v1/messages`, so a dead provider
fails over instead of taking Nosy down.
