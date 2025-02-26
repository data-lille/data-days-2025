---
title: 'REX : Les sentence-transformers en prod, ou comment booster un search avec
  des LLMs'
kind: conference_longue
speakers:
- adrien-legrand
short_description: "Nous aborderons dans cette présentation les étapes de mise en production, les défis techniques rencontrés, les points et les questions notables que nous nous sommes posé, et enfin les leçons apprises au cours de ce projet."
start_time: "15:30"
track: Amphi Migeon
categories:
- Data Science & IA
published: true
---

La technologie avance et les attentes des utilisateurs évoluent. Notre moteur de recherche fonctionnait très bien pour les requêtes traditionnelles. Toutefois, les utilisateurs ont pris l’habitude des services toujours plus performants, et nous avons vu de plus en plus de requêtes en langage naturel émerger.  

En effet, **2 à 4 % des requêtes** sortent du cadre des requêtes traditionnelles, et le moteur de recherche actuel peine à leur fournir des réponses pertinentes (voire même juste *peine à fournir une réponse*).  
Pour relever ce défi sans pour autant refondre entièrement le moteur de recherche, nous avons développé une solution en deux temps :  

### 1. Classification  
Grâce aux **sentence transformers**, nous distinguons les requêtes "OK pour le search" et celles nécessitant une reformulation.
Cette étape permet d’identifier les recherches qui ne sont pas directement interprétables par le moteur de recherche.  

### 2. Reformulation  
Pour les requêtes classées "à reformuler", nous transformons la requête initiale en plusieurs requêtes ciblées grâce à un **LLM**.  
Par exemple, une requête vague comme *"construire mur chambre"* est convertie en plusieurs requêtes plus précises telles que :  
- "carreaux de plâtre" 
- "colle pour carreaux de plâtre"
- "enduit"
- "calicot"

Cette décomposition permet d’orienter le moteur de recherche vers des termes qu’il comprend et donc de répondre à quasiment toutes les requêtes, d’améliorer notablement la qualité des résultats, ainsi que l’expérience utilisateur.  

Nous aborderons dans cette présentation les étapes de mise en production, les défis techniques rencontrés, les points et les questions notables que nous nous sommes posé, et enfin les leçons apprises au cours de ce projet.
