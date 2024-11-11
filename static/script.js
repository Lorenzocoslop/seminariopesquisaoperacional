// Função para gerar campos de restrições com base no número especificado pelo usuário
function generateConstraints() {
    const numRestrictions = parseInt(document.getElementById('num-restrictions').value);
    const container = document.getElementById('constraints-container');
    container.innerHTML = '';

    for (let i = 0; i < numRestrictions; i++) {
        container.innerHTML += `
            <div class="row mb-2">
                <div class="col">
                    <input type="text" class="form-control constraint" placeholder="Coeficientes da restrição (ex: 2, 3)">
                </div>
                <div class="col">
                    <select class="form-select sign">
                        <option value="<=">≤</option>
                        <option value=">=">≥</option>
                        <option value="=">=</option>
                    </select>
                </div>
                <div class="col">
                    <input type="text" class="form-control bound" placeholder="Limite (ex: 12)">
                </div>
            </div>`;
    }
}

// Função para capturar os dados e enviar a solicitação para o servidor
function calculateSimplex() {
    const objectiveType = document.getElementById('objective-type').value;
    
    // Captura e valida os coeficientes da função objetivo
    const objectiveFunction = document.getElementById('objective-function').value
        .split(',')
        .map(item => item.trim())
        .map(Number);

    if (objectiveFunction.some(isNaN)) {
        alert("Por favor, insira coeficientes válidos para a função objetivo.");
        return;
    }

    // Captura as restrições, sinais e limites
    const constraints = Array.from(document.getElementsByClassName('constraint')).map(input => 
        input.value.split(',').map(item => item.trim()).map(Number)
    );

    const signs = Array.from(document.getElementsByClassName('sign')).map(select => select.value);
    const bounds = Array.from(document.getElementsByClassName('bound')).map(input => parseFloat(input.value));

    // Validação das restrições e dos limites
    if (constraints.some(row => row.some(isNaN))) {
        alert("Por favor, insira coeficientes válidos para todas as restrições.");
        return;
    }

    if (bounds.some(isNaN)) {
        alert("Por favor, insira valores numéricos válidos para os limites das restrições.");
        return;
    }

    // Envio da solicitação ao servidor via AJAX
    $.ajax({
        url: '/calculate',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            objective_type: objectiveType,
            objective_function: objectiveFunction,
            constraints: constraints,
            signs: signs,
            bounds: bounds
        }),
        success: function(response) {
            $('#result').html(`
                <h3>Resultado</h3>
                <p>Valor ótimo da função objetivo: ${-response.optimal_value}</p>
                <p>Valores das variáveis: ${response.variables.join(', ')}</p>
                <img src="data:image/png;base64,${response.grafico}" alt="Gráfico da Solução Ótima" class="img-fluid mt-3">
            `);
        },
        error: function(xhr) {
            const errorMessage = xhr.responseJSON?.error || "Solução não encontrada.";
            $('#result').html(`<p class="text-danger">Erro: ${errorMessage}</p>`);
        }
    });
}
