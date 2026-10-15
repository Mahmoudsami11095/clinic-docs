const fs = require('fs');

function mergeDisjointBlocks(filePath) {
  const text = fs.readFileSync(filePath, 'utf8');
  // First merge radiology
  const lines = text.split('\n');
  
  // Parse manually or regex to combine
  // Since both radiology and consent appear twice, let's read all keys
  const parsed = {};
  
  // We can use a regex to extract each top-level block
  const blockRegex = /"([^"]+)":\s*\{([^}]+)\}/g;
  let match;
  while ((match = blockRegex.exec(text)) !== null) {
    const blockName = match[1];
    const blockContent = match[2];
    if (!parsed[blockName]) {
      parsed[blockName] = {};
    }
    const innerRegex = /"([^"]+)":\s*"([^"]*)"/g;
    let innerMatch;
    while ((innerMatch = innerRegex.exec(blockContent)) !== null) {
      parsed[blockName][innerMatch[1]] = innerMatch[2];
    }
  }

  // Now format nicely as JSON
  fs.writeFileSync(filePath, JSON.stringify(parsed, null, 2));
  console.log(`Cleaned and merged ${filePath}`);
}

mergeDisjointBlocks('clinic-app/public/i18n/en.json');
mergeDisjointBlocks('clinic-app/public/i18n/ar.json');
