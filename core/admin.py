from django.contrib import admin
from core import models

for a in models.__dir__():
    if a[0] != "_" and a != "models" and a != "User" and a != "randint" and a != "datetime":
        exec(f"admin.site.register(models.{a})")
