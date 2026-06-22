#!/usr/bin/env node
/**
 * Test whether MathJax startup.promise resolves in our bundles.
 * Uses jsdom to simulate a browser environment.
 *
 * Usage: node tools/test-promise.js <path-to-bundle.js> [options-json]
 * Example: node tools/test-promise.js mathjax-concrete-euler/tex-mml-svg-mathjax-concrete-euler.js
 *          node tools/test-promise.js mathjax-concrete-euler/tex-mml-svg-mathjax-concrete-euler.js '{"enableEnrichment":false}'
 */
const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const bundlePath = process.argv[2];
if (!bundlePath) {
    console.error('Usage: node test-promise.js <bundle.js> [options-json]');
    process.exit(1);
}

const optionsArg = process.argv[3] ? JSON.parse(process.argv[3]) : {};
const bundleCode = fs.readFileSync(path.resolve(bundlePath), 'utf-8');

const html = `<!DOCTYPE html>
<html><head></head><body>
<p>Test: $x^2 + y^2 = z^2$</p>
<script>
MathJax = {
  tex: { inlineMath: [['$', '$']] },
  svg: { fontCache: 'global' },
  ${Object.keys(optionsArg).length ? `options: ${JSON.stringify(optionsArg)},` : ''}
  startup: {
    ready() {
      console.log('[TEST] ready() called');
      MathJax.startup.defaultReady();
      console.log('[TEST] defaultReady() returned');

      var p = MathJax.startup.promise;
      console.log('[TEST] promise exists:', !!p);

      p.then(function() {
        console.log('[TEST] RESOLVED');
      }).catch(function(e) {
        console.log('[TEST] REJECTED:', e);
      });
    }
  }
};
</script>
</body></html>`;

const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    resources: 'usable',
    url: 'http://localhost:8080/mathjax-fonts/mathjax-concrete-euler/',
    pretendToBeVisual: true,
});

const window = dom.window;

// Inject the bundle
const script = window.document.createElement('script');
script.textContent = bundleCode;

// Capture console
const origLog = window.console.log;
const origWarn = window.console.warn;
const origError = window.console.error;
window.console.log = (...args) => console.log(...args);
window.console.warn = (...args) => console.warn('WARN:', ...args);
window.console.error = (...args) => console.error('ERROR:', ...args);

console.log('[TEST] Loading bundle:', bundlePath);
console.log('[TEST] Options:', JSON.stringify(optionsArg));

try {
    window.document.head.appendChild(script);
} catch(e) {
    console.error('[TEST] Bundle load error:', e.message);
}

// Wait and check
setTimeout(() => {
    if (window.MathJax && window.MathJax.startup && window.MathJax.startup.promise) {
        // Check if promise resolved
        const p = window.MathJax.startup.promise;
        // Race with a short timeout
        Promise.race([
            p.then(() => 'RESOLVED').catch(e => 'REJECTED: ' + e),
            new Promise(r => setTimeout(() => r('STILL PENDING'), 2000))
        ]).then(result => {
            console.log('[TEST] After 5s total:', result);
            if (result === 'STILL PENDING') {
                // Check _actionPromises
                try {
                    const doc = window.MathJax.startup.document;
                    const ap = doc._actionPromises;
                    console.log('[TEST] _actionPromises count:', ap ? ap.length : 'none');
                    // Check renderActions
                    const ra = doc.renderActions;
                    if (ra && ra.items) {
                        console.log('[TEST] renderActions:');
                        ra.items.forEach((item, i) => {
                            console.log(`  [${i}] id=${item.id} priority=${item.priority}`);
                        });
                    }
                } catch(e) {
                    console.log('[TEST] inspect error:', e.message);
                }
            }
            process.exit(result === 'RESOLVED' ? 0 : 1);
        });
    } else {
        console.log('[TEST] No MathJax.startup.promise found');
        process.exit(1);
    }
}, 3000);
