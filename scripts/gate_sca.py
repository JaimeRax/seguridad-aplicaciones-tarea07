#!/usr/bin/env python3
"""Quality Gate SCA para reportes JSON de OWASP Dependency-Check."""
import json
import sys
from pathlib import Path

UMBRAL = 7.0


def puntuacion(vuln):
    """Mayor puntuación CVSS disponible (v4, v3 o v2)."""
    valores = []
    for campo in ("cvssv4", "cvssv3", "cvssv2"):
        cvss = vuln.get(campo)
        if isinstance(cvss, dict) and cvss.get("baseScore") is not None:
            valores.append(float(cvss["baseScore"]))
    return max(valores) if valores else None


def main():
    if len(sys.argv) != 2:
        print("Uso: python scripts/gate_sca.py reports/dependency-check-report.json", file=sys.stderr)
        return 2

    archivo = Path(sys.argv[1])
    try:
        datos = json.loads(archivo.read_text(encoding="utf-8"))
        dependencias = datos["dependencies"]
        if not isinstance(dependencias, list) or not dependencias:
            raise ValueError("El reporte no tiene dependencias analizadas")
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"ERROR SCA: falta un reporte valido: {error}", file=sys.stderr)
        return 2

    hallazgos = {}
    for dependencia in dependencias:
        for vuln in dependencia.get("vulnerabilities", []):
            identificador = str(vuln.get("name", "SIN-ID"))
            origen = str(vuln.get("source", "desconocido"))
            key = (origen, identificador)
            valor = puntuacion(vuln)
            severidad = str(vuln.get("severity", "")).upper()
            bloquea = (valor is not None and valor >= UMBRAL) or (
                valor is None and severidad in {"HIGH", "CRITICAL"}
            )
            anterior = hallazgos.get(key)
            if anterior is None or (bloquea and not anterior["bloquea"]):
                hallazgos[key] = {
                    "cvss": valor,
                    "severidad": severidad,
                    "archivo": dependencia.get("fileName", "sin nombre"),
                    "bloquea": bloquea,
                }

    bloqueantes = [(clave, dato) for clave, dato in hallazgos.items() if dato["bloquea"]]
    print(f"Dependencias/archivos revisados: {len(dependencias)}")
    print(f"Identificadores SCA encontrados: {len(hallazgos)}; bloqueantes: {len(bloqueantes)}")
    for (origen, identificador), dato in bloqueantes:
        puntaje = f"CVSS {dato['cvss']:.1f}" if dato["cvss"] is not None else dato["severidad"]
        print(f"BLOQUEANTE: {identificador} ({origen}; {puntaje}) en {dato['archivo']}")

    if bloqueantes:
        print("QUALITY GATE SCA: FAILED")
        return 1
    print("QUALITY GATE SCA: SUCCESS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
