#!/usr/bin/env python3
"""
effect_size.py — Tamaño de efecto no paramétrico Â₁₂ de Vargha y Delaney.

Por qué esta medida y no otra
-----------------------------
Arcuri y Briand, en la guía canónica para evaluar algoritmos aleatorizados en
ingeniería de software, recomiendan **Â₁₂ para resultados de escala de intervalo** y
desaconsejan explícitamente la familia de la *d* de Cohen, porque asume normalidad y
la desviación estándar se vuelve poco confiable ante distribuciones asimétricas. Las
distribuciones de F1 por video de este proyecto son marcadamente asimétricas —hay una
masa de videos en 100 y una cola larga hacia 0—, así que la advertencia aplica.

Los mismos autores señalan que un p-valor sin tamaño de efecto no dice nada útil: con
n suficiente casi cualquier diferencia sale significativa, aunque sea irrelevante. Y a
la inversa, la forma de distinguir «no hay efecto» de «no hay potencia» ante un
resultado no significativo es mirar el **intervalo de confianza del tamaño de efecto**:
un IC angosto centrado en 0.5 es evidencia de ausencia de efecto; uno ancho es
simplemente falta de potencia. Esa distinción es la que sostiene RQ2, donde la
afirmación es «ninguna diferencia es detectable» y no «todas las variantes son iguales».

Qué mide Â₁₂
------------
La probabilidad de que una observación tomada al azar de A supere a una tomada al azar
de B, contando los empates como medio:

    Â₁₂(A, B) = P(A > B) + 0.5 · P(A = B)

0.5 es ausencia de efecto. Los umbrales de magnitud de Vargha y Delaney son 0.56
(pequeño), 0.64 (mediano) y 0.71 (grande), simétricos por debajo de 0.5.

Sobre el intervalo de confianza
-------------------------------
`a12_ic` remuestrea **videos completos**, no observaciones sueltas. Los diseños de este
proyecto son pareados —la misma arquitectura evaluada por dos condiciones—, y
remuestrear cada brazo por separado rompería ese apareamiento e inflaría el intervalo.
Â₁₂ en sí es una medida de superioridad estocástica que ignora el apareamiento; el IC
sí lo respeta.

Uso
---
    from scripts.utils.effect_size import a12, a12_ic, magnitud
    a, (lo, hi) = a12_ic(xs, ys)
    print(f"Â₁₂ = {a:.3f} [{lo:.3f}, {hi:.3f}] — {magnitud(a)}")
"""
from __future__ import annotations

import numpy as np

# Umbrales de Vargha y Delaney, tal como los reproduce Arcuri y Briand.
UMBRALES = ((0.71, "grande"), (0.64, "mediano"), (0.56, "pequeño"))


def a12(x, y) -> float:
    """Â₁₂ = P(x > y) + 0.5·P(x = y), vía rangos (equivale a comparar todos los pares)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    m, n = len(x), len(y)
    if m == 0 or n == 0:
        return float("nan")
    # Rangos promediados sobre la muestra combinada; la forma cerrada evita el O(m·n).
    juntos = np.concatenate([x, y])
    orden = juntos.argsort(kind="mergesort")
    rangos = np.empty(len(juntos), float)
    rangos[orden] = np.arange(1, len(juntos) + 1)
    # promediar los rangos de los empates, que es lo que introduce el 0.5·P(x=y)
    vals, inicio, cuenta = np.unique(juntos, return_index=True, return_counts=True)
    for i, c in zip(inicio, cuenta):
        if c > 1:
            iguales = juntos == juntos[i]
            rangos[iguales] = rangos[iguales].mean()
    r1 = rangos[:m].sum()
    return (r1 / m - (m + 1) / 2) / n


def magnitud(a: float) -> str:
    """Etiqueta de Vargha y Delaney. Simétrica: 0.29 es tan grande como 0.71."""
    if not np.isfinite(a):
        return "—"
    d = abs(a - 0.5) + 0.5
    for umbral, nombre in UMBRALES:
        if d >= umbral:
            return nombre
    return "insignificante"


def a12_ic(x, y, n_boot: int = 10_000, alfa: float = 0.05,
           pareado: bool = True, seed: int = 0) -> tuple[float, tuple[float, float]]:
    """Â₁₂ con intervalo de confianza percentil por bootstrap.

    `pareado=True` remuestrea índices de video comunes a las dos condiciones, de modo
    que cada réplica conserva el apareamiento del diseño. Requiere len(x) == len(y) y
    que la posición i sea el mismo video en las dos. Con `pareado=False` remuestrea
    cada brazo por separado, para comparaciones genuinamente no pareadas.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    punto = a12(x, y)
    if not np.isfinite(punto):
        return punto, (float("nan"), float("nan"))
    if pareado and len(x) != len(y):
        raise ValueError(f"pareado=True exige el mismo n: {len(x)} vs {len(y)}")

    rng = np.random.default_rng(seed)
    reps = np.empty(n_boot)
    for b in range(n_boot):
        if pareado:
            i = rng.integers(0, len(x), len(x))
            reps[b] = a12(x[i], y[i])
        else:
            reps[b] = a12(x[rng.integers(0, len(x), len(x))],
                          y[rng.integers(0, len(y), len(y))])
    lo, hi = np.percentile(reps, [100 * alfa / 2, 100 * (1 - alfa / 2)])
    return punto, (float(lo), float(hi))


def resumen(a: float, ic: tuple[float, float]) -> str:
    """'0.512 [0.451, 0.573] · insignificante · IC incluye 0.5'."""
    incluye = ic[0] <= 0.5 <= ic[1]
    return (f"{a:.3f} [{ic[0]:.3f}, {ic[1]:.3f}] · {magnitud(a)} · "
            f"IC {'incluye' if incluye else 'excluye'} 0.5")


def _autotest() -> None:
    """Comprueba la implementación contra casos donde el valor se conoce a mano."""
    # 1. Distribuciones idénticas -> 0.5 exacto
    assert abs(a12([1, 2, 3], [1, 2, 3]) - 0.5) < 1e-12
    # 2. Dominancia total -> 1.0 y 0.0
    assert a12([4, 5, 6], [1, 2, 3]) == 1.0
    assert a12([1, 2, 3], [4, 5, 6]) == 0.0
    # 3. Todos empatados -> 0.5 (los empates cuentan medio)
    assert abs(a12([2, 2, 2], [2, 2, 2]) - 0.5) < 1e-12
    # 4. Caso a mano: x=[1,3], y=[2,2]. Pares: 1v2 pierde, 1v2 pierde, 3v2 gana,
    #    3v2 gana -> 2/4 = 0.5
    assert abs(a12([1, 3], [2, 2]) - 0.5) < 1e-12
    # 5. Contra fuerza bruta sobre datos aleatorios con empates
    rng = np.random.default_rng(7)
    for _ in range(200):
        x = rng.integers(0, 6, rng.integers(2, 15)).astype(float)
        y = rng.integers(0, 6, rng.integers(2, 15)).astype(float)
        bruto = np.mean([(1.0 if a > b else 0.5 if a == b else 0.0) for a in x for b in y])
        assert abs(a12(x, y) - bruto) < 1e-9, (x, y, a12(x, y), bruto)
    # 6. Magnitudes en los umbrales publicados
    assert magnitud(0.5) == "insignificante"
    assert magnitud(0.60) == "pequeño" and magnitud(0.40) == "pequeño"
    assert magnitud(0.66) == "mediano"
    assert magnitud(0.80) == "grande" and magnitud(0.20) == "grande"
    # 7. El IC de dos muestras idénticas tiene que rodear a 0.5
    a, (lo, hi) = a12_ic(rng.normal(size=60), rng.normal(size=60), n_boot=2000)
    assert lo <= 0.5 <= hi
    print("effect_size: 7/7 comprobaciones OK")


if __name__ == "__main__":
    _autotest()
