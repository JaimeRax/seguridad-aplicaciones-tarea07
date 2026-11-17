# Tarea S07 - Pipeline DevSecOps (laboratorio controlado)

**Curso:** Seguridad en Aplicaciones — Maestría en Seguridad Informática (UMG)  
**Modalidad:** práctica individual para GitHub Actions.  
**Aviso:** este repositorio inicia intencionalmente vulnerable. No exponer el servidor ni utilizar en producción.

## Lo que contiene

- `.github/workflows/devsecops-pipeline.yml`: SAST con Semgrep, SCA con OWASP Dependency-Check, SBOM CycloneDX y Quality Gate.
- `.semgrep/rules.yml`: regla propia `masi-s07-no-eval` (severidad ERROR).
- `server.js`: ejemplo deliberadamente inseguro (evaluación dinámica de una entrada).
- `package-lock.json`: `lodash@4.17.20` fijado con hash de integridad (versión afectada por CVE-2021-23337, CVSS 7.2 según NVD).
- `remediacion.patch`: parche que elimina `eval()` y actualiza lodash a 4.17.21.
- `scripts/gate_semgrep.py`: el análisis falla ante severidades ERROR/HIGH/CRITICAL.
- `evidencias/`: guardar exclusivamente capturas reales de GitHub Actions.

## Publicación y primera ejecución (FAILED)

1. Crear un repositorio **nuevo**, preferiblemente privado mientras se practica, en GitHub.
2. Subir **todos** los archivos preservando las rutas, incluidos `.github/` y `.semgrep/`.
3. Habilitar GitHub Actions si GitHub lo solicita y comprobar que la rama se llame `main` o `master`.
4. Abrir `Actions` > `Tarea S07 - DevSecOps SAST SCA SBOM` y revisar el primer run. También se puede iniciar con `Run workflow`.
5. Deben examinarse los jobs `sast`, `sca` y `quality-gate`; un fallo técnico de la herramienta o conexión **no** es evidencia válida de vulnerabilidad.
6. Descargar artefactos `informe-semgrep-json`, `sbom-cyclonedx` e `informe-dependency-check` cuando estén disponibles.
7. Capturar pantalla de los jobs y del reporte, con fecha y URL de la ejecución.

## Remediación y segunda ejecución (SUCCESS)

Desde una copia local del repositorio, en el estado vulnerable inicial:

```bash
git apply --check remediacion.patch
git apply remediacion.patch
npm ci --ignore-scripts --no-audit --no-fund
npm run check
git add server.js package.json package-lock.json
git commit -m "fix: remove eval and upgrade vulnerable lodash dependency"
git push
```

También se puede aplicar el parche con un editor y subir los tres archivos actualizados mediante GitHub.

Volver a GitHub Actions y comprobar que ambos jobs de análisis y el job `quality-gate` concluyen correctamente. Guardar capturas auténticas FAILED y SUCCESS.

## Política y limitaciones

- **SAST:** las reglas `p/security-audit`, `p/owasp-top-ten` y la regla local reportan resultados JSON; `gate_semgrep.py` bloquea el build si encuentra severidad `ERROR`, `HIGH` o `CRITICAL`.
- **SCA:** OWASP Dependency-Check se ejecuta con `--failOnCVSS 7`; reporta CVEs con criticidad HIGH/CRITICAL de acuerdo con CVSS. Puede haber falsos positivos y diferencias entre fuentes de datos; requieren triage.
- **SBOM:** Syft genera un documento CycloneDX con información sobre paquetes presentes durante el build. No inventar componentes si el documento real difiere.
- **Datos NVD:** la calidad del escaneo depende de la base de vulnerabilidades, su actualización y la disponibilidad de servicios externos; revisar logs ante problemas. La acción sugerida por el material del catedrático utiliza una imagen con base de datos precargada, pero su versión y estado actual deben validarse en la ejecución.
- **Suministro:** en un pipeline de producción conviene fijar los actions por SHA y mantener el gestor de dependencias, las firmas y las políticas de revisión de cambios. Aquí se usan versiones/tags para facilitar la práctica.

## Verificación documental

En el informe PDF incluir: enlace al repositorio; identificación del commit antes/después; extracto de **las primeras 30 líneas reales** de `sbom.cyclonedx.json`; la estructura completa de **un componente real**; un hallazgo SAST con línea/archivo; un hallazgo SCA con paquete/CVE/CVSS; e imágenes auténticas FAILED y SUCCESS.

## Referencias técnicas

- Documento de tarea y diapositivas de Semana 7 facilitadas por el catedrático.
- NVD, CVE-2021-23337: https://nvd.nist.gov/vuln/detail/CVE-2021-23337
- OWASP Dependency-Check: https://github.com/dependency-check/DependencyCheck
- GitHub Action Dependency-Check: https://github.com/dependency-check/Dependency-Check_Action
- Semgrep: https://semgrep.dev/docs/
- Anchore SBOM Action: https://github.com/anchore/sbom-action
