from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse_lazy, reverse


class Categoria(models.Model):

    

    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Categoria_detail", kwargs={"pk": self.pk})



class Movie(models.Model):

    title = models.CharField(max_length=40, unique=True)
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE, blank=True, null=True)

    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1895),
            MaxValueValidator(2050),
        ]
    )

    rating = models.PositiveSmallIntegerField(choices=(
        (1, "★☆☆☆☆"),
        (2, "★★☆☆☆"),
        (3, "★★★☆☆"),
        (4, "★★★★☆"),
        (5, "★★★★★"),
    ))
