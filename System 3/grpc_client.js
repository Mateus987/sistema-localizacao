var PROTO_PATH = __dirname + '/grpc.proto';

var parseArgs = require('minimist');
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

function main() {
    var argv = parseArgs(process.argv.slice(2), {
        string: 'target'
    });

    var target;
    if (argv.target)
        target = argv.target;
    else
        target = 'localhost:50051';

    var client = new trabalho_proto.ApiService(target, grpc.credentials.createInsecure());
    var user;

    if (argv._.length > 0)
        user = argv._[0];
    else
        user = 'world';

    client.GetDispo({ id_dispositivo: "1cd68ad2-723f-4928-8213-a07dc517b84a" }, function (err, response) {
        console.log(response)
    });
}

main();