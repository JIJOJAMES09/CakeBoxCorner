from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from myapp.models import Cakebox
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.decorators import action

from rest_framework import permissions,authentication

from cakeboxapi.serializers import UserSerializer


class Cakeboxserializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Cakebox
        fields="__all__"



class CakeboxView(ViewSet):

    def list(self,request,*args,**kwargs):
        qs=Cakebox.objects.all()

        if "flavour" in request.query_params:
            fl=request.query_params.get("flavour")
            qs=qs.filter(flavour__iexact=fl)

        if "shape" in request.query_params:
            sh=request.query_params.get("shape")
            qs=qs.filter(shape__iexact=sh)

        if "layer" in request.query_params:
            la=request.query_params.get("layer")
            qs=qs.filter(layer=la)

        if "weight" in request.query_params:
            we=request.query_params.get("weight")
            qs=qs.filter(weight__iexact=we)


        if "price" in request.query_params:
            pr=request.query_params.get("price")
            qs=qs.filter(price=pr)



        serializer=Cakeboxserializer(qs,many=True)

        return Response(data=serializer.data)
    

    def create(self,request,*args,**kwargs):
        serializer=Cakeboxserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Cakebox.objects.get(id=id)
        serializer=Cakeboxserializer(qs)
        return Response(data=serializer.data)
    

    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        cake_obj=Cakebox.objects.get(id=id)
        serializer=Cakeboxserializer(instance=cake_obj,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        


    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        try:
            Cakebox.objects.get(id=id).delete()
            return Response(data="deleted")
        except Exception:
            return Response(data="no matching record found")



    @action(methods=["get"],detail=False)
    def all_flavour(self,request,*args,**kwargs):
        qs=Cakebox.objects.all().values_list("flavour",flat=True).distinct()
        return Response(data=qs)
    

class CakeboxesViewsetView(ModelViewSet):
    serializer_class=Cakeboxserializer
    model=Cakebox
    queryset=Cakebox.objects.all()
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAdminUser]


class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=Cakebox.objects.all()
    model=Cakebox
    http_method_names=["post"]