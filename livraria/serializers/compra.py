from rest_framework import serializers
from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from livraria.models import Compra, ItensCompra


class ItensCompraSerializer(ModelSerializer):
    total = SerializerMethodField()

    class Meta:
        model = ItensCompra
        fields = ("quantidade", "preco_item", "total", "livro")
        depth = 2

    def get_total(self, instance):
        return instance.quantidade * instance.preco_item


class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email", read_only=True)
    status = CharField(source="get_status_display", read_only=True)
    data = serializers.DateTimeField(read_only=True)
    itens = ItensCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ("id", "usuario", "data", "status", "total", "itens")


class CriarEditarItensCompraSerializer(ModelSerializer):
    class Meta:
        model = ItensCompra
        fields = ("livro", "quantidade")

    def validate(self, data):
        if data["quantidade"] > data["livro"].quantidade:
            raise serializers.ValidationError({"quantidade": "Quantidade solicitada não disponível em estoque."})
        return data


class CriarEditarCompraSerializer(ModelSerializer):
    itens = CriarEditarItensCompraSerializer(many=True)
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    data = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Compra
        fields = ("usuario", "data", "itens")

    def create(self, validated_data):
        itens = validated_data.pop("itens")
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            item["preco_item"] = item["livro"].preco  # Coloquem o preço do livro no item de compra
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra

    def update(self, instance, validated_data):
        itens = validated_data.pop("itens")
        if itens:
            instance.itens.all().delete()
            for item in itens:
                item["preco_item"] = item["livro"].preco  # Coloquem o preço do livro no item de compra
                ItensCompra.objects.create(compra=instance, **item)
        instance.save()
        return instance
