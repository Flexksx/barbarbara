from api_rest_contract.equipment import CreateEquipmentRequest, EquipmentResponse
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.database import get_session
from api.equipment import service as equipment_service

router = APIRouter(prefix="/equipment", tags=["equipment"])


@router.get("")
def list_equipment(session: Session = Depends(get_session)) -> list[EquipmentResponse]:
    return equipment_service.list_all(session)


@router.get("/{equipment_id}")
def get_equipment(equipment_id: str, session: Session = Depends(get_session)) -> EquipmentResponse:
    result = equipment_service.get_by_id(session, equipment_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Equipment '{equipment_id}' not found")
    return result


@router.post("", status_code=201)
def create_equipment(
    request: CreateEquipmentRequest, session: Session = Depends(get_session)
) -> EquipmentResponse:
    return equipment_service.create(session, request)


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: str, session: Session = Depends(get_session)) -> None:
    deleted = equipment_service.delete(session, equipment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Equipment '{equipment_id}' not found")
