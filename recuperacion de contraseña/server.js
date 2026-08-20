const express = require("express");
const { Resend } = require("resend");
const path = require("path");
// Cargar el .env desde la raíz del proyecto (donde vive RESEND_API_KEY).
require("dotenv").config({ path: path.resolve(__dirname, "..", ".env") });

const app = express();

app.use(express.json());

const resend = new Resend(process.env.RESEND_API_KEY);

// Health check: la app Python pregunta si el server está activo. No dispara
// ningún email (GET, responde 200 con JSON).
app.get("/health", (req, res) => {
    res.status(200).json({ ok: true });
});

app.post("/recuperar", async (req, res) => {

    try {

        const email = req.body.email;

        // generar PIN
        const pin = Math.floor(100000 + Math.random() * 900000);

        // enviar correo
        await resend.emails.send({
            from: process.env.RESEND_FROM || "onboarding@resend.dev",
            to: email,
            subject: "Recuperación de contraseña",
            html: `
                <h1>Tu PIN es:</h1>
                <h2>${pin}</h2>
                <p>El código vence en 5 minutos.</p>
            `
        });

        res.send({
            mensaje: "Correo enviado",
            pin: pin
        });

    } catch (error) {

        console.log(error);

        res.status(500).send("Error");
    }
});

app.listen(process.env.PORT || 3000, () => {
    console.log("Servidor funcionando");
});