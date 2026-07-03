import fs from "fs";

export function accessLogger(req, res, next) {

    const logEntry = `
Access log info:
    Route: "${req.originalUrl}"
    method: ${req.method},
    User agent: ${req.headers["user-agent"]},
    IP address: ${req.ip},
    Timestamp: ${new Date().toISOString()}
`;

    console.log(logEntry);

// append file (persistent storage)
    fs.appendFileSync(
        "./logs/access.log",
        logEntry + "\n"
    );

    next();
}
