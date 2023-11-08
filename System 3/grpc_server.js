var PROTO_PATH = '../System 2/src/rpc/rpc.proto';

const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('./database.sqlite3');

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

const insertDispo = db.prepare('INSERT INTO dispositivo (id_dispositivo, marca) VALUES (?, ?)');

function sendDispo(call, callback) {
    insertDispo.run(call.request.id_dispositivo, call.request.marca);
    callback(null, { message: "Dispo Recebido" });
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
    server.addService(trabalho_proto.ApiService.service, { SendDispo: sendDispo });

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