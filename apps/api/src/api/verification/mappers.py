from api_core.action import Action as CoreAction
from api_core.action import Add, Pour, Strain
from api_core.constraint import Constraint as CoreConstraint
from api_core.constraint import CurdlesBelow, MaxAbv
from api_core.equipment import Equipment as CoreEquipment
from api_core.material import Material as CoreMaterial
from api_core.mixture import Mixture as CoreMixture
from api_core.properties import Properties as CoreProperties
from api_core.verification import StepViolation as CoreStepViolation
from api_core.verification import VerificationResult
from api_rest_contract.action import (
    ActionResponse,
    AddActionResponse,
    PourActionResponse,
    StrainActionResponse,
)
from api_rest_contract.constraint import ConstraintResponse, CurdlesBelowResponse, MaxAbvResponse
from api_rest_contract.equipment import EquipmentResponse
from api_rest_contract.material import MaterialResponse
from api_rest_contract.mixture import MixtureComponentResponse, MixtureResponse
from api_rest_contract.properties import PropertiesResponse
from api_rest_contract.verification import StepViolationResponse, VerifyPlanResponse


def properties_to_core(source: PropertiesResponse) -> CoreProperties:
    return CoreProperties(ph=source.ph, brix=source.brix, abv=source.abv, density=source.density)


def constraint_to_core(source: ConstraintResponse) -> CoreConstraint:
    match source:
        case CurdlesBelowResponse(ph=ph):
            return CurdlesBelow(ph=ph)
        case MaxAbvResponse(abv=abv):
            return MaxAbv(abv=abv)


def material_to_core(source: MaterialResponse) -> CoreMaterial:
    return CoreMaterial(
        id=source.id,
        properties=properties_to_core(source.properties),
        tags=source.tags,
        constraints=tuple(constraint_to_core(c) for c in source.constraints),
    )


def equipment_to_core(source: EquipmentResponse) -> CoreEquipment:
    return CoreEquipment(
        id=source.id,
        capacity_ml=source.capacity_ml,
        accepts_tags=source.accepts_tags,
    )


def action_to_core(source: ActionResponse) -> CoreAction:
    match source:
        case AddActionResponse():
            return Add(
                material_id=source.material_id,
                volume_ml=source.volume_ml,
                equipment_id=source.equipment_id,
            )
        case PourActionResponse():
            return Pour(
                from_equipment_id=source.from_equipment_id,
                to_equipment_id=source.to_equipment_id,
            )
        case StrainActionResponse():
            return Strain(
                from_equipment_id=source.from_equipment_id,
                to_equipment_id=source.to_equipment_id,
                remove_tags=source.remove_tags,
            )


def properties_to_response(source: CoreProperties) -> PropertiesResponse:
    return PropertiesResponse(
        ph=source.ph, brix=source.brix, abv=source.abv, density=source.density
    )


def mixture_to_response(source: CoreMixture) -> MixtureResponse:
    components = tuple(
        MixtureComponentResponse(material_id=c.material.id, volume_ml=c.volume_ml)
        for c in source.components
    )
    props = source.properties
    return MixtureResponse(
        components=components,
        total_volume_ml=source.total_volume_ml,
        properties=properties_to_response(props) if props else None,
    )


def equipment_to_response(source: CoreEquipment) -> EquipmentResponse:
    return EquipmentResponse(
        id=source.id,
        capacity_ml=source.capacity_ml,
        accepts_tags=source.accepts_tags,
        contents=mixture_to_response(source.contents) if source.contents.components else None,
    )


def violation_to_response(source: CoreStepViolation) -> StepViolationResponse:
    return StepViolationResponse(step=source.step, kind=source.kind, message=source.message)


def result_to_response(source: VerificationResult) -> VerifyPlanResponse:
    return VerifyPlanResponse(
        valid=source.valid,
        violations=[violation_to_response(v) for v in source.violations],
        equipment_states={k: equipment_to_response(v) for k, v in source.equipment_states.items()},
    )
