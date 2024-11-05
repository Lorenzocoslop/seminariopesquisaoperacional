from flask import Flask, render_template, request, jsonify
from scipy.optimize import linprog

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
            if A[i] is not None:  # Verifica se A[i] não é None
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

    # Retornar resultados
    if resultado.success:
        return jsonify({'optimal_value': resultado.fun, 'variables': resultado.x.tolist()})
    else:
        return jsonify({'error': 'Solução não encontrada'}), 400

if __name__ == '__main__':
    app.run(debug=True)
