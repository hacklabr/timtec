bower install --save <nome-do-pacore>

Verificar o diff do arquivo bower.json se adicionou a dependência que você acabou de instalar.

O bower vai instalar um monte de arquivos que não precisamos, como sources, etc. 

NÃO COMITE ESTES ARQUIVOS!

Comite apenas os arquivos novos do pacote que você acabou de instalar e que você vai usar.

Em seguida, para zerar o bower_components, você pode fazer:

rm -rf bower_components
git checkout bower_components/
