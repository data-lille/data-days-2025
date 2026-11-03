---
title: 'A|A: Comment Libérer les Agents de l''Orchestration Centralisée'
kind: conference_longue
speakers:
- olivier-wulveryck
short_description: "# Le Pitch:\n\nAlors que les gains de performance des LLMs ralentissent,\
  \ le véritable levier d'innovation devient l'architecture. Cette conférence explore\
  \ comment libérer les agents IA de leur \"chef d'orchestre\" pour les faire collaborer\
  \ en chorégraphie. \nLes takeaways : concevoir des systèmes plus résilients, décupler\
  \ leur efficacité par la composition et débloquer des usages proactifs impossibles\
  \ jusqu'alors.\n\n# Longer:\nEt si vos agents IA pouvaient choisir leur mode de\
  \ collaboration ? Cette présentation explore AgentHub, une preuve de concept basée\
  \ sur le protocole Agent2Agent qui libère les agents des contraintes de l'orchestration\
  \ centralisée.\n\n**La vision : Autonomie vs Contrôle Central**\n\nLes systèmes\
  \ d'IA traditionnels imposent un workflow rigide avec un orchestrateur omniscient\
  \ qui dicte chaque étape. AgentHub propose une architecture hybride où les agents\
  \ décident de collaborer \\- en workflow orchestré quand nécessaire, en chorégraphie\
  \ émergente quand  \napproprié.\n\n**Ce que vous découvrirez :**\n\n\\- Protocole\
  \ Agent2Agent : Communication standardisée (Messages, Tasks, Artifacts, Context)\
  \ qui permet aux agents de négocier leur collaboration plutôt que de la subir  \n\
  \\- Architecture Event-Driven Hybride : Un broker \"stupide\" qui route les événements\
  \ sans imposer de logique métier, laissant l'intelligence aux agents eux-mêmes \
  \ \n\\- Autonomie des agents : Démonstration live où des agents spécialisés (chat,\
  \ debug) choisissent leurs tâches, gèrent leurs priorités et collaborent sans coordinateur\
  \ central  \n\\- De la POC à la Production : Observabilité complète (OpenTelemetry,\
  \ Jaeger, Grafana) qui révèle comment ces agents autonomes créent des patterns de\
  \ collaboration émergents\n\n**Pourquoi c'est différent :**\n\nContrairement aux\
  \ orchestrateurs qui imposent \"Publisher → Workflow Engine → Workers\", AgentHub\
  \ permet \"Agents ⇄ Broker ⇄ Agents\" où chaque agent est souverain. Le workflow\
  \ peut émerger de leurs interactions plutôt que d'être imposé d'en haut.\n\n**Technologies**\
  \ : Go, gRPC, Protocol Buffers, Agent2Agent Protocol, OpenTelemetry\n\nUne exploration\
  \ technique de l'intelligence distribuée où le contrôle est décentralisé et l'intelligence\
  \ est aux frontières."
start_time: '16:10'
track: Amphithéâtre René Thery
categories:
- Data Autres
is_extra: false
published: true
---

# Le Pitch:

Alors que les gains de performance des LLMs ralentissent, le véritable levier d'innovation devient l'architecture. Cette conférence explore comment libérer les agents IA de leur "chef d'orchestre" pour les faire collaborer en chorégraphie. 
Les takeaways : concevoir des systèmes plus résilients, décupler leur efficacité par la composition et débloquer des usages proactifs impossibles jusqu'alors.

# Longer:
Et si vos agents IA pouvaient choisir leur mode de collaboration ? Cette présentation explore AgentHub, une preuve de concept basée sur le protocole Agent2Agent qui libère les agents des contraintes de l'orchestration centralisée.

**La vision : Autonomie vs Contrôle Central**

Les systèmes d'IA traditionnels imposent un workflow rigide avec un orchestrateur omniscient qui dicte chaque étape. AgentHub propose une architecture hybride où les agents décident de collaborer \- en workflow orchestré quand nécessaire, en chorégraphie émergente quand  
approprié.

**Ce que vous découvrirez :**

\- Protocole Agent2Agent : Communication standardisée (Messages, Tasks, Artifacts, Context) qui permet aux agents de négocier leur collaboration plutôt que de la subir  
\- Architecture Event-Driven Hybride : Un broker "stupide" qui route les événements sans imposer de logique métier, laissant l'intelligence aux agents eux-mêmes  
\- Autonomie des agents : Démonstration live où des agents spécialisés (chat, debug) choisissent leurs tâches, gèrent leurs priorités et collaborent sans coordinateur central  
\- De la POC à la Production : Observabilité complète (OpenTelemetry, Jaeger, Grafana) qui révèle comment ces agents autonomes créent des patterns de collaboration émergents

**Pourquoi c'est différent :**

Contrairement aux orchestrateurs qui imposent "Publisher → Workflow Engine → Workers", AgentHub permet "Agents ⇄ Broker ⇄ Agents" où chaque agent est souverain. Le workflow peut émerger de leurs interactions plutôt que d'être imposé d'en haut.

**Technologies** : Go, gRPC, Protocol Buffers, Agent2Agent Protocol, OpenTelemetry

Une exploration technique de l'intelligence distribuée où le contrôle est décentralisé et l'intelligence est aux frontières.
