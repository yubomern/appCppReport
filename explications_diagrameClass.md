Relations entre class 
    Diagram UML  


1. -  Type de relations utilisées 
    Assoication :
        coreDumpManager utilise PlatfromUtils 
        Siginfications :
            une classe utilise une autre donnéés sans etre_propertaire 
    Composition:
        •	CoreDumpData contient :
            o	SystemMetrics
            o	CrashAnalysis
            Siginfications:
                Si CoreDumpData est détruit → ses composants aussi.

    Dépendance:
        •	CoreDumpManager dépend de CrashExporterFactory
            Signification :
                Utilisation dans une méthode, pas stockée comme attribut.
    Héritage / Implémentation :
        •	JsonCrashExporter implémente ICrashExporter
        •	CsvCrashExporter implémente ICrashExporter
        Signification :
            Permet le polymorphisme (changer le comportement dynamiquement).
    



1.2 Relations détaillées dans ton diagramme
    CoreDumpManager → CoreDumpData
    •	Type : Composition
    •	Le manager possède les données du crash

    CoreDumpManager → PlatformUtils
    •	Type : Association
    •	Utilisé pour accéder aux fonctions système

CoreDumpManager → CrashExporterFactory
    •	Type : Dépendance
    •	Utilisé uniquement lors de l’export

CrashExporterFactory → ICrashExporter
    •	Type : Création (Factory Pattern)
    •	Crée dynamiquement un exporteur

ICrashExporter → Json / CSV Exporter
    •	Type : Héritage (polymorphisme)

CoreDumpData → SystemMetrics & CrashAnalysis
•	Type : Composition






2. code explication : 
std::unique_ptr ? 
    std::unique_ptr<ICrashExporter>
2.1 Définition
std::unique_ptr est un smart pointer (pointeur intelligent) introduit en C++11.
->  Il représente une propriété unique d’un objet.



utiliséés 
. Gestion automatique de la mémoire
Pas besoin de faire :
    delete exporter;
Évite les fuites mémoire

. Sécurité
Impossible de copier un unique_ptr :
std::unique_ptr<A> p1 = ...;
std::unique_ptr<A> p2 = p1; ❌ (interdit )


Compatible avec le Factory Pattern
Dans ton cas :
    std::unique_ptr<ICrashExporter> Create(...)

Le factory crée et retourne un objet sans ambiguïté sur sa gestion mémoire.

Pourquoi pas       shared_ptr ?
unique_ptr	               shared_ptr
1 seul propriétaire ✅	  plusieurs propriétaires
rapide ⚡	              plus lent
simple	                    plus complexe
idéal embarqué ✅	        overhead



        





