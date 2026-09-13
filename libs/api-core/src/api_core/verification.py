from __future__ import annotations

from dataclasses import dataclass

from api_core.action import Action, Add, Pour, Strain
from api_core.equipment import Equipment
from api_core.material import Material


@dataclass(frozen=True, slots=True)
class StepViolation:
    step: int
    kind: str
    message: str


@dataclass(frozen=True, slots=True)
class VerificationResult:
    valid: bool
    violations: tuple[StepViolation, ...]
    equipment_states: dict[str, Equipment]


def _verify_add(
    step: int,
    action: Add,
    materials: dict[str, Material],
    state: dict[str, Equipment],
) -> list[StepViolation]:
    violations: list[StepViolation] = []

    if action.material_id not in materials:
        violations.append(
            StepViolation(
                step, "material_not_found", f"Material '{action.material_id}' not in registry"
            )
        )
        return violations

    if action.equipment_id not in state:
        violations.append(
            StepViolation(
                step, "equipment_not_found", f"Equipment '{action.equipment_id}' not found"
            )
        )
        return violations

    material = materials[action.material_id]
    eq = state[action.equipment_id]

    if not eq.can_accept(material):
        violations.append(
            StepViolation(
                step,
                "tag_not_accepted",
                f"Equipment '{eq.id}' does not accept tags {material.tags}",
            )
        )
        return violations

    if action.volume_ml > eq.remaining_capacity_ml():
        violations.append(
            StepViolation(
                step,
                "capacity_exceeded",
                f"Equipment '{eq.id}' has {eq.remaining_capacity_ml():.1f}ml free, "
                f"need {action.volume_ml:.1f}ml",
            )
        )
        return violations

    new_eq = eq.add(material, action.volume_ml)
    violations.extend(
        StepViolation(step, "constraint_violated", cv.message)
        for cv in new_eq.contents.check_constraints()
    )

    if not violations:
        state[action.equipment_id] = new_eq

    return violations


def _verify_pour(
    step: int,
    action: Pour,
    state: dict[str, Equipment],
) -> list[StepViolation]:
    violations: list[StepViolation] = []

    violations.extend(
        StepViolation(step, "equipment_not_found", f"Equipment '{eid}' not found")
        for eid in (action.from_equipment_id, action.to_equipment_id)
        if eid not in state
    )

    if violations:
        return violations

    from_eq = state[action.from_equipment_id]
    to_eq = state[action.to_equipment_id]

    if from_eq.contents.total_volume_ml > to_eq.remaining_capacity_ml():
        violations.append(
            StepViolation(
                step,
                "capacity_exceeded",
                f"Equipment '{to_eq.id}' has {to_eq.remaining_capacity_ml():.1f}ml free, "
                f"need {from_eq.contents.total_volume_ml:.1f}ml",
            )
        )
        return violations

    emptied, filled = from_eq.pour_into(to_eq)
    violations.extend(
        StepViolation(step, "constraint_violated", cv.message)
        for cv in filled.contents.check_constraints()
    )

    if not violations:
        state[action.from_equipment_id] = emptied
        state[action.to_equipment_id] = filled

    return violations


def _verify_strain(
    step: int,
    action: Strain,
    state: dict[str, Equipment],
) -> list[StepViolation]:
    violations: list[StepViolation] = []

    violations.extend(
        StepViolation(step, "equipment_not_found", f"Equipment '{eid}' not found")
        for eid in (action.from_equipment_id, action.to_equipment_id)
        if eid not in state
    )

    if violations:
        return violations

    from_eq = state[action.from_equipment_id]
    to_eq = state[action.to_equipment_id]
    strained_volume = from_eq.contents.strain(action.remove_tags).total_volume_ml

    if strained_volume > to_eq.remaining_capacity_ml():
        violations.append(
            StepViolation(
                step,
                "capacity_exceeded",
                f"Equipment '{to_eq.id}' has {to_eq.remaining_capacity_ml():.1f}ml free, "
                f"strained volume is {strained_volume:.1f}ml",
            )
        )
        return violations

    emptied, filled = from_eq.strain_into(to_eq, action.remove_tags)
    violations.extend(
        StepViolation(step, "constraint_violated", cv.message)
        for cv in filled.contents.check_constraints()
    )

    if not violations:
        state[action.from_equipment_id] = emptied
        state[action.to_equipment_id] = filled

    return violations


def verify(
    actions: list[Action],
    materials: dict[str, Material],
    equipment: dict[str, Equipment],
) -> VerificationResult:
    violations: list[StepViolation] = []
    state: dict[str, Equipment] = dict(equipment)

    for step_index, action in enumerate(actions):
        step = step_index + 1
        match action:
            case Add():
                violations.extend(_verify_add(step, action, materials, state))
            case Pour():
                violations.extend(_verify_pour(step, action, state))
            case Strain():
                violations.extend(_verify_strain(step, action, state))

    return VerificationResult(
        valid=len(violations) == 0,
        violations=tuple(violations),
        equipment_states=state,
    )
