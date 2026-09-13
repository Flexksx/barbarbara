from api_rest_contract.constraint import ConstraintResponse, CurdlesBelowResponse, MaxAbvResponse
from api_rest_contract.material import CreateMaterialRequest, MaterialResponse
from api_rest_contract.properties import PropertiesResponse

from api.material.models import MaterialModel


def _parse_constraint(data: dict[str, float | str]) -> ConstraintResponse:
    match data.get("type"):
        case "curdles_below":
            return CurdlesBelowResponse(ph=float(data["ph"]))
        case "max_abv":
            return MaxAbvResponse(abv=float(data["abv"]))
        case other:
            msg = f"Unknown constraint type: {other}"
            raise ValueError(msg)


def request_to_model(request: CreateMaterialRequest) -> MaterialModel:
    return MaterialModel(
        id=request.id,
        ph=request.properties.ph,
        brix=request.properties.brix,
        abv=request.properties.abv,
        density=request.properties.density,
        tags=list(request.tags),
        constraints=[c.model_dump() for c in request.constraints],
    )


def model_to_response(model: MaterialModel) -> MaterialResponse:
    constraints = tuple(_parse_constraint(c) for c in model.constraints)
    return MaterialResponse(
        id=model.id,
        properties=PropertiesResponse(
            ph=model.ph,
            brix=model.brix,
            abv=model.abv,
            density=model.density,
        ),
        tags=frozenset(model.tags),
        constraints=constraints,
    )
