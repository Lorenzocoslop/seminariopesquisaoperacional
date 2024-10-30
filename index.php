<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora Simplex</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <div class="container mt-5">
        <h1 class="text-center">Calculadora Simplex</h1>
        <form id="simplexForm" method="POST" action="simplex_calculator.php">
            <div class="mb-3">
                <label for="objective" class="form-label">Qual é o objetivo da função?</label>
                <select id="objective" name="objective" class="form-select">
                    <option value="max">Maximizar</option>
                    <option value="min">Minimizar</option>
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Função Objetivo:</label>
                <div class="input-group">
                    <input type="number" name="coefX1" class="form-control" placeholder="Coeficiente de X1" required>
                    <span class="input-group-text">X1 +</span>
                    <input type="number" name="coefX2" class="form-control" placeholder="Coeficiente de X2" required>
                    <span class="input-group-text">X2</span>
                </div>
            </div>
            <div class="mb-3">
                <label for="numRestrictions" class="form-label">Número de Restrições:</label>
                <input type="number" id="numRestrictions" class="form-control" min="1" max="10" placeholder="Ex: 3" required>
            </div>
            <div id="restrictionsContainer" class="mt-3">
                <!-- Restrições dinâmicas serão adicionadas aqui -->
            </div>
            <button type="button" id="generateRestrictions" class="btn btn-primary mt-3">Gerar Restrições</button>
            <button type="submit" class="btn btn-success mt-3" id="calculateButton" style="display: none;">Calcular</button>
        </form>
        <div id="result" class="mt-4"></div>
    </div>

    <script>
        // Função para gerar as restrições dinamicamente
        $('#generateRestrictions').click(function() {
            const numRestrictions = parseInt($('#numRestrictions').val());
            if (isNaN(numRestrictions) || numRestrictions < 1) {
                alert('Por favor, insira um número válido de restrições.');
                return;
            }
            $('#restrictionsContainer').html(''); // Limpar restrições anteriores

            for (let i = 1; i <= numRestrictions; i++) {
                $('#restrictionsContainer').append(`
                    <div class="mb-3">
                        <div class="input-group">
                            <input type="number" name="coefX1_${i}" class="form-control" placeholder="Coeficiente X1" required>
                            <span class="input-group-text">X1 +</span>
                            <input type="number" name="coefX2_${i}" class="form-control" placeholder="Coeficiente X2" required>
                            <span class="input-group-text">X2</span>
                            <select name="constraint_${i}" class="form-select">
                                <option value="≤">≤</option>
                                <option value="≥">≥</option>
                                <option value="=">=</option>
                            </select>
                            <input type="number" name="value_${i}" class="form-control" placeholder="Valor" required>
                        </div>
                    </div>
                `);
            }
            $('#calculateButton').show(); // Mostrar o botão de calcular após gerar restrições
        });

        // Envio do formulário via AJAX
        $('#simplexForm').submit(function(event) {
            event.preventDefault();
            const formData = $(this).serialize();

            $.ajax({
                url: 'simplex_calculator.php', // Nome do arquivo PHP que processará o cálculo
                type: 'POST',
                data: formData,
                success: function(response) {
                    $('#result').html(response); // Exibir o resultado
                },
                error: function() {
                    $('#result').html('<div class="alert alert-danger">Ocorreu um erro ao calcular.</div>');
                }
            });
        });
    </script>
</body>
</html>
