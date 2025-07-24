import os
import glob
from typing import List, Dict, Any
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

class DocumentationAnalyzer:
    """
    Analyse la cohérence entre la documentation (fichiers Markdown) et le code source (fichiers Python).
    Utilise le fichier de contexte global pour comprendre les standards du projet.
    """

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.context_path = os.path.join(project_root, "context", "aura_context.md")
        self.docs_path = os.path.join(project_root, "docs")
        self.src_path = os.path.join(project_root, "src")
        self.context = self._load_context()

    def _load_context(self) -> Dict[str, Any]:
        """Charge le contexte à partir du fichier aura_context.md."""
        logging.info(f"Chargement du contexte depuis : {self.context_path}")
        try:
            with open(self.context_path, 'r', encoding='utf-8') as f:
                # Pour l'instant, une simple lecture. Plus tard, on pourrait parser le markdown.
                content = f.read()
            logging.info("Contexte chargé avec succès.")
            return {"content": content}
        except FileNotFoundError:
            logging.error(f"Fichier de contexte non trouvé à l'adresse : {self.context_path}")
            return {}
        except Exception as e:
            logging.error(f"Erreur lors du chargement du contexte : {e}")
            return {}

    def analyze(self) -> List[str]:
        """
        Lance l'analyse complète et retourne une liste de problèmes de cohérence.
        """
        if not self.context:
            return ["Analyse impossible : le contexte n'a pas pu être chargé."]

        logging.info("Début de l'analyse de la documentation...")
        
        markdown_files = self._find_files(self.docs_path, "*.md")
        python_files = self._find_files(self.src_path, "*.py")

        issues = []
        issues.extend(self._check_undocumented_files(markdown_files, python_files))
        
        if not issues:
            logging.info("Analyse terminée. Aucune incohérence majeure détectée.")
        else:
            logging.warning(f"Analyse terminée. {len(issues)} problèmes trouvés.")

        return issues

    def _find_files(self, path: str, pattern: str) -> List[str]:
        """Trouve tous les fichiers correspondant à un pattern dans un répertoire."""
        return glob.glob(os.path.join(path, '**', pattern), recursive=True)

    def _check_undocumented_files(self, markdown_files: List[str], python_files: List[str]) -> List[str]:
        """
        Vérifie si des fichiers Python ne sont jamais mentionnés dans la documentation.
        """
        issues = []
        python_basenames = {os.path.basename(f) for f in python_files}
        
        # Concaténer tout le contenu de la documentation en une seule chaîne
        full_docs_content = ""
        for md_file in markdown_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    full_docs_content += f.read()
            except Exception as e:
                issues.append(f"Impossible de lire le fichier Markdown '{md_file}': {e}")
        
        if not full_docs_content:
            issues.append("Le contenu de la documentation est vide ou n'a pas pu être lu.")
            return issues

        # Vérifier chaque fichier python
        for py_basename in python_basenames:
            # On ignore les fichiers __init__.py et les fichiers dans __pycache__
            if py_basename == "__init__.py" or "__pycache__" in py_basename:
                continue
            
            if py_basename not in full_docs_content:
                issue_msg = f"Fichier non documenté : Le fichier '{py_basename}' existe dans le code source mais n'est mentionné dans aucun document du répertoire /docs."
                issues.append(issue_msg)
                logging.warning(issue_msg)

        logging.info("Vérification des fichiers non documentés terminée.")
        return issues


if __name__ == '__main__':
    # Exemple d'utilisation
    project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    analyzer = DocumentationAnalyzer(project_root_dir)
    analysis_results = analyzer.analyze()

    print("\n--- Rapport d'Analyse de la Documentation ---")
    if analysis_results:
        for issue in analysis_results:
            print(f"- [PROBLÈME] {issue}")
    else:
        print("Aucun problème de cohérence détecté.")
    print("-------------------------------------------")