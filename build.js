const fs = require('fs');
const path = require('path');

// 1. Resolve Backend URL from environment variables
let backendUrl =
    process.env.BACKEND_URL ||
    process.env.VITE_API_URL ||
    process.env.API_URL ||
    process.env.PUBLIC_API_URL ||
    '';

// If not in process.env, check .env file if it exists
const envPath = path.join(__dirname, '.env');
if (!backendUrl && fs.existsSync(envPath)) {
    const envContent = fs.readFileSync(envPath, 'utf-8');
    const match = envContent.match(/^(?:BACKEND_URL|VITE_API_URL|API_URL|PUBLIC_API_URL)\s*=\s*['"]?(.*?)['"]?$/m);
    if (match && match[1]) {
        backendUrl = match[1].trim();
    }
}

// Clean up trailing slash
if (backendUrl) {
    backendUrl = backendUrl.replace(/\/+$/, '');
}

console.log('[build] Configured Backend URL:', backendUrl || '(default: localhost for dev, empty for origin)');

// 2. Ensure frontend and public directories exist
const frontendDir = path.join(__dirname, 'frontend');
const publicDir = path.join(__dirname, 'public');

if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
}

// 3. Generate config.js content
const configContent = `// Runtime configuration for Cardio Disease Prediction API
// Auto-generated during build. In local dev, falls back to localhost if empty.
window.__APP_CONFIG__ = {
    BACKEND_URL: "${backendUrl}"
};
`;

fs.writeFileSync(path.join(frontendDir, 'config.js'), configContent, 'utf-8');
fs.writeFileSync(path.join(publicDir, 'config.js'), configContent, 'utf-8');

// 4. Sync files from frontend to public
if (fs.existsSync(frontendDir)) {
    const files = fs.readdirSync(frontendDir);
    for (const file of files) {
        if (file === 'package-lock.json' || file === 'node_modules') continue;
        const srcFile = path.join(frontendDir, file);
        const destFile = path.join(publicDir, file);
        if (fs.statSync(srcFile).isFile()) {
            fs.copyFileSync(srcFile, destFile);
        }
    }
}

console.log('[build] Build completed successfully. Static files and config.js synced.');
