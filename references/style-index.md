# Index de choix du style

Arbre de décision à utiliser quand le créateur donne un sujet sans savoir quel style il
veut. Il sert à **proposer 2 options argumentées**, pas à choisir à sa place.

## Arbre de décision par sujet

| Forme du sujet donné par le créateur | Styles à proposer | Pourquoi |
|---|---|---|
| « comment faire X », « l'erreur que tout le monde fait avec X » | `a1-astuce-si-tu`, puis `a2-objet-mecanisme` | structure méthode et impératifs |
| un objet, un produit, un prix à justifier | `a2-objet-mecanisme`, puis `a3-fait-choc` | mécanisme caché / fait constaté |
| un lieu, un univers fictif, l'origine d'une mode | `a2-objet-mecanisme`, puis `d1-lore-enquete` | décodage court, ou enquête datée si le sujet a une histoire |
| une personne réelle, un exploit, une étude scientifique | `a3-fait-choc`, puis `b2-defi-chiffres` | escalade chronologique ou chiffres |
| un drama entre créateurs, une actu communautaire courte | `a3-fait-choc`, puis `d2-top-suspense` | récit choc unique, ou top si plusieurs cas |
| « N choses / N types / N règles » à traiter avec humour | `b1-top-vannes`, puis `b3-quiz-score` | items courts + vanne, ou test en points |
| « ce qu'on ne veut plus voir », promesse non tenue | `b1-top-vannes` (variante plainte) | le top devient règlement de comptes |
| un contenu rare, un record, un contenu quasi inaccessible | `b2-defi-chiffres`, puis `a3-fait-choc` | statistique de rareté puis escalade |
| un test en direct, un comparatif chiffré, une théorie à prouver | `b2-defi-chiffres` (variantes test / countdown / théorie) | chiffres affichés + sas avant le résultat |
| une communauté qui doit se reconnaître et se noter | `b3-quiz-score`, puis `b1-top-vannes` | items-reconnaissance + score |
| des setups, composants ou annonces à juger | `b4-notation-verdict`, puis `b1-top-vannes` | note sur 10 ou tier, verdict assumé |
| une actu artistique, un hommage, une controverse | `c1-actu-emotion`, puis `c2-top-culturel` | hyperbole de réaction + décodage |
| un classement culturel, une histoire collective, une diaspora | `c2-top-culturel`, puis `c1-actu-emotion` | contexte historique par item |
| l'histoire vraie et datée d'un jeu ou d'un univers | `d1-lore-enquete`, puis `a3-fait-choc` | dates-preuves + révélation vérifiable |
| un top 3 de moments vécus par des créateurs | `d2-top-suspense`, puis `b1-top-vannes` | teasing du dernier + sas d'abonnement |
| un sujet de jeu vidéo, de sport ou de culture pop avec avis tranché | `b1-top-vannes`, `b2-defi-chiffres` ou `b4-notation-verdict` | selon que le ton est drôle, chiffré ou juge |

## Les 3 questions qui tranchent

1. **Le créateur a-t-il un avis ou une vanne sur le sujet ?**
   Oui → famille B. Non → famille A (curiosité neutre), C (culture expliquée) ou
   D (enquête documentée).
2. **Le sujet porte-t-il une émotion collective ou un engagement ?**
   Oui → famille C. Non → famille A, B ou D.
3. **Le script doit-il faire faire quelque chose au spectateur ?**
   Oui, reproduire une méthode → `a1` / `a2`. Oui, compter un score → `b3`. Oui,
   juger et noter → `b4`. Oui, s'abonner avant la chute → `d2` (sas). Non → `a3`,
   `b1`, `b2`, `c2`, `d1`.

## Correspondance avec le corpus d'origine

| Style | Chaîne dont le style est tiré | Référence à citer si le créateur veut des exemples |
|---|---|---|
| `a1`, `a2`, `a3` | Fitness-Muscu (+ Jinskow, CieloTech, Ysto, Shota, luK en variantes) | sujets grand public, zéro CTA, titres à emoji |
| `b1`, `b2`, `b3` | Jey & Max (+ y0us, Jinskow, Shota en variantes `b2`) | gaming, tutoiement, titres en MAJUSCULES |
| `b4` | CieloTech | tech & setup, verdict noté, hashtags dans le titre |
| `c1`, `c2` | Slim Infos Musique | musique et culture, 3e personne, CTA systématique |
| `d1` | Ysto Roblox (+ Jinskow) | lore daté et vérifiable, question + abonnement |
| `d2` | luK | top 3 à suspense, sas d'abonnement, hashtags `#pourtoi #viral #fyp` |

## Techniques transversales (tous styles)

- **Sas d'abonnement** : retarder la chute ou le dernier item par un appel chiffré
  (« avant que je te dise, abonne-toi parce qu'on rush les 100 000 abonnés »). Mesuré
  en `d2` (4/4), `b4` (giveaway, 2/7), `b2` (y0us, mid-video) et `a3` (ShotaPrime, luK).
  Jamais en ouverture, jamais après la chute.
- **Renvoi** : finir par « Va voir ma dernière vidéo » (`d2` : 4/4, `a3` drama).
- **Titres à hashtags** : réservés à `b4`, `d2`, y0us et Shota — partout ailleurs, titre
  sans hashtag (voir `references/hashtags.md`).

## Ce qui ne doit pas arriver

- Écrire un script sans style annoncé.
- Appliquer le CTA d'une famille à une autre (`a1`, `a2`, `a3`, `b1`, `b2` : aucun CTA
  final sauf sas documenté dans la fiche ; `b4` : verdict, pas d'abo final ; `b3` :
  score ; `c1`/`c2`/`d1` : question + abonnement ; `d2` : sas + renvoi).
- Choisir un style de famille B pour un sujet sur lequel le créateur n'a ni avis ni
  connaissance : la vanne tomberait à plat.
- Choisir `c1` pour un sujet peu documenté : le beat de décodage exige des détails
  vérifiables.