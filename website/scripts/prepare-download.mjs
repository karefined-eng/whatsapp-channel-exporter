import { execFileSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const websiteRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repositoryRoot = resolve(websiteRoot, '..');
// On Windows, `npm` is `npm.cmd`; execFileSync without shell:true cannot resolve
// the .cmd shim (ENOENT), and Node >= 20 blocks spawning .cmd without shell
// (EINVAL). Vercel/Linux uses the plain name and needs no shell.
const isWindows = process.platform === 'win32';
const npmCommand = isWindows ? 'npm.cmd' : 'npm';
const spawnOptions = { cwd: repositoryRoot, stdio: 'inherit' };
if (isWindows) spawnOptions.shell = true;
const archive = resolve(repositoryRoot, 'wa-channel-exporter.zip');
const publicArchive = resolve(websiteRoot, 'public', 'wa-channel-exporter.zip');

// The website is deployed independently from the extension. Build the archive
// from the same checkout so the download cannot drift from the published code.
if (!existsSync(resolve(repositoryRoot, 'node_modules', 'jszip'))) {
  execFileSync(npmCommand, ['ci', '--omit=dev', '--ignore-scripts', '--no-audit', '--no-fund'], {
    cwd: repositoryRoot,
    stdio: 'inherit',
    ...(isWindows ? { shell: true } : {})
  });
}

execFileSync(npmCommand, ['run', 'build'], spawnOptions);

mkdirSync(dirname(publicArchive), { recursive: true });
copyFileSync(archive, publicArchive);
console.log(`Published ${publicArchive}`);
