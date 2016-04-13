## Sobre o OpenID

> OpenID é um sistema de identificação desenvolvido por Brad Fitzpatrick do LiveJournal. Trata-se de uma rede distribuída na qual a identidade do utilizador é dada por uma URL ou XRI que pode ser verificada por qualquer servidor executando o protocolo. [Wikipedia](https://pt.wikipedia.org/wiki/OpenID)

## OpenID e Timtec

O plugin chamado [django-allauth](https://github.com/pennersr/django-allauth) é responsável por prover autenticação de usuário através de aplicativos sociais e também pelo OpenID. 

Através da configuração do arquivo `settings.py` presente no Timtec, é possível ter os botões de autenticação do usuário via OpenID.

## Logando no Timtec com OpenID do Moodle

Para que usuários do Moodle possam se autenticar no Timtec é necessário ter uma instância do Moodle com plugin [OpenID provider](https://moodle.org/plugins/local_openid_idp) instalado.

Supondo que essa instância esteja no endereço *http://meu-moodle.com*, teremos uma URL de OpendID que é *http://meu-moodle.com/local/openid_idp/*.

Com a URL do OpenID podemos adicionar uma entrada em `settings_local.py`, da seguinte forma:

```python
#
# restante do settings_local.py
#

SOCIALACCOUNT_PROVIDERS['openid'] = {
        'SERVERS': [
            {
                'id': 'moodle',
                'name': 'Moodle',
                'openid_url': 'http://meu-moodle.com/local/openid_idp/'
            },
        ]
    }
```

O fluxo ficará como o seguinte:

1. O usuário anônimo chega a tela inicial
2. Escolha se atenticar pelo Moodle
3. O usuário será direcionado ao site com o Moodle
4. Se o usuário estiver autenticado ele deve concordar em ceder suas informações básicas ao Titmec
5. O usuário é então direcionado de volta ao site do timtec, onde já estará logado.

## Referências

[1] - https://www.turnkeylinux.org/moodle
[2] - https://github.com/pennersr/django-allauth
[3] - https://moodle.org/plugins/local_openid_idp