from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import json
from bson import ObjectId

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client['django_mongo_db_aggregation']
sales_collection = db['sales']
suppliers_collection = db['suppliers']

@api_view(['POST'])
def insert_sales_data(request):
    try:
        # print("Received request body:", request.body)  # Log the raw request body
        data = json.loads(request.body)

        # Check if data is a list or a single dictionary
        if isinstance(data, dict):
            data = [data]  # Wrap a single dict in a list

        for entry in data:
            # Validate required fields for each entry
            required_fields = ['item', 'quantity', 'price', 'date', 'tags', 'supplier_id']
            for field in required_fields:
                if field not in entry:
                    print(f"Missing field: {field}")  # Log missing field
                    return Response(
                        {"error": f"Missing required field: {field}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Convert supplier_id to ObjectId
            entry['supplier_id'] = ObjectId(entry['supplier_id'])
            
            # Insert the document into the sales collection
            sales_collection.insert_one(entry)

        return Response({"message": "Data inserted successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        print("Error:", str(e))  # Log error
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def insert_supplier_data(request):
    try:
        print("Received request body:", request.body) 
        data = json.loads(request.body)

        # Check if data is a list or a single dictionary
        if isinstance(data, dict):
            data = [data]  # Wrap a single dict in a list

        for supplier in data:
            # Validate required fields for each supplier
            required_fields = ['name', 'contact']
            for field in required_fields:
                if field not in supplier:
                    return Response(
                        {"error": f"Missing required field: {field}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            # Insert each supplier into the suppliers collection
            suppliers_collection.insert_one(supplier)

        return Response({"message": "Supplier data inserted successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@require_http_methods(["GET"])
def get_sales_data(request):
    # Pipeline to match documents with quantity > 5, group, and calculate sum and average
    pipeline = [
        {"$match": {"quantity": {"$gt": 5}}},
        {"$group": {
            "_id": "$item",
            "totalQuantity": {"$sum": "$quantity"},
            "averagePrice": {"$avg": "$price"}
        }}
    ]
    results = list(sales_collection.aggregate(pipeline))
    return JsonResponse(results, safe=False)

@require_http_methods(["GET"])
def lookup_supplier_info(request):
    # Pipeline to perform a lookup with the suppliers collection
    pipeline = [
        {
            "$lookup": {
                "from": "suppliers",
                "localField": "supplier_id",
                "foreignField": "_id",
                "as": "supplier_info"
            }
        }
    ]
    results = list(sales_collection.aggregate(pipeline))

    # Function to recursively convert ObjectId to string
    def convert_objectid_to_str(obj):
        if isinstance(obj, list):
            return [convert_objectid_to_str(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_objectid_to_str(value) for key, value in obj.items()}
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    # Convert all ObjectIds in the results
    results = convert_objectid_to_str(results)

    return JsonResponse(results, safe=False)


@require_http_methods(["GET"])
def unwind_tags(request):
    # Assuming you have a similar aggregation or query logic here
    results = list(sales_collection.aggregate([
        {
            "$unwind": "$tags"
        },
        {
            "$group": {
                "_id": "$tags",
                "count": {"$sum": 1}
            }
        }
    ]))

    # Convert all ObjectIds in the results to strings
    def convert_objectid_to_str(obj):
        if isinstance(obj, list):
            return [convert_objectid_to_str(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_objectid_to_str(value) for key, value in obj.items()}
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    # Convert ObjectIds in results
    results = convert_objectid_to_str(results)

    return JsonResponse(results, safe=False)

@require_http_methods(["GET"])
def set_and_unset_example(request):
    # Assuming you have your MongoDB aggregation or query logic here
    results = list(sales_collection.aggregate([
        # Your aggregation pipeline goes here
    ]))

    # Convert all ObjectIds in the results to strings
    def convert_objectid_to_str(obj):
        if isinstance(obj, list):
            return [convert_objectid_to_str(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_objectid_to_str(value) for key, value in obj.items()}
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    # Convert ObjectIds in results
    results = convert_objectid_to_str(results)

    return JsonResponse(results, safe=False)


@require_http_methods(["GET"])
def check_tags_array(request):
    # Assuming you have your MongoDB query or aggregation here
    results = list(sales_collection.find({
        # Your query criteria here
    }))

    # Convert all ObjectIds in the results to strings
    def convert_objectid_to_str(obj):
        if isinstance(obj, list):
            return [convert_objectid_to_str(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: convert_objectid_to_str(value) for key, value in obj.items()}
        elif isinstance(obj, ObjectId):
            return str(obj)
        return obj

    # Convert ObjectIds in results
    results = convert_objectid_to_str(results)

    return JsonResponse(results, safe=False)
