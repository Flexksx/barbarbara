from api_rest_contract.verification import VerifyPlanRequest, VerifyPlanResponse
from fastapi import APIRouter

from api.verification import service as verification_service

router = APIRouter(tags=["verification"])


@router.post("/verify")
def verify_plan(request: VerifyPlanRequest) -> VerifyPlanResponse:
    return verification_service.verify_plan(request)
