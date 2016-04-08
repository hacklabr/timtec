# Documentação do formato de dados das atividades

## Relacionamento
// type
relationship


// data
{
  "question":"Relacione as colunas",
  "column1":[
    "Pizza",
    "Esfiha",
    "Pastel",
    "Panqueca"
  ],
  "column2":[
    "Quadrado",
    "Cilindro",
    "Circulo",
    "Triangulo"
  ]
}

// expected
[
  3,
  4,
  1,
  2
]

## Verdadeiro ou Falso
// type
trueorfalse


//data
{
  "alternatives":[
    "SQL \u00e9 uma linguagem estruturada de consultas",
    "MySQL \u00e9 uma linguagem derivada do SQL direcionada a programadores",
    "Bancos de dados s\u00e3o ideais para resolver problemas de monitoramento de temperatura",
    "PostgreSQL \u00e9 um sistema gerenciador de banco de dados"
  ],
  "question":"Marque verdadeiro ou falso para as afirma\u00e7\u00f5es abaixo"
}


//expected
[
  true,
  false,
  false,
  true
]

## Multipla Escolha

//type
multiplechoice


//data
{
  "question":"Quais desses s\u00e3o bancos de dados relacionais",
  "alternatives":[
    "PostgreSQL",
    "MySQL",
    "CouchDB",
    "ISIS"
  ]
}


//expected
[
  true,
  true,
  false,
  false
]

## Escolha Simples
//type
simplechoice

//data
{
  "alternatives":[
    "Envio de mensagens pela Internet",
    "Cria\u00e7\u00e3o de imagens para filmes",
    "Opera\u00e7\u00e3o de uma m\u00e1quina de corte",
    "Controle de assinaturas de uma jornal"
  ],
  "question":"Quais destas aplica\u00e7\u00f5es usam banco de dados?"
}

//expected
3

## Texto Markdown
//type
markdown


//data
{
  "data":"oi mundo"
}


//expected
[]

## Editor HTML5
//type
html5


//data
{
  "data":"<b>oi mundo</b>"
}


//expected
{
  "expected_answer":"<b>oi mundo</b>"
} 

## Editor PHP
**type**: php



**data**:

[
  {
    "name": "index.php",
    "index": 0,
    "content": "<?php echo 'Hello, world' ?>",
    "editable": true
  },
  {
    "name": "file.php",
    "index": 1,
    "content": "<?php echo 3 + 3 ?>",
    "editable": true
  } 
]
**expected**:

{ 
  "expected_answer":"Hello, world"
}