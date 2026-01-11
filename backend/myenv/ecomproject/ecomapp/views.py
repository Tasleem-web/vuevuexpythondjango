from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .products import products
from .models import Member
from django.db import connection

# Create your views here.


@api_view(["GET"])
def getRoutes(request):
    return Response("Hello World")


@api_view(["GET"])
def getProducts(request):
    return Response(products)


@api_view(["GET"])
def get_product_by_id(request, product_id):
    product = [product for product in products if product["id"] == str(product_id)]
    return Response(product[0])


@api_view(["POST"])
def postCart(request):
    data = request.data
    print("Data:", data)
    return Response("Item was added to cart")


@api_view(["GET"])
def getCartItems(request):
    sample_cart = [
        {
            "id": "1",
            "product": {
                "id": "14",
                "title": "Wireless Charger",
                "description": "Fast wireless charging pad",
                "image": "/product_images/Wireless_Charger.jpeg",
                "price": 29.99,
                "created_at": "2023-11-01T10:00:00Z",
                "updated_at": "2023-11-01T10:00:00Z",
            },
            "quantity": 2,
        },
        {
            "id": "2",
            "product": {
                "id": "15",
                "title": "Phone Tripod",
                "description": "Portable phone tripod for video",
                "image": "/product_images/Phone_Tripod.jpeg",
                "price": 22.99,
                "created_at": "2023-11-01T10:00:00Z",
                "updated_at": "2023-11-01T10:00:00Z",
            },
            "quantity": 1,
        },
    ]
    return Response(sample_cart)


@api_view(["DELETE"])
def removeCartItem(request, cart_item_id):
    print("Removing cart item with ID:", cart_item_id)
    return Response(f"Cart item with ID {cart_item_id} was removed")


@api_view(["POST"])
def postMembers(request):
    data = request.data
    print("Member Data:", data)
    
    try:
        # Create and save member to database
        member = Member.objects.create(
            name=data.get('name'),
            email=data.get('email'),
            status=data.get('status')
        )
        return Response({
            "message": "Member was added successfully",
            "member_id": member.id
        })
    except Exception as e:
        return Response({
            "error": str(e)
        }, status=400)


@api_view(["GET"])
def getMembers(request):
    all_items = Member.objects.all()
    members = []
    for item in all_items:
        members.append({
            "id": item.id,
            "name": item.name,
            "email": item.email,
            "status": item.status,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        })
    return Response(members)

@api_view(["GET"])
def getMember(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
        return Response({
            "status": "success",
            "member":{
                "id": member.id,
                "name": member.name,
                "email": member.email,
                "status": member.status,
                "created_at": member.created_at,
                "updated_at": member.updated_at,
            },
            "message": "Member retrieved successfully"
        })
    except Member.DoesNotExist:
        return Response({
            "status": "failed",
            "message": "Member not found"
        }, status=404)
        
@api_view(["DELETE"])
def deleteMember(request, member_id):
    try:
        member = Member.objects.get(id=member_id)
        member.delete()
        return Response({
            "status": "success",
            "message": "Member deleted successfully"
        })
    except Member.DoesNotExist:
        return Response({
            "status": "failed",
            "message": "Member not found"
        }, status=404)
        
@api_view(["PUT"])
def updateMember(request, member_id):
    data = request.data
    try:
        member = Member.objects.get(id=member_id)
        member.name = data.get('name', member.name)
        member.email = data.get('email', member.email)
        member.status = data.get('status', member.status)
        member.save()
        return Response({
            "status": "success",
            "message": "Member updated successfully"
        })
    except Member.DoesNotExist:
        return Response({
            "status": "failed",
            "message": "Member not found"
        }, status=404)
        
@api_view(["PATCH"])
def partialUpdateMember(request, member_id):
    data = request.data
    try:
        member = Member.objects.get(id=member_id)
        if 'name' in data:
            member.name = data['name']
        if 'email' in data:
            member.email = data['email']
        if 'status' in data:
            member.status = data['status']
        member.save()
        return Response({
            "status": "success",
            "message": "Member partially updated successfully"
        })
        
    except Member.DoesNotExist:
        return Response({
            "status": "failed",
            "message": "Member not found"
        }, status=404)


@api_view(["GET"])
def getMembersWithStatus(request):
    """Run raw SQL JOIN between ecomapp_member and ecomapp_status and return rows as JSON."""
    sql = """
        SELECT m.id, m.email, m.name, s.status AS current_status, m.status, m.created_at, m.updated_at
        FROM ecomapp_member m
        INNER JOIN ecomapp_status s ON m.status = s.status_id
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    results = [dict(zip(columns, row)) for row in rows]
    return Response(results)
        