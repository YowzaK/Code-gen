from fastapi import APIRouter
from app.models.feature_spec import FeatureSpec
from app.services.spec_service import SpecService

router = APIRouter()

@router.post("/upload")
async def upload_spec(spec: FeatureSpec):
    
    result = await SpecService.process_spec(spec)

    return {
        "Message" : "Successfully uploaded spec",
        "data" : result
    }