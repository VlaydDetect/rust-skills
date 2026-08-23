#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { delimiter, extname, join } from "node:path";
import { createInterface } from "node:readline/promises";

const CONFIG = JSON.parse(readFileSync(new URL("config.json", import.meta.url), "utf8"));
const required = ["marketplace", "plugin", "repository", "ref", "targets", "scopes"];
const scalars = ["marketplace", "plugin", "repository", "ref"];
const arrays = ["targets", "scopes"];
const safeName = /^[a-z0-9-]+$/;
if (
  Object.keys(CONFIG).sort().join() !== [...required].sort().join()
  || scalars.some((key) => typeof CONFIG[key] !== "string" || !CONFIG[key])
  || arrays.some((key) =>
    !Array.isArray(CONFIG[key])
    || !CONFIG[key].length
    || new Set(CONFIG[key]).size !== CONFIG[key].length
    || CONFIG[key].some((item) => typeof item !== "string" || !item)
  )
  || !safeName.test(CONFIG.marketplace)
  || !safeName.test(CONFIG.plugin)
  || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(CONFIG.repository)
  || !/^v[0-9A-Za-z][0-9A-Za-z._-]*$/.test(CONFIG.ref)
  || arrays.some((key) => CONFIG[key].some((item) => !safeName.test(item)))
) {
  throw new Error("invalid installer config");
}
const {
  marketplace: MARKETPLACE,
  plugin: PLUGIN,
  repository: REPOSITORY,
  ref: REF,
  targets: TARGETS,
  scopes: SCOPES,
} = CONFIG;

function parseArgs(argv) {
  const args = { target: "all", scope: "user", dryRun: false, yes: false };
  for (let index = 0; index < argv.length; index += 1) {
    const option = argv[index];
    if (option === "--dry-run") args.dryRun = true;
    else if (option === "--yes") args.yes = true;
    else if (option === "--target" || option === "--scope") {
      const value = argv[++index];
      if (!value) throw new Error(`${option} requires a value`);
      args[option === "--target" ? "target" : "scope"] = value;
    } else if (option === "--help" || option === "-h") {
      console.log("Usage: rust-engineering-install [--target codex-cli|chatgpt-desktop|claude-code|claude-desktop|all] [--scope user|project|local] [--dry-run] [--yes]");
      process.exit(0);
    } else throw new Error(`unknown option: ${option}`);
  }
  if (![...TARGETS, "all"].includes(args.target)) throw new Error(`invalid target: ${args.target}`);
  if (!SCOPES.includes(args.scope)) throw new Error(`invalid scope: ${args.scope}`);
  return args;
}

function plannedLines(target, scope) {
  const selected = target === "all" ? TARGETS : [target];
  const lines = [
    `Rust Engineering ${REF.replace(/^v/, "")}`,
    `Marketplace: ${REPOSITORY}@${REF}`,
  ];
  if (selected.includes("codex-cli")) lines.push(
    `Codex add: codex plugin marketplace add ${REPOSITORY} --ref ${REF}`,
    `Codex refresh: codex plugin marketplace upgrade ${MARKETPLACE}`,
    `Codex install: codex plugin add ${PLUGIN}@${MARKETPLACE}`,
  );
  if (selected.includes("claude-code")) lines.push(
    `Claude add: claude plugin marketplace add ${REPOSITORY}@${REF} --scope ${scope}`,
    `Claude refresh: claude plugin marketplace update ${MARKETPLACE}`,
    `Claude install: claude plugin install ${PLUGIN}@${MARKETPLACE} --scope ${scope}`,
    `Claude update: claude plugin update ${PLUGIN}@${MARKETPLACE} --scope ${scope}`,
  );
  if (selected.includes("chatgpt-desktop")) lines.push(
    "ChatGPT Desktop: open the plugin directory, select rust-engineering from rust-skills, confirm installation, then start a new task.",
  );
  if (selected.includes("claude-desktop")) lines.push(
    `Claude Desktop: in a local session open /plugin, add ${REPOSITORY}@${REF}, install ${PLUGIN}@${MARKETPLACE}, then run /reload-plugins or restart.`,
  );
  return lines;
}

function resolveExecutable(command) {
  if (process.platform !== "win32") return command;
  const extensions = (process.env.PATHEXT || ".COM;.EXE;.BAT;.CMD").split(";");
  for (const directory of (process.env.PATH || "").split(delimiter)) {
    for (const extension of extensions) {
      const candidate = join(directory.replace(/^"|"$/g, ""), `${command}${extension.toLowerCase()}`);
      if (existsSync(candidate)) return candidate;
    }
  }
  return command;
}

function invoke(command, args, json = false) {
  const executable = resolveExecutable(command);
  const isCommandShim = [".bat", ".cmd"].includes(extname(executable).toLowerCase());
  const program = isCommandShim ? (process.env.ComSpec || "cmd.exe") : executable;
  const programArgs = isCommandShim ? ["/d", "/s", "/c", `""${executable}" ${args.join(" ")}"`] : args;
  const result = spawnSync(program, programArgs, {
    encoding: "utf8",
    stdio: json ? "pipe" : "inherit",
    windowsVerbatimArguments: isCommandShim,
  });
  if (result.error?.code === "ENOENT") throw new Error(`${command === "codex" ? "Codex" : "Claude Code"} CLI not found; install it separately or use the Desktop instructions`);
  if (result.error) throw result.error;
  if (result.status !== 0) {
    const detail = json ? `\n${(result.stderr || "").trim()}` : "";
    throw new Error(`command failed (${result.status}): ${[command, ...args].join(" ")}${detail}`);
  }
  if (!json) return null;
  try {
    return JSON.parse(result.stdout);
  } catch (error) {
    throw new Error(`invalid JSON from: ${[command, ...args].join(" ")}`, { cause: error });
  }
}

function *records(value) {
  if (Array.isArray(value)) {
    for (const item of value) yield *records(item);
  } else if (value && typeof value === "object") {
    yield value;
    for (const item of Object.values(value)) yield *records(item);
  }
}

function marketplaceRecord(data) {
  return [...records(data)].find((item) => item.name === MARKETPLACE);
}

function pluginInstalled(data) {
  return [...records(data)].some((item) =>
    item.name === PLUGIN
    && item.marketplaceName === MARKETPLACE
    && item.installed !== false
  );
}

function assertExpectedSource(record) {
  const normalized = JSON.stringify(record).toLowerCase().replaceAll("\\", "/");
  if (!normalized.includes(REPOSITORY.toLowerCase())) throw new Error(`marketplace name collision: ${MARKETPLACE} uses another source`);
}

function installCodex() {
  const existing = marketplaceRecord(invoke("codex", ["plugin", "marketplace", "list", "--json"], true));
  if (existing) {
    assertExpectedSource(existing);
    invoke("codex", ["plugin", "marketplace", "upgrade", MARKETPLACE]);
  } else invoke("codex", ["plugin", "marketplace", "add", REPOSITORY, "--ref", REF]);
  if (!pluginInstalled(invoke("codex", ["plugin", "list", "--json"], true))) {
    invoke("codex", ["plugin", "add", `${PLUGIN}@${MARKETPLACE}`]);
  }
}

function installClaude(scope) {
  const existing = marketplaceRecord(invoke("claude", ["plugin", "marketplace", "list", "--json"], true));
  if (existing) {
    assertExpectedSource(existing);
    invoke("claude", ["plugin", "marketplace", "update", MARKETPLACE]);
  } else invoke("claude", ["plugin", "marketplace", "add", `${REPOSITORY}@${REF}`, "--scope", scope]);
  const installed = pluginInstalled(invoke("claude", ["plugin", "list", "--json"], true));
  invoke("claude", ["plugin", installed ? "update" : "install", `${PLUGIN}@${MARKETPLACE}`, "--scope", scope]);
}

async function confirm() {
  const input = createInterface({ input: process.stdin, output: process.stdout });
  const answer = await input.question("Run the host-native installation commands? [y/N] ");
  input.close();
  return ["y", "yes"].includes(answer.trim().toLowerCase());
}

async function main() {
  let args;
  try {
    args = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(`ERROR: ${error.message}`);
    return 2;
  }
  console.log(plannedLines(args.target, args.scope).join("\n"));
  if (args.dryRun) return 0;
  const selected = args.target === "all" ? TARGETS : [args.target];
  const cliTargets = selected.filter((item) => item === "codex-cli" || item === "claude-code");
  if (cliTargets.length && !args.yes && !(await confirm())) {
    console.log("Cancelled; no changes made.");
    return 0;
  }
  const failures = [];
  for (const target of cliTargets) {
    try {
      if (target === "codex-cli") installCodex();
      else installClaude(args.scope);
    } catch (error) {
      if (args.target !== "all") {
        console.error(`ERROR: ${error.message}`);
        return 2;
      }
      failures.push(error.message);
    }
  }
  for (const failure of failures) console.error(`SKIP: ${failure}`);
  return failures.length < cliTargets.length || !cliTargets.length ? 0 : 2;
}

process.exitCode = await main();
