
from fastapi import APIRouter
from app.routes import users, prospects, products, categories, country, stages, agents, enrollment, participants, events, materials

router = APIRouter()
router.include_router(users.router)
router.include_router(participants.router)
router.include_router(events.router)
router.include_router(materials.router)


router.include_router(prospects.router)
router.include_router(products.router)
router.include_router(categories.router)
router.include_router(country.router)
router.include_router(stages.router)
router.include_router(agents.router)
router.include_router(enrollment.router)
