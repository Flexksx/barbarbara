from api_rest_contract.material import CreateMaterialRequest, MaterialResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_session
from api.material import service as material_service

router = APIRouter(prefix="/materials", tags=["materials"])


@router.get("")
def list_materials(session: Session = Depends(get_session)) -> list[MaterialResponse]:
    return material_service.list_all(session)


@router.get("/{material_id}")
def get_material(material_id: str, session: Session = Depends(get_session)) -> MaterialResponse:
    result = material_service.get_by_id(session, material_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Material '{material_id}' not found")
    return result


@router.post("", status_code=201)
def create_material(
    request: CreateMaterialRequest, session: Session = Depends(get_session)
) -> MaterialResponse:
    return material_service.create(session, request)


@router.delete("/{material_id}", status_code=204)
def delete_material(material_id: str, session: Session = Depends(get_session)) -> None:
    deleted = material_service.delete(session, material_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Material '{material_id}' not found")
