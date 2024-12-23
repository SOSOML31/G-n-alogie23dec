# Contraintes métier

## Relation parent-enfant
- Un individu ne peut pas être né avant ses parents biologiques.
- Un individu ne peut pas être parent et enfant de la même personne.

## Attributs individuels
- Les champs `prénom`, `nom de famille` et `date de naissance` sont obligatoires.
- La `date de mort` doit être postérieure à la `date de naissance` (si présente).
- Une combinaison `prénom + nom + date de naissance` doit être unique.

## Relations
- Chaque individu peut avoir entre 0 et 2 parents biologiques.
- Les relations incluent des parents biologiques, adoptifs, ou beaux-parents.