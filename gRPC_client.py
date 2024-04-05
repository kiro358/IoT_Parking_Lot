import grpc
import dynamic_pricing_pb2
import dynamic_pricing_pb2_grpc

def fetch_dynamic_pricing(demand_factor):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = dynamic_pricing_pb2_grpc.DynamicPricingServiceStub(channel)
        response = stub.GetDynamicPricing(dynamic_pricing_pb2.PricingRequest(demand_factor=demand_factor))
        return response.price
