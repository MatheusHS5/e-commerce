from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify

''' Model de Produto '''

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(upload_to='produto_imagens/&Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço') 
    preco_marketing_promocional = models.FloatField(default=0, verbose_name='Promoção!')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )

    ''' FORMATANDO OS VALORES A SEREM EXIBIDOS NO ADMIN'''
    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional_formatado(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')
    get_preco_promocional_formatado.short_description = 'Preço Promo.'

    ''' Exibindo a imagem do produto no sistema e redimencionando a imagem'''
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            print('retornando, largura original menor que nova largura')
            img_pil.close()
            return

        new_heigth = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_heigth), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )
        print('imagem foi redimencionada')

    ''' Redimencionando as imagens do sistema'''
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super() .save(*args, **kwargs)

    ''' Retornando o nome do objeto produto para o sistema'''
    def __str__(self):
        return self.nome

''' Model de Variação '''

class Variacao(models.Model):
    Produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    ''' Criando a opção plural para model'''
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
