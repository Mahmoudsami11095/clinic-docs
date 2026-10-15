const { spawn } = require('child_process');
const path = require('path');

const pyScript = path.join(__dirname, '.agent-company', 'src', 'dashboard', 'server.py');
const port = process.env.PORT || '8088';

console.log(`Starting ClinicCorp AI Mission Control Dashboard on port ${port}...`);

const server = spawn('python', ['-u', pyScript, port], {
  stdio: 'inherit'
});

server.on('error', (err) => {
  console.error('Failed to start dashboard server:', err);
});

server.on('exit', (code, signal) => {
  console.log(`Dashboard server exited with code ${code} signal ${signal}`);
});

process.on('SIGINT', () => {
  server.kill('SIGINT');
  process.exit();
});

process.on('SIGTERM', () => {
  server.kill('SIGTERM');
  process.exit();
});
