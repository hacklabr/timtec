Vamos entender o sistema de temas com um exemplo.

Neste tutorial veremos como criar um novo tema para o Timtec para customizar a aparência padrão do sistema. Para isso faremos:

- Criar pastas necessárias para colocar os novos assets
- Configurar o timtec para usar o novo tema
- Trocar o banner da home do site

Para esse tutorial vamos supor que você já baixou o código, fez a instalação do sistema e esta com um gerenciador de arquivos aberto ou com um terminal na pasta raiz do projeto. O [guia de temas](https://github.com/hacklabr/timtec/wiki/Temas) pode ajudar com qualquer dúvida que você ficar sobre o sistema de temas.

# Criando a pasta de temas e estrutura

Dentro da raiz do projeto encontramos a pasta `themes` que contém todos os temas do timtec, é lá que iremos colocar os nossos arquivos para poder criar o nosso tema. Dentro da pasta podemos ver os temas que já foram incorporados ao desenvolvimento do sistema como `new-if` e `timtec`.

O tema mais importante ainda é o tema chamado `default`, é dele que todos os outros temas importam arquivos e tudo que não tiver definido em algum tema é definido no tema `default`. Uma regra simples para construir um tema novo é só copiar arquivos do `default` para outra pasta. 

O nome de cada tema é simplesmente o nome do diretório, no projeto preferimos ter só caracteres em minúsculo e traço ('-') para nomear os temas, assim a compatibilidade entre todos os sistemas e as várias formas que esse nome é usado fica garantida. Para esse tutorial vamos chamar o nosso tema de `tutorial`.

Para começar um tema crie uma pasta dentro da pasta `themes` com o nome de `tutorial`. Dentro dela coloque o mínimo necessário para um tema que são as pastas `templates` e a pasta `static`. A pasta `static` vai conter a nova imagem e as modificações de estilo que vamos fazer, então dentro dela crie a pasta `css` para os estilos e a pasta `img` para a imagens.

A sua arvore deve ficar assim:

```
themes
  ↳ tutorial 
      ↳ templates
      ↳ static
          ↳ css
          ↳ img
```

Essa é a estrutura básica que todos os temas devem seguir. No diretório templates você tem os arquivos de html template para gerar as paginas do sistema e no diretório static vc tem

# Configurar o tema no timtec

Criamos o nosso tema, mas agora é preciso dizer para o sistema usa-lo ao invés dos temas que já estavam instalados. O que controla qual é o tema atual é a variável `TIMTEC_THEME` no arquivo `settings-local.py`. Mudar essa variável para 'tutorial' (com as aspas) faz com que o nosso novo tema seja carregado.

Reinicie o Timtec e veja o seu tema rodando. Ele vai ser exatamente igual ao tema default, porque nós ainda não modificamos nenhum arquivo.

# Trocar o banner da home do sistema

Botar uma imagem qualquer em `themes/tutorial/static/images/banner-home.png`.

Recarregue o Timtec e você verá o novo banner na home no browser.

# Por onde continuar

Seguir o padrão definido do `default` e no [guia de temas](https://github.com/hacklabr/timtec/wiki/Temas) é o necessário para implementar todas as features necessárias para ter o timtec com a cara que você quiser.
