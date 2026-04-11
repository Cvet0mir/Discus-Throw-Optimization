import matplotlib.pyplot as plt

def render_latex_to_image(latex, filename):
    fig = plt.figure()
    fig.text(0.1, 0.5, f"${latex}$", fontsize=20)

    plt.axis("off")
    plt.savefig(filename, bbox_inches="tight", dpi=200)
    plt.close()

render_latex_to_image(
    r"y = - \frac{g x^2}{2 v^2 \cos^2(\theta)} + x \tan(\theta) + h",
    "formula.png"
)