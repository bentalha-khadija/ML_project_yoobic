# 📝 Comment Mettre à Jour sur Git

## Commandes à Exécuter

### 1. Vérifier les changements
```bash
git status
```
Cela montre tous les fichiers modifiés, ajoutés ou supprimés.

---

### 2. Ajouter tous les changements
```bash
git add .
```
Le `.` signifie "tous les fichiers". Cela prépare tous vos changements pour le commit.

**OU** si vous voulez ajouter des fichiers spécifiques:
```bash
git add README.md
git add prepare_model.py
git add .gitignore
```

---

### 3. Faire le commit
```bash
git commit -m "Clean up project and add comprehensive README"
```

Le message entre guillemets décrit vos changements. Voici des exemples:
- `"Clean up project and add comprehensive README"`
- `"Remove unused files and update documentation"`
- `"Add logging system and clean project structure"`

---

### 4. Pousser vers GitHub
```bash
git push origin main
```

**OU** si votre branche s'appelle `master`:
```bash
git push origin master
```

---

## Commandes Complètes (tout en une fois)

```bash
# 1. Voir ce qui a changé
git status

# 2. Ajouter tout
git add .

# 3. Commit avec message
git commit -m "Clean up project and add comprehensive README"

# 4. Push vers GitHub
git push origin main
```

---

## Si c'est votre premier push

Si le repo n'existe pas encore sur GitHub:

```bash
# 1. Créer un repo sur GitHub d'abord (sur le site web)

# 2. Initialiser git localement (si pas déjà fait)
git init

# 3. Ajouter tous les fichiers
git add .

# 4. Premier commit
git commit -m "Initial commit: Store Sales Prediction App"

# 5. Lier au repo GitHub
git remote add origin https://github.com/votre-username/ML_project_yoobic.git

# 6. Pousser
git push -u origin main
```

---

## Vérifier après le push

```bash
# Voir l'historique des commits
git log --oneline

# Voir le remote configuré
git remote -v
```

---

## Commandes Utiles

```bash
# Voir les différences avant de commit
git diff

# Annuler des changements (ATTENTION: efface vos modifs!)
git checkout -- fichier.py

# Voir les fichiers dans le dernier commit
git ls-files

# Ignorer des fichiers (ajouter dans .gitignore)
echo "logs/*.log" >> .gitignore
```

---

## En cas d'erreur

**"fatal: not a git repository"**
→ Vous n'êtes pas dans le bon dossier ou git n'est pas initialisé
```bash
git init
```

**"failed to push"**
→ Quelqu'un d'autre a push avant vous
```bash
git pull origin main
git push origin main
```

**"Authentication failed"**
→ Configurez vos identifiants GitHub
```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre@email.com"
```

---

## Bon Flow de Travail

1. Travaillez sur votre code
2. `git status` - Voyez ce qui a changé
3. `git add .` - Ajoutez tout
4. `git commit -m "Message descriptif"` - Sauvegardez
5. `git push origin main` - Envoyez sur GitHub
6. Répétez!

---

**C'est tout!** Vos changements seront sur GitHub 🚀
