from flask import Flask, render_template, request, jsonify
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gerar_grafico(c, A, b, signs, resultado):
    fig, ax = plt.subplots()

    # Limites do gráfico
    x1_vals = range(0, 60)
    ax.set_xlim((0, 60))
    ax.set_ylim((0, 60))

    # Plotar as restrições
    for i, (coef, limite, sign) in enumerate(zip(A, b, signs)):
        if sign == '<=':
            x2 = [(limite - coef[0] * x1) / coef[1] if coef[1] != 0 else float('inf') for x1 in x1_vals]
            ax.plot(x1_vals, x2, label=f'{coef[0]}x1 + {coef[1]}x2 <= {limite}')
        elif sign == '>=':
            x2 = [(limite - coef[0] * x1) / coef[1] if coef[1] != 0 else float('inf') for x1 in x1_vals]
            ax.plot(x1_vals, x2, label=f'{coef[0]}x1 + {coef[1]}x2 >= {limite}', linestyle='--')
        elif sign == '=':
            x2 = [(limite - coef[0] * x1) / coef[1] if coef[1] != 0 else float('inf') for x1 in x1_vals]
            ax.plot(x1_vals, x2, label=f'{coef[0]}x1 + {coef[1]}x2 = {limite}', linestyle=':')

    # Marcar a solução ótima
    if resultado.success:
        x1_opt, x2_opt = resultado.x
        ax.plot(x1_opt, x2_opt, 'ro', label=f'Solução Ótima: X1={x1_opt:.2f}, X2={x2_opt:.2f}, Z={-resultado.fun:.2f}')

    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.legend()
    ax.set_title("Método Gráfico - Região Viável para a Solução Ótima")

    # Converter o gráfico para uma imagem base64 para exibir no HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close(fig)

    return img_base64

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    objective_type = data['objective_type']
    c = data['objective_function']
    A = data['constraints']
    b = data['bounds']
    signs = data['signs']

    # Verificar se A, b e signs estão corretos
    print("A:", A)
    print("b:", b)
    print("signs:", signs)

    # Verificação adicional para garantir que c não contém None
    if c is None or any(coef is None for coef in c):
        return jsonify({'error': 'Coeficientes da função objetivo inválidos ou não fornecidos'}), 400

    # Converter problema de maximização para minimização, se necessário
    if objective_type == 'max':
        c = [-coef for coef in c]

    # Configurar restrições para scipy
    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    for i, sign in enumerate(signs):
        if sign == '<=':
            A_ub.append(A[i])
            b_ub.append(b[i])
        elif sign == '>=':
            if A[i] is not None:
                A_ub.append([-a for a in A[i]])
                b_ub.append(-b[i])
            else:
                return jsonify({'error': f'Restrição A[{i}] é None'}), 400
        elif sign == '=':
            A_eq.append(A[i])
            b_eq.append(b[i])
        else:
            return jsonify({'error': f'Sinal inválido: {sign}'}), 400

    # Resolver o problema
    resultado = linprog(c, A_ub=A_ub or None, b_ub=b_ub or None, A_eq=A_eq or None, b_eq=b_eq or None, method='highs')

    # Verificar se a solução foi encontrada e gerar o gráfico
    if resultado.success:
        grafico_base64 = gerar_grafico(c, A, b, signs, resultado)
        return jsonify({
            'optimal_value': resultado.fun,
            'variables': resultado.x.tolist(),
            'grafico': grafico_base64
        })
    else:
        return jsonify({'error': 'Solução não encontrada'}), 400

if __name__ == '__main__':
    app.run(debug=True)
