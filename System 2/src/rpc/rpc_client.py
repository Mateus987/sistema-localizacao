import grpc
import src.rpc.rpc_pb2 as rpc_pb2
import src.rpc.rpc_pb2_grpc as rpc_pb2_grpc

class GrpcClient:
    def send_grpc_dispo(self, id_dispositivo, nome, marca, codigo):
        request = rpc_pb2.SendDispoRequest(
            id_dispositivo=id_dispositivo,
            marca=marca
        )

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = rpc_pb2_grpc.ApiServiceStub(channel)

            try:
                response = stub.SendDispo(request)
                return response
            except grpc.RpcError as e:
                return e

    def send_grpc_pos(self, id_dispositivo, lat, long):
        request = rpc_pb2.SendPosRequest(
            id_dispositivo=id_dispositivo,
            lat=lat,
            long=long
        )

        with grpc.insecure_channel('localhost:50051') as channel:
            stub = rpc_pb2_grpc.ApiServiceStub(channel)

            try:
                response = stub.SendPos(request)
                return response
            except grpc.RpcError as e:
                return e
