# POCKET SIGNAL PRO — déploiement depuis Android

## Ce que fait cette version
- Tableau de bord web.
- Catalogue des symboles chargé depuis OTCharts pour Pocket Option OTC ou Forex réel.
- Analyse à la demande avec EMA 9/21, RSI 14 et momentum.
- Durées OTC : 5, 15, 30 secondes, 1 minute et 5 minutes. 10 secondes est agrégé à partir de deux bougies de 5 secondes.
- Forex réel : 1 minute et 5 minutes dans ce fournisseur.
- Aucun login Pocket Option, aucune exécution d'ordre.

Le score affiché est heuristique, pas une probabilité de réussite. La version n'est pas un scanner continu.

## Étape A — obtenir une clé de données
1. Depuis Chrome Android, ouvre https://otcharts.com/api-key
2. Crée/confirmes ton compte OTCharts et crée une clé.
3. Copie la clé une seule fois et garde-la privée.
4. Le niveau gratuit est limité à un seul marché, cinq instruments et 200 requêtes durant le premier mois, sans flux en direct. Pour toutes les paires et le streaming, consulte les forfaits et leurs limites avant tout paiement.
5. Ne colle jamais la clé dans un message public ni dans le code HTML.

## Étape B — mettre le projet sur GitHub depuis Android
1. Télécharge et décompresse `pocket_signal_pro_android.zip` sur ton téléphone.
2. Ouvre https://github.com dans Chrome et connecte-toi/crée ton compte si nécessaire.
3. Crée un nouveau dépôt nommé `pocket-signal-pro`. Pour le déploiement facile, choisis Public (ne mets aucun secret dans le dépôt).
4. Dans le dépôt, utilise Add file > Upload files et téléverse les fichiers du dossier du projet : `index.html`, `server.py`, `requirements.txt`, `Procfile`, `render.yaml`, `.gitignore`. Tu peux aussi téléverser README si tu en ajoutes un.
5. Valide avec Commit changes.

## Étape C — déployer sur Render
1. Ouvre https://render.com et connecte-toi avec GitHub.
2. Dans Render, choisis New > Web Service, puis le dépôt `pocket-signal-pro`.
3. Render peut détecter le fichier `render.yaml`. Vérifie :
   - Build command : `pip install -r requirements.txt`
   - Start command : `gunicorn server:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
4. Dans Environment, ajoute `OTCHARTS_API_KEY` et colle ta clé OTCharts comme valeur. Ne l'ajoute jamais dans GitHub.
5. Lance le déploiement. Une fois terminé, Render donne une adresse HTTPS `https://...onrender.com`.
6. Ouvre cette adresse dans Chrome Android.

## Étape D — installer comme raccourci
Dans Chrome Android, ouvre le site déployé > menu ⋮ > Ajouter à l'écran d'accueil (ou Installer l'application si proposé). Cela crée un raccourci. Le serveur reste hébergé sur Render.

## Limites à connaître
- Render Free met les services web en veille après 15 minutes sans activité ; le premier chargement suivant peut être lent. Ne l'utilise pas pour un scanner permanent ou des alertes critiques.
- Le plan API gratuit OTCharts ne donne pas de streaming en direct et ne couvre que cinq instruments d'un marché. Il ne suffit donc pas à réaliser l'objectif complet « toutes les paires + flux continu ».
- Le flux Pocket Option OTC et le Forex réel sont deux séries différentes. Un prix Forex réel ne remplace pas le prix OTC.
- Les intervalles disponibles sont imposés par le fournisseur : Pocket Option OTC fournit 5, 15, 30, 60 et 300 secondes ; 10 secondes est calculé en agrégeant deux bougies de 5 secondes. Forex réel commence à 60 secondes.
- Ce projet ne se connecte pas à ton compte Pocket Option et ne passe aucun ordre. Ne donne jamais ton mot de passe, ton code 2FA ou ton cookie/SSID à un service tiers.

## Dépannage
- « Clé absente » : vérifie `OTCHARTS_API_KEY` dans Environment sur Render, puis redéploie.
- « Plan does not open venue » ou HTTP 403 : le marché OTC/Forex n'est pas inclus dans ton plan API.
- « Quota » ou HTTP 429 : limite de requêtes atteinte. Ne relance pas le bouton en boucle.
- Catalogue vide : vérifie la clé, le marché autorisé et le forfait.
