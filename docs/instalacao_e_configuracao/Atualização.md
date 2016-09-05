# Atualizando o TIMTec para uma nova versão

As versões do TIMTec estão disponíveis aqui: https://github.com/hacklabr/timtec/releases

Cada versão do TIMTec é uma tag no repositório git.

O primeiro passo é atualizar o código. Dentro da raiz do repositório, com o usuário criado para instalação do software, execute:

```
$ git pull
$ git checkout NOME-DA-VERSAO
```

Onde o NOME-DA-VERSAO deve ser substítuido pela tag da versão desejada. Exemplos: `git checkout v3.1.1`.

Feito isso, [ative o ambiente virtual python](https://github.com/hacklabr/timtec/wiki/Instala%C3%A7%C3%A3o#criando-ambiente-virtual-manualmente-opcional-use-este-ou-o-make-create-production) e em seguida faça:

`$ make update`

Feito isso, o software estará atualizado.
