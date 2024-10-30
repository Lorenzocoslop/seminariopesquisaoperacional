<?php
require 'vendor/autoload.php';

use MathPHP\LinearAlgebra\MatrixFactory;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $objective = $_POST['objective'];
    $coefX1 = floatval($_POST['coefX1']);
    $coefX2 = floatval($_POST['coefX2']);

    // Função objetivo
    $objectiveFunction = [$coefX1, $coefX2];

    // Restrições
    $constraints = [];
    $rhs = [];

    $numRestrictions = intval($_POST['numRestrictions']); // Número de restrições
    for ($i = 1; $i <= $numRestrictions; $i++) {
        $coefX1_i = floatval($_POST["coefX1_$i"]); // Coeficiente de X1
        $coefX2_i = floatval($_POST["coefX2_$i"]); // Coeficiente de X2
        $constraints[$i] = [$coefX1_i, $coefX2_i]; // Adiciona os coeficientes

        // Coleta o valor da restrição
        $rhs[$i] = floatval($_POST["value_$i"]); // Valor à direita
    }

    // Converte as restrições para matriz e o valor de b
    try {
        $A = MatrixFactory::create($constraints); // Matriz A
        $b = MatrixFactory::create([array_values($rhs)]); // Vetor b

        // Resolver sistema linear Ax = b
        $solution = $A->inverse()->multiply($b);

        echo "<h3>Resultado da Otimização:</h3>";
        echo "<p>Função objetivo: {$objective} {$coefX1}X1 + {$coefX2}X2</p>";
        echo "<p>Valores ótimos:</p>";
        echo "<p>X1 = " . $solution->get(0, 0) . "</p>";
        echo "<p>X2 = " . $solution->get(1, 0) . "</p>";
        echo "<p>Valor ótimo da função objetivo = " . ($objectiveFunction[0] * $solution->get(0, 0) + $objectiveFunction[1] * $solution->get(1, 0)) . "</p>";
    } catch (Exception $e) {
        echo "<p>Não foi possível encontrar uma solução ótima. Erro: {$e->getMessage()}</p>";
    }
}
?>
