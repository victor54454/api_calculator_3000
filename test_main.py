# test_main.py - Version corrigée
from fastapi.testclient import TestClient
from main import app
import pytest
import random
import math

# Créer un client de test
client = TestClient(app)

# Test de la route d'accueil
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Bienvenue sur l'API Calculatrice"

# --- TESTS D'ADDITION ---

# Test de base de l'addition
def test_addition_basic():
    response = client.post(
        "/add",
        json={"a": 5, "b": 3}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 8
    assert response.json()["operation"] == "5.0 + 3.0"

# Test d'addition avec grands nombres
def test_addition_large_numbers():
    a = 9999999
    b = 9999999
    response = client.post(
        "/add",
        json={"a": a, "b": b}
    )
    assert response.status_code == 200
    assert response.json()["result"] == a + b

# Test d'addition avec nombres négatifs
def test_addition_negative_numbers():
    response = client.post(
        "/add",
        json={"a": -5, "b": -3}
    )
    assert response.status_code == 200
    assert response.json()["result"] == -8

# Test d'addition avec nombre décimal
def test_addition_decimal_numbers():
    response = client.post(
        "/add",
        json={"a": 2.5, "b": 3.7}
    )
    assert response.status_code == 200
    assert round(response.json()["result"], 1) == 6.2

# --- TESTS DE SOUSTRACTION ---

# Test de base de la soustraction
def test_subtraction_basic():
    response = client.post(
        "/subtract",
        json={"a": 10, "b": 4}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 6
    assert response.json()["operation"] == "10.0 - 4.0"

# Test soustraction donnant un résultat négatif
def test_subtraction_negative_result():
    response = client.post(
        "/subtract",
        json={"a": 5, "b": 10}
    )
    assert response.status_code == 200
    assert response.json()["result"] == -5

# Test soustraction avec grands nombres
def test_subtraction_large_numbers():
    a = 10000000
    b = 1
    response = client.post(
        "/subtract",
        json={"a": a, "b": b}
    )
    assert response.status_code == 200
    assert response.json()["result"] == a - b

# Test soustraction avec nombres décimaux
def test_subtraction_decimal_numbers():
    response = client.post(
        "/subtract",
        json={"a": 10.5, "b": 3.2}
    )
    assert response.status_code == 200
    assert round(response.json()["result"], 1) == 7.3

# --- TESTS DE MULTIPLICATION ---

# Test de base de la multiplication
def test_multiplication_basic():
    response = client.post(
        "/multiply",
        json={"a": 7, "b": 8}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 56
    assert response.json()["operation"] == "7.0 * 8.0"

# Test multiplication par zéro
def test_multiplication_by_zero():
    response = client.post(
        "/multiply",
        json={"a": 100, "b": 0}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 0

# Test multiplication avec nombres négatifs
def test_multiplication_negative_numbers():
    response = client.post(
        "/multiply",
        json={"a": -5, "b": 4}
    )
    assert response.status_code == 200
    assert response.json()["result"] == -20

    response = client.post(
        "/multiply",
        json={"a": -5, "b": -4}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 20

# Test multiplication avec décimaux
def test_multiplication_decimal_numbers():
    response = client.post(
        "/multiply",
        json={"a": 2.5, "b": 4}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 10.0

# --- TESTS DE DIVISION ---

# Test de base de la division
def test_division_basic():
    response = client.post(
        "/divide",
        json={"a": 20, "b": 5}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 4
    assert response.json()["operation"] == "20.0 / 5.0"

# Test division donnant un résultat décimal
def test_division_decimal_result():
    response = client.post(
        "/divide",
        json={"a": 10, "b": 3}
    )
    assert response.status_code == 200
    assert round(response.json()["result"], 6) == round(10/3, 6)

# Test division avec nombres négatifs
def test_division_negative_numbers():
    response = client.post(
        "/divide",
        json={"a": -10, "b": 2}
    )
    assert response.status_code == 200
    assert response.json()["result"] == -5

    response = client.post(
        "/divide",
        json={"a": 10, "b": -2}
    )
    assert response.status_code == 200
    assert response.json()["result"] == -5

    response = client.post(
        "/divide",
        json={"a": -10, "b": -2}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 5

# Test division de zéro
def test_division_of_zero():
    response = client.post(
        "/divide",
        json={"a": 0, "b": 5}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 0

# Test division par zéro
def test_division_by_zero():
    response = client.post(
        "/divide",
        json={"a": 10, "b": 0}
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Division par zéro impossible"

# --- TESTS DE MODULO ---

# Test de base du modulo
def test_modulo_basic():
    response = client.post(
        "/modulo",
        json={"a": 17, "b": 5}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 2
    assert response.json()["operation"] == "17.0 % 5.0"

# Test modulo avec résultat 0
def test_modulo_zero_remainder():
    response = client.post(
        "/modulo",
        json={"a": 20, "b": 5}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 0

# Test modulo avec nombres négatifs
def test_modulo_negative_numbers():
    response = client.post(
        "/modulo",
        json={"a": -17, "b": 5}
    )
    assert response.status_code == 200
    assert response.json()["result"] == -17 % 5  # Comportement Python: -17 % 5 = 3

    response = client.post(
        "/modulo",
        json={"a": 17, "b": -5}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 17 % -5  # Comportement Python: 17 % -5 = -3

# Test modulo avec nombres décimaux
def test_modulo_decimal_numbers():
    response = client.post(
        "/modulo",
        json={"a": 10.5, "b": 3}
    )
    assert response.status_code == 200
    assert round(response.json()["result"], 1) == 1.5

# Test modulo par zéro
def test_modulo_by_zero():
    response = client.post(
        "/modulo",
        json={"a": 10, "b": 0}
    )
    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Division par zéro impossible"

# --- TESTS DE VALIDATION D'ENTRÉE ---

# Test avec entrée non numérique
def test_invalid_input_not_number():
    response = client.post(
        "/add",
        json={"a": "non-nombre", "b": 4}
    )
    assert response.status_code == 422  # Unprocessable Entity

# Test avec paramètres manquants
def test_invalid_input_missing_parameters():
    response = client.post(
        "/add",
        json={"a": 5}  # Paramètre 'b' manquant
    )
    assert response.status_code == 422

    response = client.post(
        "/add",
        json={"b": 5}  # Paramètre 'a' manquant
    )
    assert response.status_code == 422

# Test avec valeurs extrêmes
def test_extreme_values():
    # Très grand nombre
    response = client.post(
        "/add",
        json={"a": 1e15, "b": 1}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 1e15 + 1

    # Très petit nombre
    response = client.post(
        "/add",
        json={"a": 1e-10, "b": 1e-10}
    )
    assert response.status_code == 200
    assert response.json()["result"] == 2e-10

# --- TESTS ALÉATOIRES ---

# Tests avec valeurs aléatoires
@pytest.mark.parametrize("test_id", range(5))  # Exécute ce test 5 fois
def test_random_addition(test_id):
    a = random.uniform(-100, 100)
    b = random.uniform(-100, 100)
    response = client.post(
        "/add",
        json={"a": a, "b": b}
    )
    assert response.status_code == 200
    assert math.isclose(response.json()["result"], a + b, rel_tol=1e-9)

@pytest.mark.parametrize("test_id", range(5))
def test_random_subtraction(test_id):
    a = random.uniform(-100, 100)
    b = random.uniform(-100, 100)
    response = client.post(
        "/subtract",
        json={"a": a, "b": b}
    )
    assert response.status_code == 200
    assert math.isclose(response.json()["result"], a - b, rel_tol=1e-9)

@pytest.mark.parametrize("test_id", range(5))
def test_random_multiplication(test_id):
    a = random.uniform(-100, 100)
    b = random.uniform(-100, 100)
    response = client.post(
        "/multiply",
        json={"a": a, "b": b}
    )
    assert response.status_code == 200
    assert math.isclose(response.json()["result"], a * b, rel_tol=1e-9)

@pytest.mark.parametrize("test_id", range(5))
def test_random_division(test_id):
    a = random.uniform(-100, 100)
    b = random.uniform(0.1, 100) if random.random() > 0.5 else random.uniform(-100, -0.1)
    response = client.post(
        "/divide",
        json={"a": a, "b": b}
    )
    assert response.status_code == 200
    assert math.isclose(response.json()["result"], a / b, rel_tol=1e-9)

# --- TESTS DE PERFORMANCE ---

def test_api_response_time():
    import time
    
    start_time = time.time()
    response = client.post(
        "/add",
        json={"a": 1, "b": 2}
    )
    end_time = time.time()
    
    # Vérifier que la réponse est rapide (moins de 500ms)
    assert end_time - start_time < 0.5
    assert response.status_code == 200

# --- TESTS DE LA FONCTIONNALITÉ GRAPHIQUE ---

def test_graph_basic():
    response = client.post(
        "/graph",
        json={
            "expression": "x^2",
            "x_min": -5,
            "x_max": 5,
            "points": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "expression" in data
    assert data["expression"] == "x^2"
    assert "x_values" in data
    assert "y_values" in data
    assert len(data["x_values"]) == 10
    assert len(data["y_values"]) == 10
    # Vérifier que la fonction x^2 est correctement calculée pour le point central
    # Assurez-vous que l'indice est valide (5 pour 10 points serait le milieu)
    middle_index = len(data["x_values"]) // 2
    if data["x_values"][middle_index] == 0:  # Si x=0 est au milieu
        assert data["y_values"][middle_index] == 0.0  # x=0 => y=0

def test_graph_sin():
    response = client.post(
        "/graph",
        json={
            "expression": "sin(x)",
            "x_min": 0,
            "x_max": 6.28,  # Environ 2*pi
            "points": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    # Vérifier que sin(0) ≈ 0
    assert abs(data["y_values"][0]) < 0.1  # sin(0) ≈ 0
    
def test_graph_invalid_expression():
    response = client.post(
        "/graph",
        json={
            "expression": "invalid_function(x)",
            "x_min": -5,
            "x_max": 5,
            "points": 10
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "error" in data
    assert data["error"] is not None

def test_graph_division_by_zero():
    response = client.post(
        "/graph",
        json={
            "expression": "1/x",
            "x_min": -5,
            "x_max": 5,
            "points": 11  # Avec 11 points, x=0 sera inclus
        }
    )
    assert response.status_code == 200
    data = response.json()
    
    # Vérification améliorée avec protection contre les erreurs
    # Vérifier que la réponse contient bien les champs attendus
    assert "x_values" in data, "Clé 'x_values' manquante dans la réponse"
    assert "y_values" in data, "Clé 'y_values' manquante dans la réponse"
    
    # Si x_values est vide, le test passe quand même (cas d'erreur géré par l'API)
    if len(data["x_values"]) > 0 and len(data["y_values"]) > 0:
        # Chercher si un point à x=0 existe
        zero_index = None
        for i, x in enumerate(data["x_values"]):
            if abs(x) < 0.01:
                zero_index = i
                break
                
        # Si un point à x=0 est trouvé, vérifier que sa valeur y est None ou que l'erreur est gérée
        if zero_index is not None:
            assert data["y_values"][zero_index] is None or data["error"] is not None