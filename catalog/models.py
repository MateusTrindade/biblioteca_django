from django.db import models
from django.urls import reverse
import uuid  # Necessário para criar instancias únicas de livros
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Genre(models.Model):
    # Esse modelo irá armazenar dados sobre os generos dos livros
    # Possui um campo chamado name, que armazena o nome do genero
    # É um campo de texto do tipo CharField
    name = models.CharField(
        max_length=200, help_text='Insira o genero do livro (ex: Ficção Cinetifica)')

    # Método que retorna o nome do genero
    def __str__(self):
        return self.name


# Desafio: Campo linguagem
class Lenguage(models.Model):
    leng = models.CharField(
        max_length=100, help_text='Insira a lingua do livro')

    def __str__(self):
        return self.leng


class Book(models.Model):
    title = models.CharField(max_length=200)
    # Author é uma chave estrangeira pois nesse projeto um livro só pode ter um author,
    # mas cada author pode ter diversos livros. Sendo então relação 1 para muitos.
    # Caso o autor seja apagado, o campo será preenchido como nulo
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text='Insira uma breve descrição do livro')
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True, help_text='<a href="https://www.isbn-international.org/content/what-isbn">Número ISBN</a> com 13 caracteres')
    # Genero é um campo muitos para muitos
    genre = models.ManyToManyField(
        Genre, help_text='Selecione um genero para esse livro')

    # Um livro é escrito em apenas uma ligua, mas podem haver muitos livros escritos na mesma lingua
    lenguage = models.ForeignKey(
        Lenguage, on_delete=models.SET_NULL, null=True, help_text='Selecione uma lingua para esse livro')

    def __str__(self):
        return self.title

    # Essa função retorna uma URL que pode ser usada para acessar detalhes de
    # registros desse modelo. Mas é preciso criar o devido mapeamento
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID unico deste livro em toda biblioteca')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponivel'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro',
    )

    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
