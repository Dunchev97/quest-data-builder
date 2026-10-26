// Invoke the unmodified game converter. All writes stay in the disposable tree.
const fs = require('fs');
const path = require('path');
const [manifestPath] = process.argv.slice(2);
const config = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const root = path.resolve(config.root);
const write = fs.writeFileSync;
let writes = [];
fs.writeFileSync = function (file, ...args) {
  const relative = path.relative(root, path.resolve(file));
  if (relative.startsWith('..') || path.isAbsolute(relative)) throw Error('Write outside sandbox: ' + file);
  writes.push(relative);
  return write.call(fs, file, ...args);
};
const converter = require(config.converter);
for (const file of config.files) {
  const start = writes.length;
  try { converter.run(root, file); }
  catch (error) { throw Error(file + ': ' + error.stack); }
  process.stdout.write(JSON.stringify({file, writes: writes.slice(start)}) + '\n');
}
