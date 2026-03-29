1. Pourquoi avez-vous utilisé un Singleton ?

✅ Réponse :

J’ai utilisé le Singleton pour garantir qu’il existe une seule instance de CoreDumpManager, car il centralise toute la gestion des crashs.
Cela évite les incohérences et facilite le contrôle global du système.



2. Pourquoi utiliser une interface ICrashExporter ?

✅ Réponse :

L’interface permet d’appliquer le polymorphisme.
On peut ajouter facilement un nouveau format d’export sans modifier le code existant, ce qui respecte le principe Open/Closed.


3. Quelle est la différence entre association et composition ?

✅ Réponse :

La composition est une relation forte avec dépendance de cycle de vie, alors que l’association est une relation faible où les objets peuvent exister indépendamment.


4. Pourquoi utiliser un Factory Pattern ?

✅ Réponse :

Le Factory Pattern permet de centraliser la création des objets et de choisir dynamiquement le type d’exporteur, ce qui rend le code plus flexible et maintenable.

5. Pourquoi utiliser std::unique_ptr ?

✅ Réponse :

Pour assurer une gestion automatique de la mémoire, éviter les fuites et garantir qu’un seul objet possède la ressource.


6. Pourquoi pas shared_ptr ?

✅ Réponse :

shared_ptr introduit un coût supplémentaire avec le comptage de références.
Dans mon cas, un seul propriétaire suffit, donc unique_ptr est plus performant.

9. Pourquoi cette architecture ?

✅ Réponse :

Pour séparer les responsabilités, améliorer la maintenabilité et faciliter l’évolution du système.


Que se passe-t-il en cas de crash ?

✅ Réponse :

Le système capture les informations, les stocke dans CoreDumpData, lance l’analyse, puis exporte les résultats.
