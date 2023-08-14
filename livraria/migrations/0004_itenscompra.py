# Generated by Django 4.2.3 on 2023-08-14 18:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("livraria", "0003_compra"),
    ]

    operations = [
        migrations.CreateModel(
            name="ItensCompra",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantidade", models.IntegerField(default=1)),
                (
                    "compra",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens",
                        to="livraria.compra",
                    ),
                ),
                (
                    "livro",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="+",
                        to="livraria.livro",
                    ),
                ),
            ],
        ),
    ]
