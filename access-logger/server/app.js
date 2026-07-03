import express from "express";
import { accessLogger } from "./logger.js";

const app = express();

// middleware aktivoidaan KAIKILLE routeille
app.use(accessLogger);

app.get("/", (req, res) => {
    res.json({ message: "Home page" });
});

app.get("/home", (req, res) => {
    res.json({ message: "Home route" });
});

app.post("/home", (req, res) => {
    res.json({ message: "POST home" });
});

app.get("/header-demo", (req, res) => {
    res.json({ message: "Headers logged" });
});

app.listen(3000, () => {
    console.log("Server running on port 3000");
});
