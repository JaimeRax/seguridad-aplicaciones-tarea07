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
    try {
      // DEMOSTRACIÓN: CWE-95, evaluación de entrada no confiable.
      const result = eval(expression);
      respond(res, 200, { result });
    } catch {
      respond(res, 400, { error: 'Expresión inválida' });
    }
    return;
  }
  respond(res, 404, { error: 'Ruta no encontrada' });
});

server.listen(3000, '127.0.0.1', () => {
  console.log('Laboratorio disponible solo en http://127.0.0.1:3000');
});
