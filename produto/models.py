from django.db import models
from PIL import Image
import os
from django.conf import settings

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/&Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField() 
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )

    ''' Exibindo a imagem do produto no sistema'''
    @staticmethod
    def resize_image(img, new_width=800):
        print(img.name)

    ''' Redimencionando as imagens do sistema'''
    def save(self, *args, **kwargs):
        super() .save(*args, **kwargs)

    ''' Retornando o nome do objeto produto para o sistema'''
    def __str__(self):
        return self.nome

""""
Variacao:
            nome - char
            produto - FK Produto
            preco - Float
            preco_promocional - Float
            estoque - Int
"""