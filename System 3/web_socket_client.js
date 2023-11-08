const WebSocket = require('ws');

const http = require('http');

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./database.sqlite3');

const insertPos = db.prepare('INSERT INTO dispo_info (id_dispositivo, quantidade_pos, total_km, data) VALUES (?, ?, ?, ?)');

const updatePos = 'UPDATE dispo_info SET quantidade_pos = ?, total_km = ?, data = ? WHERE id_dispositivo = ?';

function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in kilometers
    const dLat = deg2rad(lat2 - lat1);
    const dLon = deg2rad(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    const distance = R * c; // Distance in kilometers

    return distance;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180);
}

function receive_messages() {
    const websocket = new WebSocket('ws://localhost:8765');

    websocket.on('open', () => {
        // You can send a message here if needed
        // websocket.send('Hello world!');
    });

    websocket.on('message', (message) => {
        console.log(`Received: ${message}`);
        message = JSON.parse(message);

        let options = {
            hostname: 'localhost',
            port: 3333,
            path: '/historico/' + message.id_dispositivo,
            method: 'GET',
        };

        const req = http.request(options, (res) => {
            let data = '';

            // A chunk of data has been received.
            res.on('data', (chunk) => {
                data += chunk;
            });

            // The whole response has been received.
            res.on('end', () => {
                if (data) {
                    data = JSON.parse(data);
                    data.sort((a, b) => new Date(b.data) - new Date(a.data));
                    let total_km = 0
                    if (data.length > 1) {
                        total_km = calculateDistance(data[1].latitude, data[1].longitude, message.latitude, message.longitude);
                    }
                    db.get(
                        'SELECT * FROM dispo_info WHERE id_dispositivo = ? ORDER BY data DESC LIMIT 1',
                        [message.id_dispositivo],
                        (err, row) => {
                            if (err) {
                                console.error(err.message);
                            } else {
                                if (row) {
                                    db.run(updatePos, [row.quantidade_pos+1, row.total_km+total_km, new Date(), message.id_dispositivo], function (err) {
                                        if (err) {
                                            console.error('Error updating data:', err.message);
                                        } else {
                                            console.log(`Rows affected: ${this.changes}`);
                                        }
                                    });
                                } else {
                                    insertPos.run(message.id_dispositivo, 1, total_km, new Date())
                                }
                            }
                        });
                }
            });
        });

        req.on('error', (error) => {
            console.error('Error making GET request:', error.message);
        });

        // End the request
        req.end();
    });

    websocket.on('close', () => {
        console.log('WebSocket connection closed.');
    });

    websocket.on('error', (error) => {
        console.error(`WebSocket error: ${error.message}`);
    });
}

receive_messages();