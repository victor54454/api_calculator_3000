// Configuration
const API_URL = 'http://172.20.10.3:8000';

/**
 * Vérifie la connexion avec l'API
 * @param {Element} apiStatusElement - Élément HTML qui affiche le statut
 * @param {Element} apiStatusDot - Élément HTML pour l'indicateur visuel
 */
async function checkApiStatus(apiStatusElement, apiStatusDot) {
    try {
        const response = await fetch(API_URL);
        if (response.ok) {
            apiStatusElement.textContent = 'En ligne';
            apiStatusDot.classList.add('online');
            apiStatusDot.classList.remove('offline');
        } else {
            apiStatusElement.textContent = 'Erreur de connexion';
            apiStatusDot.classList.add('offline');
            apiStatusDot.classList.remove('online');
        }
    } catch (error) {
        apiStatusElement.textContent = 'Hors ligne';
        apiStatusDot.classList.add('offline');
        apiStatusDot.classList.remove('online');
        console.error('Erreur de connexion à l\'API:', error);
    }
}

/**
 * Affiche un message d'erreur à l'utilisateur
 * @param {string} message - Message d'erreur à afficher
 */
function showError(message) {
    alert(`Erreur: ${message}`);
}

/**
 * Initialisation des éléments communs
 * @param {Object} config - Configuration spécifique à la page
 */
function initCommon(config) {
    const { 
        apiStatusElement, 
        apiStatusDot, 
        apiUrlContainer 
    } = config;
    
    // Afficher l'URL de l'API
    if (apiUrlContainer) {
        apiUrlContainer.textContent = API_URL;
    }
    
    // Vérifier la connexion avec l'API
    checkApiStatus(apiStatusElement, apiStatusDot);
}

// Fonctions spécifiques à la calculatrice
const calculatorModule = {
    init: function(config) {
        const { 
            operationButtons,
            calculateButton,
            num1Input,
            num2Input,
            resultDisplay,
            operationText,
            historyList
        } = config;
        
        // Initialisation commune
        initCommon(config);
        
        // État local
        let selectedOperation = 'add';
        let calculationHistory = [];
        
        // Configurer les boutons d'opération
        operationButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Supprimer la classe active de tous les boutons
                operationButtons.forEach(btn => btn.classList.remove('active'));
                
                // Ajouter la classe active au bouton cliqué
                this.classList.add('active');
                
                // Mettre à jour l'opération sélectionnée
                selectedOperation = this.getAttribute('data-op');
            });
        });
        
        // Fonction pour effectuer le calcul
        async function performCalculation() {
            // Récupérer les valeurs
            const a = parseFloat(num1Input.value);
            const b = parseFloat(num2Input.value);
            
            // Vérifier que les entrées sont valides
            if (isNaN(a) || isNaN(b)) {
                showError('Veuillez entrer des nombres valides');
                return;
            }
            
            // Vérifier si l'opération est modulo/division et b est 0
            if ((selectedOperation === 'modulo' || selectedOperation === 'divide') && b === 0) {
                showError('Division par zéro impossible');
                return;
            }
            
            // Afficher l'animation de chargement
            resultDisplay.textContent = '...';
            
            try {
                // Envoyer la requête à l'API
                const response = await fetch(`${API_URL}/${selectedOperation}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ a, b })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Erreur de calcul');
                }
                
                const data = await response.json();
                
                // Afficher le résultat avec animation
                resultDisplay.textContent = data.result;
                operationText.textContent = data.operation;
                
                // Ajouter l'effet d'animation
                resultDisplay.classList.add('updated');
                setTimeout(() => {
                    resultDisplay.classList.remove('updated');
                }, 500);
                
                // Ajouter à l'historique
                addToHistory(data.operation, data.result);
                
            } catch (error) {
                showError(error.message);
                console.error('Erreur lors du calcul:', error);
            }
        }
        
        // Ajouter un calcul à l'historique
        function addToHistory(operation, result) {
            // Créer un objet pour le calcul
            const calculation = {
                operation,
                result,
                timestamp: new Date().toLocaleTimeString()
            };
            
            // Ajouter au début de l'historique
            calculationHistory.unshift(calculation);
            
            // Limiter l'historique à 10 entrées
            if (calculationHistory.length > 10) {
                calculationHistory.pop();
            }
            
            // Mettre à jour l'affichage de l'historique
            updateHistoryDisplay();
        }
        
        // Mettre à jour l'affichage de l'historique
        function updateHistoryDisplay() {
            // Vider la liste
            historyList.innerHTML = '';
            
            // Créer un élément pour chaque calcul
            calculationHistory.forEach(calc => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                
                const operation = document.createElement('div');
                operation.className = 'history-operation';
                operation.textContent = calc.operation;
                
                const result = document.createElement('div');
                result.className = 'history-result';
                result.textContent = calc.result;
                
                historyItem.appendChild(operation);
                historyItem.appendChild(result);
                
                historyList.appendChild(historyItem);
            });
            
            // Si l'historique est vide, afficher un message
            if (calculationHistory.length === 0) {
                const emptyMessage = document.createElement('div');
                emptyMessage.className = 'history-item';
                emptyMessage.textContent = 'Aucun calcul dans l\'historique';
                historyList.appendChild(emptyMessage);
            }
        }
        
        // Événements
        calculateButton.addEventListener('click', performCalculation);
        
        // Permettre l'utilisation de la touche "Entrée" pour calculer
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                performCalculation();
            }
        });
    }
};

// Fonctions spécifiques au graphique
const graphModule = {
    init: function(config) {
        const { 
            expressionInput,
            xMinInput,
            xMaxInput,
            pointsInput,
            plotBtn,
            graphCanvas,
            graphTitle,
            functionCards
        } = config;
        
        // Initialisation commune
        initCommon(config);
        
        // Variable pour le graphique
        let chartInstance = null;
        
        // Ajouter des écouteurs pour les boutons d'exemple
        functionCards.forEach(card => {
            card.addEventListener('click', function() {
                expressionInput.value = this.getAttribute('data-expr');
                plotGraph();
            });
        });
        
        // Tracer le graphique
        async function plotGraph() {
            const expression = expressionInput.value;
            const xMin = parseFloat(xMinInput.value);
            const xMax = parseFloat(xMaxInput.value);
            const points = parseInt(pointsInput.value);
            
            // Vérifier que les entrées sont valides
            if (!expression || isNaN(xMin) || isNaN(xMax) || isNaN(points)) {
                showError('Veuillez entrer des valeurs valides');
                return;
            }
            
            // Vérifier que xMin < xMax
            if (xMin >= xMax) {
                showError('X Minimum doit être inférieur à X Maximum');
                return;
            }
            
            try {
                // Désactiver le bouton pendant le chargement
                plotBtn.disabled = true;
                plotBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Chargement...';
                
                // Envoyer la requête à l'API
                const response = await fetch(`${API_URL}/graph`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        expression,
                        x_min: xMin,
                        x_max: xMax,
                        points
                    })
                });
                
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || 'Erreur lors de la génération du graphique');
                }
                
                const data = await response.json();
                
                // Vérifier s'il y a une erreur
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Mettre à jour le titre du graphique
                graphTitle.textContent = `Graphique de f(x) = ${data.expression}`;
                
                // Créer les données pour le graphique
                const chartData = {
                    labels: data.x_values,
                    datasets: [{
                        label: data.expression,
                        data: data.x_values.map((x, i) => ({ x, y: data.y_values[i] })),
                        borderColor: '#4361ee',
                        backgroundColor: 'rgba(67, 97, 238, 0.1)',
                        pointRadius: 0,
                        borderWidth: 2,
                        tension: 0.1
                    }]
                };
                
                // Détruire le graphique existant s'il y en a un
                if (chartInstance) {
                    chartInstance.destroy();
                }
                
                // Créer le nouveau graphique
                chartInstance = new Chart(graphCanvas, {
                    type: 'line',
                    data: chartData,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                type: 'linear',
                                position: 'center',
                                grid: {
                                    color: 'rgba(0, 0, 0, 0.1)'
                                }
                            },
                            y: {
                                type: 'linear',
                                position: 'center',
                                grid: {
                                    color: 'rgba(0, 0, 0, 0.1)'
                                }
                            }
                        },
                        plugins: {
                            title: {
                                display: false
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return `f(${context.parsed.x.toFixed(2)}) = ${context.parsed.y.toFixed(2)}`;
                                    }
                                }
                            }
                        }
                    }
                });
                
            } catch (error) {
                showError(error.message);
                console.error('Erreur lors du tracé du graphique:', error);
            } finally {
                // Réactiver le bouton
                plotBtn.disabled = false;
                plotBtn.innerHTML = '<i class="fas fa-chart-line"></i> Tracer le graphique';
            }
        }
        
        // Ajouter l'écouteur d'événement pour le bouton de tracé
        plotBtn.addEventListener('click', plotGraph);
        
        // Tracer le graphique initial
        plotGraph();
    }
};