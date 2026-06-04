Idea 3: Can LLMs replace the "software engineering" expert in the analysis of cloud architectures? A case study updating the Cloudscape dataset
Problema:
Cloudscape es un dataset de arquitecturas reales en la nube, compilado manualmente por un equipo de la Universidad de Wisconsin-Madison, analizando vídeos de AWS del 2019 al 2023, del playlist de YouTube This is My Architecture. En el 2024 se publicaron muchos vídeos adicionales en ese playlist, los cuales no han sido añadidos al dataset porque verlos manualmente es tedioso.
Solución:
Usar Agentic AI para construir un pipeline de análisis automatizado de vídeos, que permita actualizar el Cloudscape dataset, con intervención mínima de humanos. Se debe primero validar el pipeline con las arquitecturas que ya están en el dataset. ¿La solución propuesta logra replicar el dataset original? Si la respuesta es Sí (o al menos sí, bastante bien aunque no perfecto), en siguiente paso es actualizar los resultados de Santillán y Abad (2025, ver referencia abajo), incluyendo las nuevas arquitecturas.
Resultados esperados:
Proceso de actualización basado en agentic AI.
Validación del proceso (replicación de Cloudscape).
Tip: Considerar usar Fleiss's kappa (Eismann 2021) para validar con múltiples expertos.
Actualización del dataset y de resultados ya publicados.

Referencia(s):
Satija, S., Ye, C., Kosgi, R., Jain, A., Kankaria, R., Chen, Y., ... & Srinivasan, K. (2025). Cloudscape: A study of storage services in modern cloud architectures. In 23rd USENIX Conference on File and Storage Technologies (FAST 25) (pp. 103-121).
Santillan, S., & Abad, C. L. (2025, September). An analysis of hpc and edge architectures in the cloud. In 2025 IEEE International Conference on Cloud Engineering (IC2E) (pp. 259-266). IEEE.
Eismann, S., Scheuner, J., Van Eyk, E., Schwinger, M., Grohmann, J., Herbst, N., ... & Iosup, A. (2021). The state of serverless applications: Collection, characterization, and community consensus. IEEE Transactions on Software Engineering, 48(10), 4152-4166.
