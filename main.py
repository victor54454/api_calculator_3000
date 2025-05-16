# main.py corrigé avec gestion améliorée des expressions invalides
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import numpy as np

app = FastAPI(title="API Calculatrice")

# Configuration CORS pour permettre au frontend de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise tous les domaines en développement
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes
    allow_headers=["*"],  # Autorise tous les headers
)

# Modèle de données pour les opérations
class Operation(BaseModel):
    a: float
    b: float

# Modèle pour la réponse
class Result(BaseModel):
    operation: str
    result: float

# Modèle pour les requêtes de graphique
class GraphRequest(BaseModel):
    expression: str
    x_min: float = -10
    x_max: float = 10
    points: int = 100

# Modèle pour les réponses graphiques
class GraphResponse(BaseModel):
    expression: str
    x_values: List[float]
    y_values: List[Optional[float]]
    error: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Calculatrice"}

@app.post("/add", response_model=Result)
def addition(operation: Operation):
    result = operation.a + operation.b
    return Result(operation=f"{operation.a} + {operation.b}", result=result)

@app.post("/subtract", response_model=Result)
def subtraction(operation: Operation):
    result = operation.a - operation.b
    return Result(operation=f"{operation.a} - {operation.b}", result=result)

@app.post("/multiply", response_model=Result)
def multiplication(operation: Operation):
    result = operation.a * operation.b
    return Result(operation=f"{operation.a} * {operation.b}", result=result)

@app.post("/modulo", response_model=Result)
def modulo(operation: Operation):
    if operation.b == 0:
        raise HTTPException(status_code=400, detail="Division par zéro impossible")
    result = operation.a % operation.b
    return Result(operation=f"{operation.a} % {operation.b}", result=result)

@app.post("/divide", response_model=Result)
def division(operation: Operation):
    if operation.b == 0:
        raise HTTPException(status_code=400, detail="Division par zéro impossible")
    result = operation.a / operation.b
    return Result(operation=f"{operation.a} / {operation.b}", result=result)

# Fonction pour évaluer une expression mathématique
def evaluate_expression(expression: str, x: float) -> Optional[float]:
    # Remplacements pour rendre l'expression compatible avec Python
    expression = expression.replace("^", "**")  # Remplacer ^ par **
    try:
        # Gestion spéciale de la division par zéro
        if abs(x) < 1e-10 and ('/' in expression or '**-' in expression):
            # Vérifier si x est proche de zéro et s'il y a une division
            return None
            
        # Évaluer l'expression avec les fonctions mathématiques disponibles
        return eval(expression, {
            "x": x, 
            "sin": np.sin, 
            "cos": np.cos, 
            "tan": np.tan, 
            "exp": np.exp, 
            "log": np.log, 
            "sqrt": np.sqrt, 
            "pi": np.pi, 
            "e": np.e
        })
    except Exception as e:
        # En cas d'erreur (comme division par zéro), retourner None
        print(f"Erreur pour x={x}: {str(e)}")
        return None

@app.post("/graph", response_model=GraphResponse)
def generate_graph(request: GraphRequest):
    try:
        # Vérifier d'abord si l'expression est valide en l'évaluant pour une valeur simple
        try:
            # Essayer avec une valeur loin de zéro pour éviter les erreurs de division par zéro
            test_value = 1.0
            test_expression = request.expression.replace("^", "**")
            eval(test_expression, {
                "x": test_value, 
                "sin": np.sin, 
                "cos": np.cos, 
                "tan": np.tan, 
                "exp": np.exp, 
                "log": np.log, 
                "sqrt": np.sqrt, 
                "pi": np.pi, 
                "e": np.e
            })
        except Exception as e:
            # Si l'expression est invalide, retourner une erreur claire
            return GraphResponse(
                expression=request.expression,
                x_values=[],
                y_values=[],
                error=f"Expression invalide: {str(e)}"
            )
        
        # Générer les valeurs x
        x_values = np.linspace(request.x_min, request.x_max, request.points).tolist()
        
        # Calculer les valeurs y
        y_values = []
        all_none = True  # Pour vérifier si tous les points sont None
        
        for x in x_values:
            try:
                y = evaluate_expression(request.expression, x)
                y_values.append(y)
                if y is not None:
                    all_none = False
            except Exception as e:
                y_values.append(None)
                
        # Si tous les points sont None, c'est probablement une expression invalide
        if all_none:
            return GraphResponse(
                expression=request.expression,
                x_values=x_values,
                y_values=y_values,
                error="Impossible de calculer des valeurs valides pour cette expression"
            )
                
        return GraphResponse(
            expression=request.expression,
            x_values=x_values,
            y_values=y_values
        )
    except Exception as e:
        # En cas d'erreur globale, retourner une réponse avec message d'erreur
        return GraphResponse(
            expression=request.expression,
            x_values=[],
            y_values=[],
            error=f"Erreur: {str(e)}"
        )

# Pour lancer l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)