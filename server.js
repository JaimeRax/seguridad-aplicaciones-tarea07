// Laboratorio académico controlado: NO desplegar en producción.
// El servidor escucha exclusivamente en 127.0.0.1.
const http = require('node:http');
const { escape } = require('lodash');

function respond(res, code, data) {
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(data));
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, 'http://localhost');
  if (url.pathname === '/hello') {
    const name = url.searchParams.get('name') || 'estudiante';
    respond(res, 200, { message: `Hola, ${escape(name)}` });
    return;
  }
  if (url.pathname === '/calculate') {
    const expression = url.searchParams.get('expr') || '';
    // Remediación: permitir únicamente sumas de enteros (sin evaluación dinámica).
    const match = /^([0-9]{1,4})\+([0-9]{1,4})$/.exec(expression);
    if (!match) {
      respond(res, 400, { error: 'Solo se admiten sumas de enteros (ej. 2+3)' });
      return;
    }
    const result = Number(match[1]) + Number(match[2]);
    respond(res, 200, { result });
    return;
  }
  respond(res, 404, { error: 'Ruta no encontrada' });
});

server.listen(3000, '127.0.0.1', () => {
  console.log('Laboratorio disponible solo en http://127.0.0.1:3000');
});
