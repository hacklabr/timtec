# Atualizando o TIMTec para uma nova versão

## Instale o phantomjs

Se estiver em dúvida, execute novamente o comando abaixo.

```
$ apt-get install -y phantomjs
```

## Renomeie o arquivo settings_production.py para settings_local.py

Na raíz do repositório, faça:
```
$ mv timtec/settings_production.py timtec/settings_local.py
```

## Proceda com o procedimento de atualização normal

Siga os passos descritos na [[Atualização]].

Fique atento se a nova versão não possui necessidade de alguma configuração adicional. A partir da [versão 3.0.2](https://github.com/hacklabr/timtec/releases/tag/v3.0.2), por exemplo, é necessário que seja [configurado a variável YOUTUBE_API_KEY](https://github.com/hacklabr/timtec/wiki/Configura%C3%A7%C3%A3o#configura%C3%A7%C3%A3o-da-chave-da-api-do-youtube)

