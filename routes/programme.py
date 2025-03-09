# routes/programme.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date, time
from models import db, Accueil, Programme
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Affiche les logs de niveau DEBUG et supérieur
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

programme_bp = Blueprint('programme', __name__, url_prefix='/programme')

def get_next_candidate(total_candidates=20):
    logger.debug("--> get_next_candidate")
    # Ensemble de tous les candidats possibles (de 1 à total_candidates)
    all_candidates = set(range(1, total_candidates + 1))
    logger.debug("All Candidates : %s", all_candidates)
    # Récupérer tous les candidate_id déjà utilisés dans la table Programme
    used_candidates = {
        programme.candidate_id
        for programme in Programme.query.all()
        if programme.candidate_id is not None
    }
    
    # Déterminer les candidats disponibles
    available_candidates = all_candidates - used_candidates
    logger.debug("Available Candidates : %s", available_candidates)
    # Si tous les identifiants ont été utilisés, réinitialiser la rotation
    if not available_candidates:
        available_candidates = all_candidates
    
    # Retourner le candidat disponible le plus petit (ou appliquer une autre logique de sélection)
    return min(available_candidates)

@programme_bp.route('/generate', methods=['GET', 'POST'])
def generate_programme():
    logger.debug("--> generate_programme")
    if request.method == 'POST':
        # Récupération et conversion de l'heure
        horaire_planning_str = request.form.get('horairePlanning')
        logger.debug("horaire_planning_str : %s", horaire_planning_str)
        try:
            logger.debug("--> generate_programme --try in")
            horaire = datetime.strptime(horaire_planning_str, '%H:%M').time() if horaire_planning_str else datetime.now().time()
            logger.debug("--> generate_programme --try out")
        except ValueError:
            flash("L'heure n'est pas au format correct (HH:MM).")
            return redirect(url_for('programme.generate_programme'))
        
        # Nombre de perchistes (2 ou 4)
        nb_perchistes_str = request.form.get('nbPerchistes')
        try:
            nb_perchistes = int(nb_perchistes_str) if nb_perchistes_str else 4
            if nb_perchistes not in (2, 4):
                nb_perchistes = 4
        except ValueError:
            nb_perchistes = 4

        # Récupération des indisponibilités
        indisponibles_str = request.form.get('indisponibles', '')
        indisponibles = {couple.strip().lower() for couple in indisponibles_str.split(',') if couple.strip()}
        logger.debug("Indisponibles normalisés : %s", indisponibles)

        total_prog = Programme.query.count()  # Nombre de programmes déjà générés
        logger.debug("total_prog : %s", total_prog)
        
        # Récupérer et trier les membres d'Accueil (32 couples)
        accueil_members = sorted(Accueil.query.all(), key=lambda m: (m.nom, m.prenom))
        logger.debug("Les membres d'accueil : %s", accueil_members)

        # Calcul de l'offset global : chaque programme utilise 18 couples.
        offset_accueil = (total_prog * 18) % len(accueil_members) if accueil_members else 0
        logger.debug("offset_accueil calculé : %d", offset_accueil)

        # Ensemble global pour garantir l'unicité sur tout le programme
        used_global = set()

        def select_member_category(members, used, offset, role_index=0, indisponibles=set()):
            logger.debug("--> select_member_category")
            n = len(members)
            logger.debug("--> n : %d", n)
            for i in range(n):
                index = (offset + role_index + i) % n
                candidate_raw = f"{members[index].nom.strip()} {members[index].prenom.strip()}"
                candidate_normalized = candidate_raw.lower()
                logger.debug("Vérification du candidat (role_index=%d): %s", role_index, candidate_normalized)
                if candidate_normalized in indisponibles:
                    logger.debug("Le candidat %s est indisponible.", candidate_normalized)
                    continue
                if candidate_normalized in used:
                    logger.debug("Le candidat %s est déjà utilisé.", candidate_normalized)
                    continue
                used.add(candidate_normalized)
                logger.debug("Candidat sélectionné pour role_index %d: %s", role_index, candidate_raw)
                return candidate_raw
            logger.debug("Aucun candidat disponible pour role_index %d.", role_index)
            candidate_raw = f"{members[(offset + role_index) % n].nom.strip()} {members[(offset + role_index) % n].prenom.strip()}"
            logger.debug("Retour fallback pour role_index %d: %s", role_index, candidate_raw)
            return candidate_raw

        # Génération des 18 rôles pour le programme (poste_01 à poste_18)
        point_01 = select_member_category(accueil_members, used_global, offset_accueil, 0, indisponibles)
        point_02 = select_member_category(accueil_members, used_global, offset_accueil, 1, indisponibles)
        point_03 = select_member_category(accueil_members, used_global, offset_accueil, 2, indisponibles)
        point_04 = select_member_category(accueil_members, used_global, offset_accueil, 3, indisponibles)
        point_05 = select_member_category(accueil_members, used_global, offset_accueil, 4, indisponibles)
        point_06 = select_member_category(accueil_members, used_global, offset_accueil, 5, indisponibles)
        point_07 = select_member_category(accueil_members, used_global, offset_accueil, 6, indisponibles)
        point_08 = select_member_category(accueil_members, used_global, offset_accueil, 7, indisponibles)
        point_09 = select_member_category(accueil_members, used_global, offset_accueil, 8, indisponibles)
        point_10 = select_member_category(accueil_members, used_global, offset_accueil, 9, indisponibles)
        point_11 = select_member_category(accueil_members, used_global, offset_accueil, 10, indisponibles)
        point_12 = select_member_category(accueil_members, used_global, offset_accueil, 11, indisponibles)
        point_13 = select_member_category(accueil_members, used_global, offset_accueil, 12, indisponibles)
        point_14 = select_member_category(accueil_members, used_global, offset_accueil, 13, indisponibles)
        point_15 = select_member_category(accueil_members, used_global, offset_accueil, 14, indisponibles)
        point_16 = select_member_category(accueil_members, used_global, offset_accueil, 15, indisponibles)
        point_17 = select_member_category(accueil_members, used_global, offset_accueil, 16, indisponibles)
        point_18 = select_member_category(accueil_members, used_global, offset_accueil, 17, indisponibles)

        # Optionnel : pour candidate_id, on peut utiliser le nombre de membres d'accueil
        candidate_id = get_next_candidate(total_candidates=len(accueil_members))
        
        new_programme = Programme(
            horairePlanning = horaire,
            poste_01 = point_01, 
            poste_02 = point_02, 
            poste_03 = point_03, 
            poste_04 = point_04, 
            poste_05 = point_05, 
            poste_06 = point_06, 
            poste_07 = point_07, 
            poste_08 = point_08, 
            poste_09 = point_09, 
            poste_10 = point_10,
            poste_11 = point_11, 
            poste_12 = point_12,
            poste_13 = point_13, 
            poste_14 = point_14, 
            poste_15 = point_15, 
            poste_16 = point_16, 
            poste_17 = point_17, 
            poste_18 = point_18, 
            candidate_id = candidate_id
        )

        db.session.add(new_programme)
        db.session.commit()

        flash("Programme généré avec succès!")
        return redirect(url_for('programme.list_programme'))

    return render_template('programme/generate.html')

@programme_bp.route('/')
def list_programme():
    logger.debug("--> list_programme")
    programmes = Programme.query.order_by(Programme.horairePlanning.desc()).all()
    return render_template('programme/list.html', programmes=programmes)

@programme_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_programme(id):
    logger.debug("--> edit_programme")
    programme = Programme.query.get_or_404(id)
    if request.method == 'POST':
        # Mettez à jour les champs du programme avec les données du formulaire
        programme.horairePlanning = request.form.get('horairePlanning', programme.horairePlanning)
        programme.poste_01 = request.form.get('poste_01', programme.poste_01)
        programme.poste_02 = request.form.get('poste_02', programme.poste_02)
        programme.poste_03 = request.form.get('poste_03', programme.poste_03)
        programme.poste_04 = request.form.get('poste_04', programme.poste_04)
        programme.poste_05 = request.form.get('poste_05', programme.poste_05)
        programme.poste_06 = request.form.get('poste_05', programme.poste_06)
        programme.poste_07 = request.form.get('poste_07', programme.poste_07)
        programme.poste_08 = request.form.get('poste_08', programme.poste_08)
        programme.poste_09 = request.form.get('poste_09', programme.poste_09)
        programme.poste_10 = request.form.get('poste_10', programme.poste_10)
        programme.poste_11 = request.form.get('poste_11', programme.poste_11)
        programme.poste_12 = request.form.get('poste_12', programme.poste_12)
        programme.poste_13 = request.form.get('poste_13', programme.poste_13)
        programme.poste_14 = request.form.get('poste_14', programme.poste_14)
        programme.poste_15 = request.form.get('poste_15', programme.poste_15)
        programme.poste_16 = request.form.get('poste_16', programme.poste_16)
        programme.poste_17 = request.form.get('poste_17', programme.poste_17)
        programme.poste_18 = request.form.get('poste_18', programme.poste_18)

        
        db.session.commit()
        flash("Programme modifié avec succès !", "success")
        return redirect(url_for('programme.list_programme'))
    return render_template('programme/edit.html', programme=programme)

@programme_bp.route('/delete/<int:id>', methods=['POST'])
def delete_programme(id):
    programme = Programme.query.get_or_404(id)
    db.session.delete(programme)
    db.session.commit()
    flash("Programme supprimé avec succès !", "success")
    return redirect(url_for('programme.list_programme'))