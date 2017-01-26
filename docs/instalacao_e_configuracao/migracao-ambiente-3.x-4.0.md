Migração de ambientes 3.x para 4.0
==================================

Ressalvas:
----------

Caso você esteja na versão 3.3, no momento da realização dos migrations do banco, ocorrerá o seguinte erro:
```
django.db.utils.ProgrammingError: column "user_can_certificate_even_without_progress" of relation "core_class" already exists
```

Isso significa que o campo citado já existe na tabela. Neste caso, basta executar o seguinte trecho abaixo:
```
# (executar procedimentos com o virtualenv ativado)
python manage.py migrate core 0021 --fake
```
