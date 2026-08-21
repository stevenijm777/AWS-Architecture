# 🧮 Algorithms & Mathematical Formulations

## 1. Adaptive Dark Pixel Ratio Thresholding

Let $I_t(x, y)$ be the grayscale intensity of frame $f_t$ at pixel coordinate $(x, y)$, where $x \in [1, W]$ and $y \in [1, H]$.

The dark-pixel ratio $D(f_t)$ is defined as:

$$D(f_t) = \frac{1}{W \times H} \sum_{x=1}^{W} \sum_{y=1}^{H} \mathbb{I}\left(I_t(x, y) < 45\right) \times 100$$

where $\mathbb{I}(\cdot)$ is the indicator function.

To adapt to whiteboard lighting variations across video publication dates, the adaptive threshold $\tau_{dark}$ is calculated relative to the maximum dark pixel ratio $D_{max} = \max_t D(f_t)$:

$$\tau_{dark} = 0.75 \times D_{max}$$

Frames satisfying $D(f_t) \ge \tau_{dark}$ are retained as valid candidate whiteboard keyframes.

---

## 2. Presenter Occlusion Scoring in Central ROI

To detect presenter body blockage in glass whiteboard frames, we extract a central Region of Interest (ROI):

$$\text{ROI}_t = I_t\left(y \in [0.2H, 0.9H], x \in [0.25W, 0.75W]\right)$$

We compute the mean column intensity vector $\mu_c(t)$:

$$\mu_c(t) = \frac{1}{H_{ROI}} \sum_{y \in \text{ROI}} \text{ROI}_t(y, c)$$

Columns with $\mu_c(t) > 55.0$ indicate presenter skin, clothing, or foreground obstruction. The occlusion score $O(f_t)$ is defined as:

$$O(f_t) = \frac{1}{W_{ROI}} \sum_{c=1}^{W_{ROI}} \mathbb{I}\left(\mu_c(t) > 55.0\right) \times 100$$

The frame $f^*$ selected for vision analysis minimizes occlusion among keyframe candidates in the final 10% of the video duration:

$$f^* = \arg\min_{f_t \in \text{Candidates}} O(f_t)$$

---

## 3. Morphological Opening for Icon Isolation

To prevent hand-drawn connecting arrows from joining adjacent AWS icons into single giant contours during morphological closure, a rectangular morphological opening is applied first:

$$I_{clean} = (I_{gray} \circ K_{5\times5}) \bullet K_{15\times15}$$

where $\circ$ denotes morphological opening with a $5\times 5$ rectangular structuring element $K_{5\times5}$, and $\bullet$ denotes closing with $K_{15\times15}$. Opening suppresses thin line artifacts while preserving icon contours.
