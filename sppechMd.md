Ce diagramme de classes représente l’architecture du système CoreDump que j’ai développé en C++.
Il montre les différentes classes, leurs responsabilités ainsi que leurs relations.
L’objectif est de structurer la gestion des crashs de manière modulaire, extensible et maintenable.


CoreDumpManager (classe principale)

La classe principale est CoreDumpManager.
Elle suit le design pattern Singleton afin de garantir une seule instance dans le système.

Son rôle est de :

collecter les données de crash
lancer l’analyse
exporter les résultats

Elle agit comme un contrôleur central.



CoreDumpData (stockage des données)

La classe CoreDumpData est un conteneur qui regroupe toutes les informations liées au crash :

les métadonnées
la stack trace
les informations système

Elle contient également deux objets importants :
SystemMetrics et CrashAnalysis.


Dans ce diagramme, plusieurs types de relations UML sont utilisés.

tout d'abord  le Composition

Par exemple, CoreDumpData contient SystemMetrics et CrashAnalysis.
C’est une relation de composition, car ces objets n’existent pas indépendamment.
Si CoreDumpData est détruit, ils le sont aussi.


par suite une  Association

CoreDumpManager utilise PlatformUtils pour accéder aux fonctions système.
C’est une association, car il utilise ces fonctions sans les posséder.


Dépendance

CoreDumpManager dépend de CrashExporterFactory uniquement lors de l’export.
C’est donc une dépendance temporaire.


Héritage (polymorphisme)

L’interface ICrashExporter est implémentée par :

JsonCrashExporter
CsvCrashExporter

Cela permet de changer dynamiquement le format d’export.


design patterns 
Factory Pattern

Le CrashExporterFactory permet de créer dynamiquement l’exporteur selon le format demandé.
Cela respecte le principe Open/Closed.

J’ai utilisé std::unique_ptr pour gérer la mémoire automatiquement.

Cela permet :

d’éviter les fuites mémoire
de garantir une propriété unique
d’améliorer les performances

Ce choix est particulièrement adapté aux systèmes embarqués.


En résumé, ce diagramme montre une architecture :

modulaire
extensible
sécurisée

grâce à l’utilisation des design patterns et des bonnes pratiques C++.