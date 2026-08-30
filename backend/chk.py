import asyncio
import sys
sys.path.insert(0, r'F:\github clone rep\HCL_Amplified')
from backend.app.database.connection import AsyncSessionLocal
from backend.app.models import Assessment
from sqlalchemy import select

async def check():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(Assessment))
        for a in res.scalars().all():
            qs = a.questions
            null_ca = sum(1 for q in qs if q.get('correct_answer') is None)
            valid_ca = len(qs) - null_ca
            sample_ca = qs[0].get('correct_answer') if qs else 'NO_Q'
            print(a.title[:35], 'total=', len(qs), 'null_ca=', null_ca, 'sample_ca=', sample_ca)

asyncio.run(check())
