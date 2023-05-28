from fastapi import APIRouter
from .scripts import basic_scripts

router = APIRouter(
    tags=["Nmap Scanner"],
    prefix="/nmap_scanner",
)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/scan/{ip}")
async def scan_ip(ip: str):
    
    return basic_scripts.scan_domain(ip)


@router.get("/vuln_scan/{ip}")
async def scan_ip(ip: str):
    
    return basic_scripts.vuln_scan(ip)