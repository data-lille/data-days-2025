---
title: 'IA en prod : Détection d''intention en 10ms : quantization, OpenVINO, OnnxRuntime...
  l''art de faire (vraiment) vite'
kind: conference_longue
speakers:
- adrien-legrand
short_description: "Chez Leroy Merlin, l’intention de l’utilisateur est un enjeu central\
  \ : les requêtes du moteur de recherche expriment souvent plus qu’un besoin produit\
  \ (un projet, un problème à résoudre, un besoin de service, parfois tout à la fois...).\
  \ La détecter permet **d'orienter immédiatement** l’utilisateur vers le bon parcours\
  \ (recherche multiple, conseil, configurateur, service, FAQ…) et d’améliorer nettement\
  \ **la pertinence** comme **l’expérience**.\n\nL'année dernière, nous présentions\
  \ notre solution de reformulation de requêtes du moteur de recherche, développée\
  \ pour mieux répondre aux nouveaux usages.\n\nCette année, focus sur la V2 : **la\
  \ détection d’intention**.  \nAu cœur du sujet : comment obtenir une API de classification\
  \ de texte multi-classes qui répond en **moins de 10 ms**.\n\nL’objectif est la\
  \ très haute performance au p99 en production, avec des **pics à 200 requêtes/seconde**.\
  \ Nous présenterons la démarche qui nous a permis d’y arriver : choisir un modèle\
  \ ultra-rapide (spoiler : *rexbert micro*) et une stack d’inférence CPU adaptée\
  \ (*ONNX Runtime / OpenVINO / torchao...*), et comprendre ce qu’est la **quantization**,\
  \ et quand celle-ci a (ou n’a pas) d’intérêt.\n\nNous aborderons aussi les points\
  \ clés : comment **mesurer** correctement la performance et comment **industrialiser**\
  \ la mise en place du service, de la pipeline de machine learning jusqu’au déploiement\
  \ de l’API.\n\nCe projet est l’opportunité de formaliser un **blueprint réutilisable**\
  \ pour déployer rapidement d’autres briques ultra-rapides de classification texte\
  \ (classifieurs en chaîne, chatbot, analyse de descriptions de produit de marketplace,\
  \ messages, avis utilisateurs…)."
start_time: '10:00'
track: Amphithéâtre René Thery
categories:
- Data Science & IA
is_extra: false
published: true
---

Chez Leroy Merlin, l’intention de l’utilisateur est un enjeu central : les requêtes du moteur de recherche expriment souvent plus qu’un besoin produit (un projet, un problème à résoudre, un besoin de service, parfois tout à la fois...). La détecter permet **d'orienter immédiatement** l’utilisateur vers le bon parcours (recherche multiple, conseil, configurateur, service, FAQ…) et d’améliorer nettement **la pertinence** comme **l’expérience**.

L'année dernière, nous présentions notre solution de reformulation de requêtes du moteur de recherche, développée pour mieux répondre aux nouveaux usages.

Cette année, focus sur la V2 : **la détection d’intention**.  
Au cœur du sujet : comment obtenir une API de classification de texte multi-classes qui répond en **moins de 10 ms**.

L’objectif est la très haute performance au p99 en production, avec des **pics à 200 requêtes/seconde**. Nous présenterons la démarche qui nous a permis d’y arriver : choisir un modèle ultra-rapide (spoiler : *rexbert micro*) et une stack d’inférence CPU adaptée (*ONNX Runtime / OpenVINO / torchao...*), et comprendre ce qu’est la **quantization**, et quand celle-ci a (ou n’a pas) d’intérêt.

Nous aborderons aussi les points clés : comment **mesurer** correctement la performance et comment **industrialiser** la mise en place du service, de la pipeline de machine learning jusqu’au déploiement de l’API.

Ce projet est l’opportunité de formaliser un **blueprint réutilisable** pour déployer rapidement d’autres briques ultra-rapides de classification texte (classifieurs en chaîne, chatbot, analyse de descriptions de produit de marketplace, messages, avis utilisateurs…).
