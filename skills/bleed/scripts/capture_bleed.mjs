#!/usr/bin/env node
/**
 * Capture a page as chrome-free snippet images.
 * Usage: node capture_bleed.mjs <url> --out <dir>
 * Writes manifest.json and png files. Does not build the PDF.
 */
import { spawn } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import http from "node:http";
import net from "node:net";
import path from "node:path";

const MAX_CHUNK_CSS = 1680;
const VIEW_W = 1280;
const SCALE = 2;

function arg(name, fallback = "") {
  const i = process.argv.indexOf(name);
  if (i === -1) return fallback;
  return process.argv[i + 1] || fallback;
}

const url = process.argv[2];
const outDir = arg("--out", "/tmp/bleed-out");
if (!url || url.startsWith("--")) {
  console.error("usage: node capture_bleed.mjs <url> --out <dir>");
  process.exit(2);
}
fs.mkdirSync(outDir, { recursive: true });

function connectWs(wsUrl) {
  const u = new URL(wsUrl);
  return new Promise((resolve, reject) => {
    const sock = net.connect(Number(u.port || 80), u.hostname, () => {
      const key = crypto.randomBytes(16).toString("base64");
      sock.write(
        `GET ${u.pathname}${u.search} HTTP/1.1\r\n` +
          `Host: ${u.host}\r\n` +
          `Upgrade: websocket\r\n` +
          `Connection: Upgrade\r\n` +
          `Sec-WebSocket-Key: ${key}\r\n` +
          `Sec-WebSocket-Version: 13\r\n\r\n`
      );
    });
    let buf = Buffer.alloc(0);
    let ready = false;
    const waiters = new Map();
    let seq = 0;
    const queue = [];

    function sendFrame(text) {
      const payload = Buffer.from(text);
      const mask = crypto.randomBytes(4);
      let header;
      const len = payload.length;
      if (len < 126) header = Buffer.from([0x81, 0x80 | len]);
      else if (len < 65536) header = Buffer.from([0x81, 0x80 | 126, len >> 8, len & 255]);
      else {
        header = Buffer.alloc(10);
        header[0] = 0x81;
        header[1] = 0x80 | 127;
        header.writeBigUInt64BE(BigInt(len), 2);
      }
      const masked = Buffer.alloc(len);
      for (let i = 0; i < len; i++) masked[i] = payload[i] ^ mask[i % 4];
      sock.write(Buffer.concat([header, mask, masked]));
    }

    function emitText(text) {
      let msg;
      try {
        msg = JSON.parse(text);
      } catch {
        return;
      }
      if (msg.id && waiters.has(msg.id)) {
        const done = waiters.get(msg.id);
        waiters.delete(msg.id);
        if (msg.error) done.reject(new Error(JSON.stringify(msg.error)));
        else done.resolve(msg.result || {});
      }
    }

    function consume() {
      while (buf.length >= 2) {
        const b0 = buf[0];
        const b1 = buf[1];
        const opcode = b0 & 0x0f;
        let len = b1 & 0x7f;
        let off = 2;
        if (len === 126) {
          if (buf.length < 4) return;
          len = buf.readUInt16BE(2);
          off = 4;
        } else if (len === 127) {
          if (buf.length < 10) return;
          len = Number(buf.readBigUInt64BE(2));
          off = 10;
        }
        const masked = (b1 & 0x80) !== 0;
        const maskLen = masked ? 4 : 0;
        if (buf.length < off + maskLen + len) return;
        let payload = buf.slice(off + maskLen, off + maskLen + len);
        if (masked) {
          const mask = buf.slice(off, off + 4);
          payload = Buffer.from(payload);
          for (let i = 0; i < payload.length; i++) payload[i] ^= mask[i % 4];
        }
        buf = buf.slice(off + maskLen + len);
        if (opcode === 1) emitText(payload.toString("utf8"));
        else if (opcode === 8) sock.end();
        else if (opcode === 9) {
          const pong = Buffer.concat([Buffer.from([0x8a, payload.length]), payload]);
          sock.write(pong);
        }
      }
    }

    sock.on("data", (chunk) => {
      buf = Buffer.concat([buf, chunk]);
      if (!ready) {
        const end = buf.indexOf("\r\n\r\n");
        if (end < 0) return;
        const head = buf.slice(0, end).toString();
        if (!head.includes("101")) {
          reject(new Error(head.slice(0, 240)));
          return;
        }
        buf = buf.slice(end + 4);
        ready = true;
        resolve(api);
      }
      consume();
    });
    sock.on("error", reject);

    const api = {
      send(method, params = {}) {
        const id = ++seq;
        const packet = JSON.stringify({ id, method, params });
        return new Promise((resolve, reject) => {
          waiters.set(id, { resolve, reject });
          sendFrame(packet);
        });
      },
      close() {
        sock.end();
      },
    };
  });
}

function getJson(urlStr) {
  return new Promise((resolve, reject) => {
    http
      .get(urlStr, (res) => {
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => {
          try {
            resolve(JSON.parse(data));
          } catch (err) {
            reject(err);
          }
        });
      })
      .on("error", reject);
  });
}

const STRIP_AND_MEASURE = `(() => {
  const hideSel = [
    "header", "nav", "footer", "aside",
    "[role='banner']", "[role='navigation']", "[role='contentinfo']", "[role='complementary']",
    ".sidebar", "#sidebar", ".site-header", ".site-footer", ".navbar", ".nav-bar", ".menu",
    ".cookie", "#cookie", ".cookies", ".consent", "#consent", ".gdpr",
    ".skip-link", ".skip-to-content", ".share", ".social-share", ".related", ".newsletter"
  ];
  const style = document.createElement("style");
  style.textContent = hideSel.join(",") + "{display:none !important}"
    + "[data-bleed-hide]{display:none !important}"
    + "::-webkit-scrollbar{display:none}";
  document.documentElement.appendChild(style);
  const main = document.querySelector("main, article, [role='main']") || document.body;
  document.querySelectorAll("body *").forEach((el) => {
    const s = getComputedStyle(el);
    if (s.position !== "fixed" && s.position !== "sticky") return;
    if (main.contains(el) && el.querySelector("p, h1, h2, h3, img")) return;
    el.setAttribute("data-bleed-hide", "1");
  });
  document.querySelectorAll("iframe").forEach((el) => el.setAttribute("data-bleed-hide", "1"));
  const root = document.querySelector("main, article, [role='main']") || document.body;
  const heads = [...root.querySelectorAll("h1,h2,h3,h4")].filter((el) => {
    const r = el.getBoundingClientRect();
    return r.width > 8 && r.height > 8 && getComputedStyle(el).display !== "none";
  });
  function docBox(el) {
    const r = el.getBoundingClientRect();
    return {
      x: Math.max(0, r.left + window.scrollX),
      y: Math.max(0, r.top + window.scrollY),
      w: r.width,
      h: r.height
    };
  }
  function union(boxes) {
    const x = Math.min(...boxes.map((b) => b.x));
    const y = Math.min(...boxes.map((b) => b.y));
    const r = Math.max(...boxes.map((b) => b.x + b.w));
    const b = Math.max(...boxes.map((b) => b.y + b.h));
    return { x, y, w: r - x, h: b - y };
  }
  const blocks = [];
  if (!heads.length) {
    blocks.push({ kind: "snippet", text: "", box: docBox(root), atomic: false });
  } else {
    heads.forEach((h, i) => {
      const parent = h.parentElement;
      const kids = [...parent.children];
      const start = kids.indexOf(h);
      const els = [];
      for (let k = start; k < kids.length; k++) {
        if (k > start && heads.includes(kids[k])) break;
        const r = kids[k].getBoundingClientRect();
        if (r.width > 4 && r.height > 4) els.push(kids[k]);
      }
      if (!els.length) els.push(h);
      const boxes = els.map(docBox).filter((b) => b.w > 2 && b.h > 2);
      if (!boxes.length) return;
      const hasImg = els.some((el) => el.matches("img, picture, figure, svg") || el.querySelector("img, picture, figure, svg"));
      blocks.push({
        kind: /^H[1-4]$/.test(h.tagName) ? "section" : "snippet",
        level: Number(h.tagName.slice(1)),
        text: (h.textContent || "").trim().slice(0, 140),
        box: union(boxes),
        atomic: hasImg && boxes.length === 1
      });
    });
  }
  const images = [...root.querySelectorAll("img, picture img, figure img")].map((img) => {
    const box = docBox(img);
    if (box.w < 48 || box.h < 48) return null;
    const wide = box.w >= root.getBoundingClientRect().width * 0.72;
    return { kind: wide ? "banner" : "figure", text: img.getAttribute("alt") || "", box, atomic: true };
  }).filter(Boolean);
  return {
    title: document.title || "",
    bg: getComputedStyle(document.body).backgroundColor,
    blocks,
    images
  };
})()`;

function packBlocks(blocks) {
  const chunks = [];
  let i = 0;
  while (i < blocks.length) {
    const chunk = [];
    let h = 0;
    while (i < blocks.length) {
      const b = blocks[i];
      const heading = b.kind === "section";
      const follow = heading && blocks[i + 1] ? blocks[i + 1].box.h : 0;
      const need = b.box.h + (heading ? follow : 0);
      if (chunk.length && h + need > MAX_CHUNK_CSS && !b.atomic) break;
      chunk.push(b);
      h += b.box.h;
      i += 1;
      if (heading && i < blocks.length) {
        chunk.push(blocks[i]);
        h += blocks[i].box.h;
        i += 1;
      }
      if (h >= MAX_CHUNK_CSS) break;
    }
    if (!chunk.length) {
      chunk.push(blocks[i]);
      i += 1;
    }
    const x = Math.min(...chunk.map((b) => b.box.x));
    const y = Math.min(...chunk.map((b) => b.box.y));
    const r = Math.max(...chunk.map((b) => b.box.x + b.box.w));
    const bot = Math.max(...chunk.map((b) => b.box.y + b.box.h));
    const endsHeading = chunk[chunk.length - 1].kind === "section" && chunk.length === 1;
    chunks.push({
      role: chunk.some((b) => b.kind === "banner") ? "banner" : chunk.some((b) => b.kind === "figure") ? "figure" : "snippet",
      text: chunk.map((b) => b.text).filter(Boolean).join(" / "),
      box: { x, y, w: r - x, h: bot - y },
      keep: !endsHeading,
    });
  }
  return chunks;
}

// Direct session sender is implemented in run() so attach sessionId stays explicit.
async function run() {
  const port = 9300 + Math.floor(Math.random() * 400);
  const profile = fs.mkdtempSync("/tmp/bleed-chrome-");
  const chrome = spawn(
    "/usr/bin/chromium",
    [
      "--headless=new",
      "--no-sandbox",
      "--disable-gpu",
      "--disable-dev-shm-usage",
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${profile}`,
      "--hide-scrollbars",
      "about:blank",
    ],
    { stdio: "ignore" }
  );
  const kill = () => {
    try { chrome.kill("SIGKILL"); } catch {}
  };
  try {
    let version = null;
    for (let n = 0; n < 50; n++) {
      try {
        version = await getJson(`http://127.0.0.1:${port}/json/version`);
        break;
      } catch {
        await new Promise((r) => setTimeout(r, 150));
      }
    }
    if (!version) throw new Error("chromium debug port did not open");
    const browser = await connectWs(version.webSocketDebuggerUrl);
    const created = await browser.send("Target.createTarget", { url: "about:blank" });
    const attached = await browser.send("Target.attachToTarget", { targetId: created.targetId, flatten: true });
    const session = attached.sessionId;
    const pending = new Map();
    const orig = browser.send;
    // Listen by wrapping is hard; send via browser socket with sessionId using a side channel.
    // connectWs only resolves ids it sent. Re-open page websocket instead.
    browser.close();
    const list = await getJson(`http://127.0.0.1:${port}/json/list`);
    const page = list.find((t) => t.id === created.targetId) || list.find((t) => t.type === "page");
    if (!page) throw new Error("no page target");
    const cdp = await connectWs(page.webSocketDebuggerUrl);
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: VIEW_W,
      height: 1800,
      deviceScaleFactor: SCALE,
      mobile: false,
    });
    await cdp.send("Page.navigate", { url });
    await new Promise((r) => setTimeout(r, 1800));
    await cdp.send("Runtime.evaluate", { expression: "document.fonts && document.fonts.ready", awaitPromise: true });
    const measured = await cdp.send("Runtime.evaluate", {
      expression: STRIP_AND_MEASURE,
      returnByValue: true,
    });
    const data = measured.result && measured.result.value;
    if (!data) throw new Error("measure failed: " + JSON.stringify(measured));
    const sectionChunks = packBlocks(data.blocks || []);
    const imagePlates = (data.images || []).map((img) => ({
      role: img.kind,
      text: img.text,
      box: img.box,
      keep: true,
    }));
    const plates = [];
    for (const chunk of sectionChunks) plates.push(chunk);
    for (const img of imagePlates) {
      const dup = plates.some((p) => Math.abs(p.box.y - img.box.y) < 4 && Math.abs(p.box.h - img.box.h) < 8);
      if (!dup) plates.push(img);
    }
    plates.sort((a, b) => a.box.y - b.box.y);
    const manifest = { url, title: data.title || "", bg: data.bg || "", pages: [] };
    let n = 0;
    for (const plate of plates) {
      if (plate.box.w < 8 || plate.box.h < 8) continue;
      n += 1;
      const file = `snippet-${String(n).padStart(2, "0")}.png`;
      const shot = await cdp.send("Page.captureScreenshot", {
        format: "png",
        captureBeyondViewport: true,
        fromSurface: true,
        clip: {
          x: plate.box.x,
          y: plate.box.y,
          width: Math.ceil(plate.box.w),
          height: Math.ceil(plate.box.h),
          scale: 1,
        },
      });
      if (!shot.data) throw new Error("empty screenshot for " + file);
      fs.writeFileSync(path.join(outDir, file), Buffer.from(shot.data, "base64"));
      manifest.pages.push({
        file,
        role: plate.role,
        text: plate.text,
        keep: plate.keep !== false,
        css: plate.box,
      });
    }
    if (!manifest.pages.length) throw new Error("no snippets captured");
    const bad = manifest.pages.find((p) => p.keep === false);
    if (bad) throw new Error("heading would end a page: " + bad.text);
    fs.writeFileSync(path.join(outDir, "manifest.json"), JSON.stringify(manifest, null, 2));
    cdp.close();
    console.log(JSON.stringify({ out: outDir, pages: manifest.pages.length, title: manifest.title }));
  } finally {
    kill();
  }
}

run().catch((err) => {
  console.error(err.stack || err.message);
  process.exit(1);
});
