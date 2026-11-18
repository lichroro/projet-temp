#!/bin/bash
# Kiosque de cuisine : affiche en permanence la page de supervision.
# --kiosk        : plein ecran, sans barre d'adresse ni onglets
# --noerrdialogs : aucune boite de dialogue d'erreur
exec chromium-browser --kiosk --noerrdialogs http://127.0.0.1:5000/affichage
