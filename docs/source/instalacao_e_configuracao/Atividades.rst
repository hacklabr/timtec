Documentação do formato de dados das atividades
===============================================

Relacionamento
--------------

// type relationship

// data { "question":"Relacione as colunas", "column1":[ "Pizza",
"Esfiha", "Pastel", "Panqueca" ], "column2":[ "Quadrado", "Cilindro",
"Circulo", "Triangulo" ] }

// expected [ 3, 4, 1, 2 ]

Verdadeiro ou Falso
-------------------

// type trueorfalse

//data { "alternatives":[ "SQL 0e9 uma linguagem estruturada de
consultas", "MySQL 0e9 uma linguagem derivada do SQL direcionada a
programadores", "Bancos de dados s0e3o ideais para resolver problemas de
monitoramento de temperatura", "PostgreSQL 0e9 um sistema gerenciador de
banco de dados" ], "question":"Marque verdadeiro ou falso para as
afirma0e70f5es abaixo" }

//expected [ true, false, false, true ]

Multipla Escolha
----------------

//type multiplechoice

//data { "question":"Quais desses s0e3o bancos de dados relacionais",
"alternatives":[ "PostgreSQL", "MySQL", "CouchDB", "ISIS" ] }

//expected [ true, true, false, false ]

Escolha Simples
---------------

//type simplechoice

//data { "alternatives":[ "Envio de mensagens pela Internet",
"Cria0e70e3o de imagens para filmes", "Opera0e70e3o de uma m0e1quina de
corte", "Controle de assinaturas de uma jornal" ], "question":"Quais
destas aplica0e70f5es usam banco de dados?" }

//expected 3

Editor HTML5
------------

//type html5

//data { "data":"oi mundo" }

//expected { "expected\_answer":"oi mundo" }

Editor PHP
----------

**type**: php

**data**:

[ { "name": "index.php", "index": 0, "content": "", "editable": true },
{ "name": "file.php", "index": 1, "content": "", "editable": true } ]
**expected**:

{ "expected\_answer":"Hello, world" }
