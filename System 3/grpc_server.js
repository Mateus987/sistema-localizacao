var PROTO_PATH = __dirname + '/grpc.proto';

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('../System 2/instance/database.sqlite3');

var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');

var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {
        keepCase: true,
        longs: String,
        enums: String,
        defaults: true,
        oneofs: true
    }
);

var trabalho_proto = grpc.loadPackageDefinition(packageDefinition).trabalho_sabatine;

function getDispoById(id_dispositivo, callback) {
    const query = 'SELECT * FROM dispositivo WHERE id = ?';
    db.get(query, [id_dispositivo], (err, row) => {
        callback(err, row);
    });
}

function getDispo(call, callback) {
    getDispoById(call.request.id_dispositivo, (err, dispo) => {
        if (err) {
            console.error(err.message);
        } else {
            if (dispo) {
                callback(null, { id_dispositivo: dispo.id, nome: dispo.nome, codigo: dispo.codigo, marca: dispo.marca });
            } else {
                callback(null, null);
            }
        }
    });
}

function onShutdown() {
    db.close((err) => {
        if (err) {
            console.error(err.message);
            process.exit(0);
        } else {
            console.log('Database connection closed.');
            process.exit(0);
        }
    });
}

function main() {
    var server = new grpc.Server();
    server.addService(trabalho_proto.ApiService.service, { GetDispo: getDispo });

    server.tryShutdown = onShutdown;

    process.on('SIGINT', () => {
        console.log('Received SIGINT signal. Initiating server shutdown.');
        server.tryShutdown(() => {
            console.log('Server shutdown complete.');
        });
    });

    process.on('SIGTERM', () => {
        console.log('Received SIGTERM signal. Initiating server shutdown.');
        server.tryShutdown(() => {
            console.log('Server shutdown complete.');
        });
    });

    server.bindAsync('0.0.0.0:50051', grpc.ServerCredentials.createInsecure(), () => {
        server.start();
    });
}

main();