# Recuperación de contraseña — versión anterior en Node.js (material de tesis)

> **Estado actual: NO forma parte del flujo de la aplicación.**
> Se conserva como material de referencia de la tesis. La lógica vive hoy
> en Flask, en `core/mailer.py` (`solicitar_pin`).

## Qué era

Un microservicio independiente escrito en Express (Node.js) de ~55 líneas.
Su única función era atender dos endpoints:

| Endpoint | Función |
|---|---|
| `GET /health` | Responder `{ok:true}` para que la app Flask supiera que estaba vivo |
| `POST /recuperar` | Generar un PIN de 6 dígitos, enviarlo por Resend y **devolverlo en la respuesta JSON** |

La app Flask le hablaba por HTTP a través del módulo `core/nodo_recuperacion.py`
(hoy eliminado), que además podía auto-levantarlo con `subprocess` en desarrollo.

## Por qué se migró a Flask

El prototipo no hacía nada que Flask no pudiera hacer por sí solo: el SDK
oficial de Resend para Python ya estaba integrado (`core/mailer.py`) para el
envío de mensajes de soporte. Mantener un segundo proceso/servicio solo para
un email sumaba complejidad sin ningún beneficio técnico:

- Un punto de falla extra: si el Node no estaba corriendo (local o dormido
  en producción), la recuperación fallaba con "No se pudo enviar el correo".
- Despliegue doble: dos servicios en Render, dos logs, más variables de entorno.

## Mejoras que trajo la migración

1. **PIN criptográficamente seguro:** se genera con `secrets.randbelow`
   (CSPRNG de Python) en lugar de `Math.random()` de Node, que no es
   apto para seguridad.
2. **El PIN ya no viaja por HTTP:** antes el Node devolvía el PIN en la
   respuesta JSON hacia Flask; ahora nace y muere dentro del proceso Flask,
   que guarda únicamente su hash (`generate_password_hash`) en MySQL.
3. **Un solo servicio** en producción (antes web + node): menos horas de
   instancia, deploy y logs únicos, una variable de entorno menos.
4. **Sin riesgo de timeout por servicio dormido:** los servicios gratuitos
   de Render se duermen por inactividad; con dos servicios, el primer intento
   de recuperación podía fallar mientras el Node despertaba (~1 minuto).
5. **Texto del correo corregido:** decía "vence en 5 minutos" pero la validez
   real es de 15 minutos. Hoy ambos salen de la constante `PIN_EXPIRA_MINUTOS`
   en `core/mailer.py`, compartida también por los `INSERT` de los blueprints.

## Cómo ejecutarlo (solo si se necesita demostrarlo)

```bash
cd docs/recuperacion
npm install
node server.js   # escucha en http://localhost:3000
```

Lee `RESEND_API_KEY` del `.env` de la raíz del repositorio y usa el remitente
`RESEND_FROM` (por defecto `onboarding@resend.dev`). En modo testing de Resend
solo entrega correos al dueño de la cuenta de Resend.
