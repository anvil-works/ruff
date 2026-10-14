// Expose the native executable directly so anvil-cli does not spawn a JS launcher.
const suffix = process.platform === "win32" ? ".exe" : "";
module.exports.executablePath = require.resolve(
  `@anvil-works/anvil-ty-${process.platform}-${process.arch}/bin/anvil-ty-native${suffix}`
);
