from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.models.feature_spec import FeatureSpec
from app.services.spec_service import SpecService

router = APIRouter()

@router.post("/upload")
async def upload_spec(spec: FeatureSpec, session: Session = Depends(get_session)):
    
    result = await SpecService.process_spec(spec, session)

    return {
        "Message" : "Successfully uploaded spec",
        "data" : result
    }